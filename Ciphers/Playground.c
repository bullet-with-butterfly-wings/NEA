#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <windows.h>
#include <assert.h>

#define BLOCK 32
int main(){
    char *readFile(char *filename);
  
    unsigned char K[9];
    printf("Enter your key (max 9 characters):");
    scanf("%[^\n]%*c", K);
    unsigned char K_now[9];
    memcpy(K_now, &K[0],9);
    FILE *f1 = fopen("file.bin", "wb");
    if (f1) {
      size_t r1 = fwrite(K_now, sizeof K_now[0], 9, f1);
      printf("wrote %zu elements out of %d requested\n", r1,  2);
      fclose(f1);
    }
    printf("Cool");
    Sleep(1000);
    char *filename = "file.bin"; 
    // open the file for writing
    FILE *fp = fopen(filename, "r");
    if (fp == NULL)
    {
        printf("Error opening the file %s", filename);
        return -1;
    }
    printf("Cool");
    Sleep(1000);
    char *message = readFile("file.bin");
    fscanf(fp,"%s", message);
    
    printf("%s",message);
    printf("Cool");
    Sleep(1000);    
    //printf("Left half : %s\n",L);
    //printf("Right half : %s\n",R);
    return 0;
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