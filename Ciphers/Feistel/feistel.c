#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h>
#include <openssl/sha.h> 

# define BLOCK 64 
# define KEY_LENGTH 10
# define N 5

//ADD keys
int main(void) {
  //Set up
  void sha256(char *string, char outputBuffer[32]);
  void copy_for_sign(unsigned char * dest, unsigned char * source, int l);
  void convert(int * output, char* str);
  void print_arr(int input[], int l);
  void e_round(unsigned char * L, unsigned char * R);
  void copy(unsigned char dest[], char source[], int l);
  
  char message[BLOCK] = {};
  memset(message, 0, BLOCK);
  //scanf("%[^\n]s",message);
  strcpy(message,"jonas");
  char K[KEY_LENGTH] = {};
  strcpy(K,"aaa");
  //Ecryption
  unsigned char L[BLOCK/2] = {0}, R[BLOCK/2] = {0};
  copy(L,message, BLOCK/2);
  copy(R,message+BLOCK/2,BLOCK/2);

  printf("L: %*.*s \n", 32, 32, L);
  printf("R: %s \n", R);  
  //printf("%lld", sizeof(L));
  //printf("%lld", sizeof(R));
  
  for (int k = 0; k < N; k++){  
    printf("%d round \n",k+1);
    e_round(L,R);  
  }
  Sleep(1000);
  //Decryption
  unsigned char buffer[BLOCK/2];
  copy_for_sign(buffer, R, BLOCK/2);
  copy_for_sign(R, L, BLOCK/2);
  copy_for_sign(L, buffer, BLOCK/2);
  for (int k = 0; k < N; k++){  
    printf("Decryption %d round \n",k+1);
    e_round(L,R);  
  }

  copy_for_sign(buffer, R, BLOCK/2);
  copy_for_sign(R, L, BLOCK/2);
  copy_for_sign(L, buffer, BLOCK/2);
  
  printf("Results \n");
  printf("L: %*.*s \n", 32, 32, L);
  printf("R: %*.*s \n", 32, 32, R);
  Sleep(100000);
  return 0;
}

void print_arr(int* input, int l){
  for (int i = 0; i < l;i++){
    printf("%d,", *(input+i));
  }
  printf("\n");
}

void copy(unsigned char * dest, char * source, int l){
  for (int i = 0; i < l; i++){
    dest[i] = (unsigned)source[i];
  }
}
//it made some warnings about casting
void copy_for_sign(unsigned char * dest, unsigned char * source, int l){
  for (int i = 0; i < l; i++){
    dest[i] = source[i];
  }
}


void e_round(unsigned char * L, unsigned char * R){
  char unsigned L_1[BLOCK/2];
  char unsigned R_1[BLOCK/2];  
  copy_for_sign(L_1, R, BLOCK/2);
  //static unsigned char F[32];
  SHA256(R, BLOCK/2, R_1);
  //printf("%lld \n", sizeof(R_1));
  for(int i = 0; i < BLOCK/2; i++){
    R[i] = R_1[i]^L[i]; 
  }
  copy_for_sign(L, L_1, BLOCK/2);
  printf("L: %*.*s \n", 32, 32, L);
  printf("R: %*.*s \n", 32, 32, R);
}

void convert(int * output, char * message){
   int l = strlen(message);
   for (int i = 0; i < l;i++){
      output[i] = (int)(message[i]);
   }
}

