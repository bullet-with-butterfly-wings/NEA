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
  void e_round(unsigned char * L, unsigned char * R, unsigned char * K);
  void copy(unsigned char dest[], char source[], int l);
  //key
  char K[KEY_LENGTH] = {"\0"};
  printf("Enter your key (max %d characters):",KEY_LENGTH-1);
  scanf("%[^\n]%*c", K);
  unsigned char K_now[KEY_LENGTH/N];
  //strcpy(K,"");
  memcpy(K_now, &K[0],KEY_LENGTH/N);

  //message
  char message[BLOCK];
  memset(message, 0, BLOCK);
  printf("Enter your message:");
  scanf("%[^\n]%*c", message);
  //strcpy(message,"");
  
  //fprintf(fp, "%s \n",K);
  //Ecryption
  unsigned char L[BLOCK/2] = {0}, R[BLOCK/2] = {0};
  copy(L,message, BLOCK/2);
  copy(R,message+BLOCK/2,BLOCK/2);

  printf("L: %*.*s \n", 32, 32, L);
  printf("R: %s \n", R);  


  for (int k = 0; k < N; k++){  
    printf("%d round \n",k+1);
    memcpy(K_now, &K[k*KEY_LENGTH/N], KEY_LENGTH/N);
    e_round(L,R, K_now);  
  }
  FILE *f1 = fopen("data.bin", "wb");
  if (f1) {
      fputs(L[0], f1);
      fwrite(L, 1, BLOCK/2, f1);
      fwrite(R, 1, BLOCK/2, f1);
      fclose(f1);
    }
 
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

void convert(int * output, char * message){
   int l = strlen(message);
   for (int i = 0; i < l;i++){
      output[i] = (int)(message[i]);
   }
}

