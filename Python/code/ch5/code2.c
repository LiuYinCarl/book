#include <stdio.h>
#include <math.h>
#include <inttypes.h>

#define PyLong_SHIFT 30
typedef uint32_t digit;


int main() {
  double dval = 6.917529027641082e+17;
  /* double dval = 10000000000000000000000.0; */
  printf("dval: %lf\n", dval);

  double frac;
  int i, ndig, expo;

  frac = frexp(dval, &expo);
  ndig = (expo-1) / PyLong_SHIFT + 1;
  frac = ldexp(frac, (expo-1) % PyLong_SHIFT + 1);
  for (i = ndig; --i >= 0;) {
    digit bits = (digit)frac;
    printf("%u ", bits);
    frac = frac - (double)bits;
    frac = ldexp(frac, PyLong_SHIFT);
  }
  printf("\n");

  return 0;
}
