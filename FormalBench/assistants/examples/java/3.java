public class BinarySearch {

    public static int search(int[] sortedArray, int value) {
        
        if (value < sortedArray[0]) return -1;
        if (value > sortedArray[sortedArray.length-1]) return -1;
        int lo = 0;
        int hi = sortedArray.length-1;
        
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