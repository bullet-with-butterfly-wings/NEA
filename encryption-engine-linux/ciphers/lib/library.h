#ifndef ciphers
#define ciphers

typedef unsigned long long huge;

int prime(huge);

huge gcd(huge, huge);
huge gcdExtended(huge a, huge b, huge *x, huge *y);
huge  pow_mod(huge b, huge e, huge n);
void SHA256(char* data, char* hashStr, int strLen);
  
#endif