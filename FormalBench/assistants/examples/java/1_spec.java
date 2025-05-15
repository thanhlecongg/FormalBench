public class SumMax {

    //@ requires a != null;
    //@ requires a.length > 0;
    void sumMax(int[] a) {
      int sum = 0;
      int max = a[0];
  
      //@ loop_invariant 0 <= i <= a.length;
      //@ loop_invariant sum <= \\count * max; 
      for (int i=0; i < a.length; i++) {
        //@ assume Integer.MIN_VALUE <= sum + a[i] <= Integer.MAX_VALUE; 
        sum += a[i];
        if (max < a[i]) max = a[i];
      }
  }
  
}