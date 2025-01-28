#include <fstream>
#include <unistd.h> 
#include <string.h>  
#include <string>
#include <iostream>
#include <time.h>
using namespace std;

int main(){
    
    char filename1[5000];
    char filename2[5000];

    sprintf(filename1, "g++ -std=c++11 Em.cpp -o Em_21R_O2_7-8-6 -lpthread"); 
    sprintf(filename2, "./Em_21R_O2_7-8-6"); 

    
    FILE *fp1 = NULL; 
    fp1 = popen(filename1, "r"); 
    pclose(fp1); 

    FILE *fp2 = NULL; 
    fp2 = popen(filename2, "r");   
    FILE *fp3 = NULL; 

    char buff;
    buff = getc(fp2);
    fp3 = fopen("result.txt", "a+");
    while (buff != EOF)  
    {
        fputc(buff, fp3);
        buff = getc(fp2);
    }
    pclose(fp2); 
    fclose(fp3);


    ifstream ModifyRes;
    ModifyRes.open("result.txt", ios::in);
    string str_read;                
    getline(ModifyRes, str_read);
    ModifyRes.close();

    while(str_read.compare("TotalData = 2^30") != 0){
        FILE *Refresh1 = NULL; 
        Refresh1 = popen(filename1, "r"); 
        pclose(Refresh1); 

        FILE *Refresh2 = NULL; 
        Refresh2 = popen(filename2, "r"); 
        FILE *fh1=NULL;
        
        char buff1;
        buff1 = getc(Refresh2);
        fh1 = fopen("result.txt", "a+");  
        while (buff1 != EOF)  
        {
            fputc(buff1, fh1);
            buff1 = getc(Refresh2);
        }

        pclose(Refresh2); 
        fclose(fh1);
        

        ifstream ModifyRes1;
        ModifyRes1.open("result.txt",ios::in); 
        getline(ModifyRes1, str_read);
        ModifyRes1.close();
    }       


    return 0;
}
