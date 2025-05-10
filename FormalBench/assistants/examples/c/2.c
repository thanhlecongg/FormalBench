#include <stdio.h>

void bubbleSort(int *a, int n) {
    int i, j, temp;

    for (i = n - 1; i > 0; i--) {

        for (j = 0; j < i; j++) {
            if (a[j] > a[j+1]) {
                temp = a[j];
                a[j] = a[j+1];
                a[j+1] = temp;
            }
        }
    }
}