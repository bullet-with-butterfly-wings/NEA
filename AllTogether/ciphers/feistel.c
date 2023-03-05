#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include<unistd.h>
#include "lib/library.h"

# define BLOCK 64 
# define KEY_LENGTH 10
# define N 2

//ADD keys
int main(int argc, char* argv[]) {
	//Set up
	int encrypt = atoi(argv[1]);
	void print_arr(int input[], int l);
	void e_round(char* L, char* R, char* K);
	//key
	char K[KEY_LENGTH+1] = {"\0"}; //"Enter your key (max %d characters):"
	strncpy(K,argv[2], KEY_LENGTH);
	//scanf("%[^\n]%*c", K);
	char K_now[KEY_LENGTH/N+1] = {"\0"}; //ending with zero
	strncpy(K_now, K, KEY_LENGTH/N);
	//message
  
	char message[BLOCK] = {"\0"};
	FILE *file;
    char *filename = "../buffer.txt";
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("Error opening file");
        return 1;
    }
    // Get the size of the file
    fseek(fp, 0L, SEEK_END);
    int file_size = ftell(fp);
    rewind(fp);
    fread(message, file_size, 1, fp);
    //printf("%s \n", buffer);
	fclose(fp);
	//fprintf(fp, "%s \n",K);
    //Ecryption
	char L[BLOCK/2] = {"\0"}, R[BLOCK/2] = {"\0"};
	strncpy(L, message, BLOCK/2);
	strncpy(R,message+BLOCK/2,BLOCK/2);

	printf("L: %.*s \n", BLOCK/2, L);
	printf("R: %.*s \n",BLOCK/2, R);  
	if (encrypt == 1){
		for (int k = 0; k < N; k++){  
			strncpy(K_now, &K[k*KEY_LENGTH/N], KEY_LENGTH/N);
			e_round(L,R, K_now);  
		}
	}else{
		char buffer[BLOCK/2];
		strncpy(buffer,L,BLOCK/2);
		strncpy(L,R,BLOCK/2);
		strncpy(R,buffer,BLOCK/2);
		for (int k = 0; k < N; k++){  
			strncpy(K_now, &K[(N-k-1)*KEY_LENGTH/N], KEY_LENGTH/N);
			e_round(L,R, K_now);  
		}
		strncpy(buffer,L,BLOCK/2);
		strncpy(L,R,BLOCK/2);
		strncpy(R,buffer,BLOCK/2);
    }

	FILE *f1 = fopen(filename, "w");
	if (f1) {
    	fwrite(L, 1, BLOCK/2, f1);
    	fwrite(R, 1, BLOCK/2, f1);
    	fclose(f1);
    }
	return 0;
}

void print_arr(int* input, int l){
  for (int i = 0; i < l;i++){
    printf("%d,", *(input+i));
  }
  printf("\n");
}


//it made some warnings about casting


void e_round(char* L,char* R, char* K){
  char buffer[BLOCK/2];
  char hash[256]; 

  strncpy(buffer, R, BLOCK/2);

  char F[BLOCK/2+KEY_LENGTH] = {"\0"};
  strncpy(F, R, BLOCK/2);
  strncpy(F+BLOCK/2, K, KEY_LENGTH);
  SHA256(F, hash);
  //printf("%lld \n", sizeof(R_1));

  for(int i = 0; i < BLOCK/2; i++){
    R[i] = hash[i]^L[i]; 
  }
  //strncpy(R+BLOCK/2, "0", 1); //zaplata xd 

  strncpy(L, buffer, BLOCK/2);
  //printf("L: %.*s \n", BLOCK/2, L);
  //printf("R: %.*s \n",BLOCK/2, R);
}


