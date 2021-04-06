void hil_s_to_xy(unsigned s, int n, unsigned *xp, unsigned *yp){
  int i, sa, sb;
  unsigned x, y, t;

  for (i=0; i<2*n; i+=2) {
    sa = (s>>(i+1))&1;
    sb = (s>>i)&1;

    if (sa == sb) {
      t = x;
      x = y;
      y = t;
      if (sa==1) {
        x = ~x;
        y = ~y;
      }
    }
    x = (x>>1) | (sa<<31);
    y = (y>>1) | ((sa^sb)<<31);
  }
  *xp = x>>(32-n);
  *yp = y>>(32-n);
}

#include <stdio.h>

int main() {
  int x, y, s;
  int ORDER = 2;

  for (s=0; s<(1<<(2*ORDER)); s++) {
    hil_s_to_xy(s, ORDER, &x, &y);
    printf("%d %d\n", x, y);
  }

}
