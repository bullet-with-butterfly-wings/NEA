#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include<time.h>
#include<math.h>

#include "../lib/library.h"

int main(){
  //int prime(huge);
  //huge gcd(huge, huge), gcdExtended(huge a, huge b, huge *x, huge *y),  pow_mod(huge b, huge e, huge n);
  srand(time(0));  
  huge m = 0; // message
  huge d = 0; //public key
  huge e = 0; //private key
  huge n = 0; //HUGE n

  char *filename = "keys.out";
   
  // open the file for writing
  FILE *fp = fopen(filename, "w");
  if (fp == NULL)
  {
      printf("Error opening the file %s", filename);
      return -1;
  }
  
  for(;;){
    huge p = rand() % 600000;
    while(!prime(p)){
      p++;
    }
    huge q = rand() % 600000;
    while(!prime(q)){
      q++;
    }
    huge n = p*q;
    
    huge phi_n = (p-1)*(q-1);
      
    int search = 1;
    huge e = 0; 
    while (search){
      e = 2 + (rand() % (phi_n-2));
      search = (gcd(phi_n,e) > 1);
    }
    //This will be sent to second side
    
    huge x,y;
    gcdExtended(e, phi_n, &x, &y);

    huge d = x;
    if (log(d) < log(10)*190){
      //huge ciphertext = pow_mod(m,e,n);
      //huge res = pow_mod(ciphertext,d,n);
      //printf("%llu",res);
      fprintf(fp,"%llu\n%llu\n%llu",n,d,e);
      fclose(fp);
      return 0;
    }
  }
}
