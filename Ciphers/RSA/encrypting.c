#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include<time.h>
#include<math.h>
#include<windows.h>

#include "..\library.h"

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
  fscanf(fp,"%llu \n %llu \n %llu", &n, &e, &d);
  printf("Enter your message:");
  scanf("%llu", &m);
  huge scrambled = pow_mod(m, d, n);
  printf("Scrambled message: %llu \n", scrambled);
  huge decrypted = pow_mod(scrambled, e, n);
  printf("Decrypted message: %llu \n", decrypted);

  Sleep(7000); //millisecond
  return 0;
  }

