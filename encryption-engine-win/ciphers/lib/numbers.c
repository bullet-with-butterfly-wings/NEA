typedef unsigned long long huge;

// Include libraries that will be used throughout the code
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

// Function to test if a number is prime using Fermat's primality test (probabilistic)
int prime(huge n){
    if (n == 2){ // 2 is a prime number
        return 1;
    }
    if (n % 2 == 0){ // If n is even, it is not prime
        return 0;
    }
    // Perform the test 10 times
    for (int i = 0; i < 10; i++)
    {
        // Generate a random number a between 1 and sqrt(n)
        huge a = 1 + rand()/(RAND_MAX/sqrt(n) + 1);
        huge res = 1;
        // Calculate a^(n-1) % n
        for (huge i = 0; i < n-1; i++){
            res = res*a % n;
        }
        // If the result is not 1, n is composite (not prime)
        if (res != 1){
            return 0;
        }
    }
    // If the test passes all 10 times, n is probably prime
    return 1;
}
    
huge gcd(huge a, huge b) //Euler's algorithm for the greatest common divisor
{
  if (b == 0){
      return a;
  }    
  return gcd(b, a % b); //Return the greatest common divisor of the smaller number and the remainder of a/b
}

huge pow_mod(huge b, huge e, huge mod){ //The modular exponentiation algorithm. Uses squaring to make the algorithm O(log(e))
  huge ans = 1;
  if (b == 0){
    return 0;
  }
  while (e > 0){
    if ((e % 2) == 1){
      ans = (ans*b) % mod;
    }
    e = e/2;
    b = (b*b) % mod; //look at the square, similarly as in the binary multiplication
  }
  return ans; 
}

huge gcdExtended(huge a, huge b, huge *x, huge *y) //extended Euler's algorithm to find out the multiplicative inverse
{
    // Base Case
    if (a == 0)
    {
        *x = 0;
        *y = 1;
        return b;
    }
    //using pointers for storing values
    huge x1, y1; // To store results of recursive call
    huge g = gcdExtended(b%a, a, &x1, &y1);
  
    // Update x and y using results of recursive
    // call
    *x = y1 - (b/a) * x1;
    *y = x1;
  
    return g;
}

