// g++ Em.cpp -o Em -lpthread
// g++ -std=c++11 Em.cpp -o Em -lpthread
// ./Em

#include <iostream>
#include <vector>
#include <random>
#include <cmath>
#include <chrono>
#include <mutex>
#include <thread>

using namespace std;


const int Block = 64;
const int Tweak = 64;
const int Key = 80;
const int ROUNDS = 36;

const int r0 = 8; //改
const int rm = 5; //改
const int r1 = 8; //改


const vector<int> delta_upper = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //改
const vector<int> key_upper = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //改

const vector<int> delta_lower = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //改
const vector<int> key_lower = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //改


const vector<int> Sbox = {0xC, 0x0, 0xF, 0xA, 0x2, 0xB, 0x9, 0x5,
                          0x8, 0x3, 0xD, 0x7, 0x1, 0xE, 0x6, 0x4};

const vector<int> Con = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x03, 0x06, 
                         0x0C, 0x18, 0x30, 0x23, 0x05, 0x0A, 0x14, 0x28,
                         0x13, 0x26, 0x0F, 0x1E, 0x3C, 0x3B, 0x35, 0x29,
                         0x11, 0x22, 0x07, 0x0E, 0x1C, 0x38, 0x33, 0x25,
                         0x09, 0x12, 0x24};

vector<int> ConH(35);
vector<int> ConL(35);
void Constant() {
    for (int i = 0; i < 35; i++) {
        ConH[i] = (Con[i] >> 3) & 0x07;
        ConL[i] = Con[i] & 0x07;
    }
}

const vector<int> Pi = {1, 2, 11, 6, 3, 0, 9, 4, 7, 10, 13, 14, 5, 8, 15, 12};
const vector<int> Pi_inv = {5, 0, 1, 4, 7, 12, 3, 8, 13, 6, 9, 2, 15, 10, 11, 14};
const vector<int> Pi_t = {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 0, 4, 2, 3, 5};
const vector<int> RK_80 = {1, 3, 4, 6, 13, 14, 15, 16};

vector<int> Rot_80;
vector<int> Rot_80_inv;
void initRotations() {
    for (int i = 4; i < 20; i++) {
        Rot_80.push_back(i);
    }
    for (int i : {1, 2, 3, 0}) {
        Rot_80.push_back(i);
    }

    for (int i : {19, 16, 17, 18}) {
        Rot_80_inv.push_back(i);
    }
    for (int i = 0; i < 16; i++) {
        Rot_80_inv.push_back(i);
    }
}

vector<vector<int>> TweakSchedule(vector<int> Ttemp, int R) {
    vector<vector<int>> TKAlltemp;

    for (int round = 0; round < R; round++) {
        
        vector<int> TK(Ttemp.begin(), Ttemp.begin() + 6);
        TKAlltemp.push_back(TK);  

        vector<int> temp(int(Tweak/4));
        for (int i = 0; i < int(Tweak/4); i++) {
            temp[i] = Ttemp[Pi_t[i]];
        }
        Ttemp = temp;
        
    }

    return TKAlltemp;
}

pair<vector<vector<int>>, vector<int>> KeySchedule_80(vector<int> Ktemp, int R0, int R1) {
    vector<vector<int>> RKAlltemp;
    
    for (int round = R0; round < R1; round++) {
        
        vector<int> RK;
        for (int i : RK_80) {
            RK.push_back(Ktemp[i]);
        }
        RKAlltemp.push_back(RK);

        for (int i = 0; i < int(Key/4); i++) {
            if (i == 1) {
                Ktemp[1] ^= Sbox[Ktemp[0]];
            } else if (i == 4) {
                Ktemp[4] ^= Sbox[Ktemp[16]];
            } else if (i == 7) {
                Ktemp[7] ^= ConH[round];
            } else if (i == 19) {
                Ktemp[19] ^= ConL[round];
            }
        }

        vector<int> temp(int(Key/4));
        for (int i = 0; i < int(Key/4); i++) {
            temp[i] = Ktemp[Rot_80[i]];
        }
        Ktemp = temp;
        
    }

    return {RKAlltemp, Ktemp};
}

