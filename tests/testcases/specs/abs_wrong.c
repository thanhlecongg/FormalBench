#include <limits.h>

/*@
  ensures \result == 0;
*/
int abs(int x) {
    if (x < 0) x = -x;
    return x;
}