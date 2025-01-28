#include <fstream>
#include <unistd.h> 
#include <string.h>  
#include <string>
#include <iostream>
#include <time.h>
using namespace std;

int Data[7][3] = {{8,5,9},
                   {9,5,8},
                   {8,6,8},
                   {7,7,8},
                   {8,7,7},
                   {7,8,7},
                   {7,9,6}
                   }; //

int main(){

    char filename[5000];
    char filename1[5000];

    for(int count = 0; count < 7; count++){ //

        int r0 = Data[count][0];
        int rm = Data[count][1];
        int r1 = Data[count][2];

    for(int totalASAK = 57; totalASAK < 64; totalASAK++){ //
    
        time_t start_t, end_t;
        double diff_t;

        time(&start_t);

        sprintf(filename, "stp TWINE-80_Boomerang_ASbox_RK_%d+%d+%dR_%dASAK.cvc", r0, rm, r1, totalASAK); 

        FILE *fp1 = NULL; 
        FILE *fp2 = NULL; 
        fp1 = popen(filename, "r"); 
        
        char buff;
        buff = getc(fp1);
        fp2 = fopen("result.txt", "w");
        while (buff != EOF)  
        {
            fputc(buff, fp2);
            buff = getc(fp1);
        }
        pclose(fp1); 
        fclose(fp2);

        time(&end_t);
        diff_t = difftime(end_t, start_t);

        ifstream ModifyRes;
        ModifyRes.open("result.txt", ios::in);
        string str_read;                
        getline(ModifyRes, str_read);
        ModifyRes.close();

        if(str_read.compare("Valid.") != 0){
            cout << "E0+Em+E1 = " << r0 << "+" << rm << "+" << r1 << ", totalASAK = " << totalASAK << ": have trail, " << "time = " << diff_t << endl;
        } 
        else{
            cout << "E0+Em+E1 = " << r0 << "+" << rm << "+" << r1 << ", totalASAK = " << totalASAK << ": no trail, " << "time = " << diff_t << endl;
        }      


        sprintf(filename1, "rm TWINE-80_Boomerang_ASbox_RK_%d+%d+%dR_%dASAK.cvc", r0, rm, r1, totalASAK); 
        FILE *fRemove = NULL; 
        fRemove = popen(filename1, "r"); 
        pclose(fRemove);

    }}

    return 0;
}