vector<vector<int>> KeySchedule_80_inv(vector<int> Ktemp, int R0, int R1) {
    vector<vector<int>> RKAlltemp;

    for (int round = R1 - 1; round >= R0; round--) {
        
        vector<int> temp(int(Key/4));
        for (int i = 0; i < int(Key/4); i++) {
            temp[i] = Ktemp[Rot_80_inv[i]];
        }
        Ktemp = temp;

        for (int i = 0; i < int(Key/4); i++) {
            if (i == 1) {
                Ktemp[1] ^= Sbox[Ktemp[0]];
            } else if (i == 4) {
                Ktemp[4] ^= Sbox[Ktemp[16]];
            } else if (i == 7) {
                Ktemp[7] ^= ConH[round];
            } else if (i == 19) {
                Ktemp[19] ^= ConL[round];
            }
        }

        vector<int> RK;
        for (int i : RK_80) {
            RK.push_back(Ktemp[i]);
        }
        RKAlltemp.push_back(RK);
        
    }

    return RKAlltemp;
}

vector<int> Enc(vector<int> Plain, vector<vector<int>> RKAlltemp, const vector<vector<int>> &TKAlltemp, int R) {

    for (int round = 0; round < R; round++) {
        
        int states = 6;
        for (int state = 0; state < int(Block/8); state++) {
            int temp1;
            if (state == 2 || state == 6) {
                temp1 = Plain[2 * state] ^ RKAlltemp[round][state];
            } else {
                states--; 
                temp1 = Plain[2 * state] ^ RKAlltemp[round][state] ^ TKAlltemp[round][states];
            }
            temp1 = Sbox[temp1];
            Plain[2 * state + 1] ^= temp1;
        }

        vector<int> temp(int(Block/4));
        for (int state = 0; state < int(Block/4); state++) {
            temp[state] = Plain[Pi[state]];
        }
        Plain = temp;
        
    }

    return Plain;
}

vector<int> Dec(vector<int> Cipher, vector<vector<int>> RKAlltemp, const vector<vector<int>> &TKAlltemp, int R) {
    int Rcount = 0;

    for (int round = R - 1; round >= 0; round--) {
        
        vector<int> temp(int(Block/4));
        for (int state = 0; state < int(Block/4); state++) {
            temp[state] = Cipher[Pi_inv[state]];
        }
        Cipher = temp;

        int states = 6;
        for (int state = 0; state < int(Block/8); state++) {
            int temp2;
            if (state == 2 || state == 6) {
                temp2 = Cipher[2 * state] ^ RKAlltemp[Rcount][state];
            } else {
                states--;
                temp2 = Cipher[2 * state] ^ RKAlltemp[Rcount][state] ^ TKAlltemp[round][states];
            }
            temp2 = Sbox[temp2];
            Cipher[2 * state + 1] ^=  temp2;
        }
        Rcount++;
        
    }

    return Cipher;
}


mutex mtx;
int TrueCount = 0;
int FalseCount = 0;

