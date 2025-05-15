public class SumMax {

    void sumMax(int[] a) {
      int sum = 0;
      int max = a[0];
  
      for (int i=0; i<a.length; i++) {
        sum += a[i];
        if (max < a[i]) max = a[i];
      }
    }
  
}