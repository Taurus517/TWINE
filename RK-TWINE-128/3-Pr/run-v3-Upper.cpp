#include <fstream>
#include <unistd.h> 
#include <string.h>  
#include <string>
#include <iostream>
#include <time.h>
using namespace std;

int Block = 64; 
int Key = 128;

int r0 = 3; //
int total_Pr_E0 = 6; //

int main(){

    char filename1[5000];
    char filename2[5000];

    sprintf(filename1, "stp T-TWINE-128_Boomerang_Pr_RK_%dR_Upper_%dPr.cvc", r0, total_Pr_E0);
    sprintf(filename2, "T-TWINE-128_Boomerang_Pr_RK_%dR_Upper_%dPr.cvc", r0, total_Pr_E0);

    FILE *fp1 = NULL; 
    FILE *fp2 = NULL; 
    fp1 = popen(filename1, "r"); 
    
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


    ifstream ModifyRes;
    ModifyRes.open("result.txt", ios::in);
    string str_read;                
    getline(ModifyRes, str_read);
    ModifyRes.close();

    while(str_read.compare("Valid.") != 0){
        
        string str;

        for(int i = 0; i < r0+1; i++){
            for(int j = 0; j < 16; j++){ 
                ifstream fr;
                fr.open("result.txt", ios::in); 

                string read;
                int pos1, pos2;
            
                while (!fr.eof()){  
                    getline(fr, read);
                    string cc = "ASSERT( E0_X0_" + to_string(i) + "_" + to_string(j) + " = 0x";
                    pos1 = read.find(cc);
                    pos2 = read.find("0x");
                    if(pos1 >= 0){
                        str += read.substr(pos2+2, 1);
                    }
                }
                fr.close();
            }
            
            for(int j = 0; j < 32; j++){ 
                ifstream fr;
                fr.open("result.txt", ios::in); 

                string read;
                int pos1, pos2;
            
                while (!fr.eof()){  
                    getline(fr, read);
                    string cc = "ASSERT( E0_K0_" + to_string(i) + "_" + to_string(j) + " = 0x";
                    pos1 = read.find(cc);
                    pos2 = read.find("0x");
                    if(pos1 >= 0){
                        str += read.substr(pos2+2, 1);
                    }
                }
                fr.close();
            }
            
        }

        
        ifstream OriginalCVC;
        OriginalCVC.open(filename2, ios::in);
        ofstream TempCVC;
        TempCVC.open("temp.cvc", ios::out); 

        string del1 = "QUERY FALSE;";
        string del2 = "COUNTEREXAMPLE;";
        string del;
        while(getline(OriginalCVC, del)){
            if(del.compare(del1)!=0){
            if(del.compare(del2)!=0){
                TempCVC << del << endl;
            }}
        }
        OriginalCVC.close();
        TempCVC.close();

        ifstream TempCVC1;
        TempCVC1.open("temp.cvc", ios::in);
        ofstream OriginalCVC1;
        OriginalCVC1.open(filename2, ios::out); 
        while(getline(TempCVC1, del)){
            OriginalCVC1 << del << endl;
        }
        OriginalCVC1.close();
        TempCVC1.close();


        ofstream OriginalCVC2;
        OriginalCVC2.open(filename2, ios::app);

    
        string str0 = "";
        for(int round = 0; round < r0+1; round++){  
            for(int state = 0; state < 16; state++){
                str0 += ("E0_X0_" + to_string(round) + "_" + to_string(state) + "@");
            } 
            for(int state = 0; state < 32; state++){
                if((round==r0)&&(state==31)){
                    str0 += ("E0_K0_" + to_string(round) + "_" + to_string(state));
                }
                else{
                    str0 += ("E0_K0_" + to_string(round) + "_" + to_string(state) + "@");
                }
            }     
        }

       
        string strc = "ASSERT NOT(" + str0 + " = 0hex" + str + ");";
        OriginalCVC2 << strc;
        OriginalCVC2 << endl << del1 << endl << del2 << endl;
        OriginalCVC2.close();


        FILE *Refresh = NULL; 
        FILE *fh1=NULL;
        Refresh = popen(filename1, "r"); 
        
        char buff1;
        buff1 = getc(Refresh);
        fh1 = fopen("result.txt", "w");  
        while (buff1 != EOF)  
        {
            fputc(buff1, fh1);
            buff1 = getc(Refresh);
        }
        pclose(Refresh); 
        fclose(fh1);
        

        ifstream ModifyRes1;
        ModifyRes1.open("result.txt",ios::in); 
        getline(ModifyRes1, str_read);
        ModifyRes1.close();
    }       


    return 0;
}