void process_data(uint64_t start, uint64_t end, const vector<vector<int>> &TKAll){

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> rd4V(0, 15);
    
    for (uint64_t count = start; count < end; count++){

        vector<int> K1(int(Key/4), 0);
        for (int i = 0; i < int(Key/4); i++) {
            K1[i] = rd4V(gen);
        }
        vector<vector<int>> RKAll_1 = KeySchedule_80(K1, r0, r0 + rm).first;
        vector<int> K_1 = KeySchedule_80(K1, r0, r0 + rm).second;


        vector<int> K2(int(Key/4), 0);
        for (int i = 0; i < int(Key/4); i++) {
            K2[i] = K1[i] ^ key_upper[i];
        }
        vector<vector<int>> RKAll_2 = KeySchedule_80(K2, r0, r0 + rm).first;
        vector<int> K_2 = KeySchedule_80(K2, r0, r0 + rm).second;



        vector<int> K3(int(Key/4), 0);
        for (int i = 0; i < int(Key/4); i++) {
            K3[i] = K_1[i] ^ key_lower[i];
        }
        vector<vector<int>> RKAll_3 = KeySchedule_80_inv(K3, r0, r0 + rm);

        vector<int> K4(int(Key/4), 0);
        for (int i = 0; i < int(Key/4); i++) {
            K4[i] = K_2[i] ^ key_lower[i];
        }
        vector<vector<int>> RKAll_4 = KeySchedule_80_inv(K4, r0, r0 + rm);



        vector<int> P1(int(Block/4), 0);
        for (int i = 0; i < int(Block/4); i++) {
            P1[i] = rd4V(gen);
        }
        vector<int> C1 = Enc(P1, RKAll_1, TKAll, rm);

        vector<int> C3(int(Block/4), 0);
        for (int i = 0; i < int(Block/4); i++) {
            C3[i] = C1[i] ^ delta_lower[i];
        }
        vector<int> P3 = Dec(C3, RKAll_3, TKAll, rm);



        vector<int> P2(int(Block/4), 0);
        for (int i = 0; i < int(Block/4); i++) {
            P2[i] = P1[i] ^ delta_upper[i];
        }
        vector<int> C2 = Enc(P2, RKAll_2, TKAll, rm);

        vector<int> C4(int(Block/4), 0);
        for (int i = 0; i < int(Block/4); i++) {
            C4[i] = C2[i] ^ delta_lower[i];
        }
        vector<int> P4 = Dec(C4, RKAll_4, TKAll, rm);


        vector<int> result(int(Block/4), 0);
        for (int i = 0; i < int(Block/4); i++) {
            result[i] = P3[i] ^ P4[i];
        }

        mtx.lock();
        if (result == delta_upper) {
            TrueCount++;
        }else {
            FalseCount++;
        }
        mtx.unlock();
    }
}

int main() {

    auto start_time = chrono::high_resolution_clock::now();

    Constant();
    initRotations();

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> rd4V(0, 15);

    vector<int> T(int(Tweak/4), 0);
    for (int i = 0; i < int(Tweak/4); i++) {
        T[i] = rd4V(gen);
    }
    vector<vector<int>> TKAll = TweakSchedule(T, rm);


    int totalCount = 26;  //改
    uint64_t totalData = pow(2,totalCount);

    int num_threads = thread::hardware_concurrency(); //线程总数
    vector<thread> threads; 
    uint64_t chunk_size = totalData / num_threads; //每个线程处理的数据量
    
    
    for(int i = 0; i < num_threads; i++){
        uint64_t start = i * chunk_size;
        uint64_t end;

        if (i == num_threads-1) {
            end = totalData;
        }else {
            end = start + chunk_size;
        }
        threads.emplace_back(process_data, start, end, TKAll);
    }

    for (auto& t : threads) {
        t.join();
    }
    
    
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::minutes>(end_time - start_time).count();
    
    
    for(int i = 0; i < 16; i++){
        cout << delta_upper[i] << ",";
    }
    cout << endl;
    for(int i = 0; i < 20; i++){
        cout << key_upper[i] << ",";
    }
    cout << endl;
    for(int i = 0; i < 16; i++){
        cout << delta_lower[i] << ",";
    }
    cout << endl;
    for(int i = 0; i < 20; i++){
        cout << key_lower[i] << ",";
    }
    cout << endl;
    

    cout << "TotalData = 2^" << float(log2(totalData)) << endl;
    cout << "TrueCount: " << TrueCount << endl;
    cout << "FalseCount: " << FalseCount << endl;
    cout << "runTime: " << duration << " 分钟" << endl << endl;

    return 0;
}
