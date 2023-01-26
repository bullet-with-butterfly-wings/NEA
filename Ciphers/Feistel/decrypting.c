#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h>
#include <assert.h>
#include <openssl/sha.h> 

# define BLOCK 64 
# define KEY_LENGTH 10
# define N 5

//ADD keys
int main(void) {
  //Set up
  char *readFile(char *filename);
  void sha256(char *string, char outputBuffer[32]);
  void copy_for_sign(unsigned char * dest, unsigned char * source, int l);
  void convert(int * output, char* str);
  void print_arr(int input[], int l);
  void e_round(unsigned char * L, unsigned char * R, unsigned char * K);
  void copy(unsigned char dest[], char source[], int l);
  
  //key
  char K[KEY_LENGTH] = {"\0"};
  printf("Enter your key (max 9 characters):");
  scanf("%[^\n]%*c", K);
  unsigned char K_now[KEY_LENGTH/N] = {0};
  memcpy(K_now, &K[0],KEY_LENGTH/N);

  char *filename = "data.bin"; 
  // open the file for writing
  FILE *fp = fopen(filename, "r");
  if (fp == NULL)
  {
      printf("Error opening the file %s", filename);
      return -1;
  }
  
  char *message = readFile("data.bin");
  fscanf(fp,"%s", message);
  unsigned char L[BLOCK/2] = {0}, R[BLOCK/2] = {0};
  copy(L,message, BLOCK/2);
  copy(R,message+BLOCK/2,BLOCK/2);  
  printf("L: %*.*s \n", 32, 32, L);
  printf("R: %*.*s \n", 32, 32, R);
  //Decryption - key is reversed

  unsigned char buffer[BLOCK/2] = {0};
  copy_for_sign(buffer, R, BLOCK/2);
  copy_for_sign(R, L, BLOCK/2);
  copy_for_sign(L, buffer, BLOCK/2);
  
  for (int k = 0; k < N; k++){  
    printf("Decryption %d round \n",k+1);
    memcpy(K_now, &K[(N-1-k)*KEY_LENGTH/N], KEY_LENGTH/N);
    e_round(L,R, K_now);  
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


void e_round(unsigned char * L, unsigned char * R, unsigned char * K){
  char unsigned L_1[BLOCK/2];
  char unsigned R_1[BLOCK/2];  
  copy_for_sign(L_1, R, BLOCK/2);

  unsigned char F[BLOCK/2+KEY_LENGTH];
  memset(F, 0, BLOCK/2+KEY_LENGTH);
  memcpy(F, R, BLOCK/2);
  memcpy(F+BLOCK/2, K, KEY_LENGTH);

  SHA256(F, BLOCK/2 + KEY_LENGTH, R_1);
  //printf("%lld \n", sizeof(R_1));
  for(int i = 0; i < BLOCK/2; i++){
    R[i] = R_1[i]^L[i]; 
  }
  copy_for_sign(L, L_1, BLOCK/2);
  printf("L: %*.*s \n", 32, 32, L);
  printf("R: %*.*s \n", 32, 32, R);
}

char *readFile(char *filename) {
    FILE *f = fopen(filename, "rt");
    assert(f);
    fseek(f, 0, SEEK_END);
    long length = ftell(f);
    fseek(f, 0, SEEK_SET);
    char *buffer = (char *) malloc(length + 1);
    buffer[length] = '\0';
    fread(buffer, 1, length, f);
    fclose(f);
    return buffer;
}

void convert(int * output, char * message){
   int l = strlen(message);
   for (int i = 0; i < l;i++){
      output[i] = (int)(message[i]);
   }
}

