public class BinarySearch {
    
    //@ requires sortedArray != null && 0 < sortedArray.length < Integer.MAX_VALUE;
    //@ requires \forall int i; 0 <= i < sortedArray.length; \forall int j; i < j < sortedArray.length; sortedArray[i] <= sortedArray[j];
    //@ old boolean containsValue = (\exists int i; 0 <= i < sortedArray.length; sortedArray[i] == value);
    //@ ensures containsValue <==> 0 <= \result < sortedArray.length;
    //@ ensures !containsValue <==> \result == -1;
    //@ pure
    public static int search(int[] sortedArray, int value) {
        
        //@ ghost boolean containsValue = (\exists int i; 0 <= i < sortedArray.length; sortedArray[i] == value);
        if (value < sortedArray[0]) return -1;
        if (value > sortedArray[sortedArray.length-1]) return -1;
        int lo = 0;
        int hi = sortedArray.length-1;
        
        //@ loop_invariant 0 <= lo < sortedArray.length && 0 <= hi < sortedArray.length;
        //@ loop_invariant containsValue ==> sortedArray[lo] <= value <= sortedArray[hi];
        //@ loop_invariant \forall int i; 0 <= i < lo; sortedArray[i] < value;
        //@ loop_invariant \forall int i; hi < i < sortedArray.length; value < sortedArray[i];
        //@ loop_decreases hi - lo;
        while (lo <= hi) {
            int mid = lo + (hi-lo)/2;
            if (sortedArray[mid] == value) {
                return mid;
            } else if (sortedArray[mid] < value) {
                lo = mid+1;
            } else {
                hi = mid-1;
            }
        }
        return -1;
    }
}