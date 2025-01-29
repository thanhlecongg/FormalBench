// failed

import java.io.*;
import java.lang.*;
import java.util.*;
import java.math.*;

class AddDictToTuple {
    
    /*@ requires testTup != null;
      @ requires testDict != null;
      @ requires (\forall Integer i; testTup.contains(i); i != null);
      @ ensures \result.size() == testTup.size() + 1;
      @ ensures (\forall int i; 0 <= i < testTup.size(); \result.get(i) == testTup.get(i));
      @ ensures \result.get(testTup.size()) == testDict;
      @*/
    public static List<Object> addDictToTuple(List<Integer> testTup, HashMap<String, Integer> testDict) {
        List<Object> res = new ArrayList<>();
        /*@ loop_invariant 0 <= res.size() <= testTup.size();
          @ loop_invariant (\forall int i; 0 <= i < res.size(); res.get(i) == testTup.get(i));
          @ decreasing testTup.size() - res.size();
          @*/
        for (Integer i : testTup) {
            res.add(i);
        }
        res.add(testDict);
        return res;
    }
}
