// timeout

import java.io.*;
import java.lang.*;
import java.util.*;
import java.math.*;

class AddConsecutiveNums {

    /*@ requires nums != null;
      @ ensures nums.length < 2 ==> \result.length == 0;
      @ ensures nums.length >= 2 ==> \result.length == nums.length - 1;
      @ ensures nums.length >= 2 ==>
      @ (\forall int i; 0 <= i < nums.length - 1; \result[i] == nums[i] + nums[i + 1]);
      @*/
    public static int[] addConsecutiveNums(int[] nums) {
        if (nums.length < 2) {
            return new int[0];
        }
        int[] result = new int[nums.length - 1];
        /*@ loop_invariant 0 <= i <= nums.length - 1;
          @ loop_invariant (\forall int j; 0 <= j < i; result[j] == nums[j] + nums[j + 1]);
          @ loop_decreases nums.length - 1 - i;
          @*/
        for (int i = 0; i < nums.length - 1; i++) {
            result[i] = nums[i] + nums[i + 1];
        }
        return result;
    }
}
