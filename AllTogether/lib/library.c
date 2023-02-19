typedef unsigned long long huge;

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>


int prime(huge n){ //Fermats primality test
    if (n == 2){
        return 1;
    }
    if (n % 2 == 0){
        return 0;
    }
    for (int i = 0; i < 10; i++)
    {
        huge a = 1 + rand()/(RAND_MAX/sqrt(n) + 1);
        huge res = 1;
        for (huge i = 0; i < n-1; i++){
            res = res*a % n;
        }
        if (res != 1){
            return 0;
        }
        /*printf("%d/10 approved \n",i+1);*/
    }
    return 1;
}
    
huge gcd(huge a, huge b)
{
  if (b == 0){
      return a;
  }    
  return gcd(b, a % b);
}

huge pow_mod(huge b, huge e, huge mod){
  huge ans = 1;
  if (b == 0){
    return 0;
  }
  while (e > 0){
    if ((e % 2) == 1){
      ans = (ans*b) % mod;
    }
    e = e/2;
    b = (b*b) % mod;
  }
  return ans; 
}

huge gcdExtended(huge a, huge b, huge *x, huge *y)
{
    // Base Case
    if (a == 0)
    {
        *x = 0;
        *y = 1;
        return b;
    }
  
    huge x1, y1; // To store results of recursive call
    huge g = gcdExtended(b%a, a, &x1, &y1);
  
    // Update x and y using results of recursive
    // call
    *x = y1 - (b/a) * x1;
    *y = x1;
  
    return g;
}

