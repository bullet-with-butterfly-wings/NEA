#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include<unistd.h>
#include "../lib/library.h"

# define BLOCK 64 
# define KEY_LENGTH 10
# define N 2

//ADD keys
int main(int argc, char* argv[]) {
	//Set up
	int encrypt = atoi(argv[1]);
	void e_round(char* L, char* R, char* K);
	//key
	char K[KEY_LENGTH+1] = {"\0"}; //"Enter your key (max %d characters):"
	strncpy(K,argv[2], KEY_LENGTH);
	char K_now[KEY_LENGTH/N+1] = {"\0"}; //ending with zero
	strncpy(K_now, K, KEY_LENGTH/N);
	//message
  
	char message[BLOCK] = {"\0"};
	FILE *file;
    char *filename = "buffer.txt";
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("Error opening file");
        return 1;
    }
    // Get the size of the file
    fseek(fp, 0L, SEEK_END);
    int file_size = ftell(fp);
    rewind(fp);
    if(fread(message, file_size, 1, fp) != 1){
		printf("Problem with reading");
	}
    //printf("%s \n", buffer);
	fclose(fp);
    //Ecryption
	char L[BLOCK/2] = {"\0"}, R[BLOCK/2] = {"\0"};
	strncpy(L, message, BLOCK/2);
	strncpy(R,message+BLOCK/2,BLOCK/2);

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
	printf("%.*s", BLOCK/2, L);
	printf("%.*s\n", BLOCK/2, R);
	return 0;
}

void e_round(char* L,char* R, char* K){
  char buffer[BLOCK/2];
  char hash[256]; 

  strncpy(buffer, R, BLOCK/2);

  char F[BLOCK/2+KEY_LENGTH] = {"\0"};
  strncpy(F, R, BLOCK/2);
  //printf("F: %.*s \n",BLOCK/2, F);
  strncpy(F+BLOCK/2, K, KEY_LENGTH);
  //printf("F: %.*s \n",BLOCK/2+KEY_LENGTH, F);
  //the problem is you are passing empty string to hash
  SHA256(F, hash, BLOCK/2+KEY_LENGTH);
  for(int i = 0; i < BLOCK/2; i++){
    R[i] = hash[i]^L[i]; 
  }
  //strncpy(R+BLOCK/2, "0", 1); //zaplata xd 

  strncpy(L, buffer, BLOCK/2);
  //printf("L: %.*s \n", BLOCK/2, L);
  //printf("R: %.*s \n",BLOCK/2, R);
}


