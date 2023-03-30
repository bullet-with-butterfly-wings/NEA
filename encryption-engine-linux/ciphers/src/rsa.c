#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include<time.h>
#include<math.h>
#include<unistd.h>

#include "../lib/library.h"

int main(){
  char *filename = "keys.out";
   
  // open the file for writing
  FILE *fp = fopen(filename, "r");
  if (fp == NULL)
  {
      printf("Error opening the file %s", filename);
      return -1;
  }

  huge e, d, n, m;
  if( fscanf(fp,"%llu \n %llu \n %llu", &n, &d, &e) != 1){
    printf("Error opening the file");
  }
  printf("Enter your message:");
  if(scanf("%llu", &m) != 1){
    printf("Error with reading the input");
  }
  huge scrambled = pow_mod(m, d, n);
  printf("Scrambled message: %llu \n", scrambled);
  huge decrypted = pow_mod(scrambled, e, n);
  printf("Decrypted message: %llu \n", decrypted);

  return 0;
}

