#include <limits.h>


// requires x != INT_MIN;
int abs(int x) {
    if (x < 0) x = -x;
    return x;
}