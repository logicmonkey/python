#include <stdio.h>

void hil_s_to_xy(unsigned s, int n, unsigned *xp, unsigned *yp){
  int i, sa, sb;
  unsigned x, y, t;
  x=0;
  y=0;

  for (i=0; i<2*n; i++) {
    sa = (s>>(2*i+1))&1;
    sb = (s>>(2*i))&1;

    if (sa==sb) {
      t = x;
      x = y;
      y = t;
      if (sa==1) {
        x = ~x;
        y = ~y;
      }
    }

    if (sa==1) {
      x |= (1<<i); // OR in a 1
    } else
      x &= ~(1<<i); // AND in a 0

    if ((sa^sb)==1)
      y |= (1<<i); // shift i/2
    else {
      y &= ~(1<<i); // loop step is +2
    }

  }
  *xp = x&((1<<n)-1);
  *yp = y&((1<<n)-1);
}

int main() {
  int x, y, s;
  int ORDER = 2;

  for (s=0; s<(1<<(2*ORDER)); s++) {
    hil_s_to_xy(s, ORDER, &x, &y);
    printf("%d %d\n", x, y);
  }
}
