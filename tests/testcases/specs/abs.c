#include <limits.h>

/*@
  requires x != INT_MIN;
  ensures \result == (x < 0 ? -x : x);
*/
int abs(int x) {
    if (x < 0) x = -x;
    return x;
}