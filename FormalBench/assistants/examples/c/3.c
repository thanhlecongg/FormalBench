void func(int *a, int n) {

    for (int i = 0; i < n; i++) {
        if (i % 2 == 0) {
            a[i] = 0;
        }
    }
}