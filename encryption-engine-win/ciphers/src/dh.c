#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "../lib/library.h"
#include <unistd.h> // for windows #include<windows.h>


int main(void) {
  huge g = 7; //primitive root - usually prime
  huge n = 2147483647; //prime
  srand(time(NULL));
  //First person
  huge a = rand()+1;//not suitable for encryption 
  huge A = pow_mod(g,a,n);
  //Second person
  huge b = rand()+1; 
  huge B = pow_mod(g,b,n);
  //Result
  huge key_1 = pow_mod(B,a,n);
  huge key_2 = pow_mod(A,b,n);
  printf("%lld \n", key_1);
  printf("%lld \n", key_2);
  return 0;
}
