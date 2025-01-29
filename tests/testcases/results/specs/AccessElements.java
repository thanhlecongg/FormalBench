// verified

import java.io.*;
import java.lang.*;
import java.util.*;
import java.math.*;

class AccessElements {
    
    /*@ requires nums != null && indices != null;
      @ requires \forall int i; 0 <= i < indices.length; 0 <= indices[i] < nums.length;
      @ ensures \result != null && \result.length == indices.length;
      @ ensures \forall int i; 0 <= i < indices.length; \result[i] == nums[indices[i]];
      @*/
    public static int[] accessElements(int[] nums, int[] indices) {
        int[] result = new int[indices.length];
        
        /*@ loop_invariant 0 <= i <= indices.length;
          @ loop_invariant \forall int j; 0 <= j < i; result[j] == nums[indices[j]];
          @ loop_decreases indices.length - i;
          @*/
        for (int i = 0; i < indices.length; i++) {
            result[i] = nums[indices[i]];
        }
        return result;
    }
}
