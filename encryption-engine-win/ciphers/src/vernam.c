#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#include<unistd.h>

#define KEY_LENGTH 10

void vernam(char *plaintext, char *key, char *ciphertext, int len) {
  for (int i = 0; i < len; i++) {
    ciphertext[i] = plaintext[i] ^ key[i % KEY_LENGTH];
  }
}

int main(int argc, char* argv[]){
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
    char buffer[255] = {'\0'};
    if(fread(buffer, file_size, 1, fp) != 1){
		  printf("Problem with reading");
	  }
    //printf("%s \n", buffer);
    fclose(fp);
    printf("%s",buffer);
    char *key = argv[1];
    char ciphertext[255] = {"\0"};
    vernam(buffer, key, ciphertext, strlen(buffer));
    //printf("CipherText: %s \n",ciphertext);
    FILE *cp = fopen(filename, "w");
    fwrite(ciphertext, strlen(ciphertext), 1, cp);
    fclose(cp);
    return 0;
}