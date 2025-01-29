// failed

import java.io.*;
import java.lang.*;
import java.util.*;
import java.math.*;

class AddDict {

    /*@ requires d1 != null && d2 != null;
      @ requires (\forall String key; d1.containsKey(key); d1.get(key) != null);
      @ requires (\forall String key; d2.containsKey(key); d2.get(key) != null);
      @ ensures (\forall String key; d1.containsKey(key) && d2.containsKey(key);
      @             result.containsKey(key) && result.get(key) == d1.get(key) + d2.get(key));
      @ ensures (\forall String key; d1.containsKey(key) && !d2.containsKey(key);
      @             result.containsKey(key) && result.get(key) == d1.get(key));
      @ ensures (\forall String key; !d1.containsKey(key) && d2.containsKey(key);
      @             result.containsKey(key) && result.get(key) == d2.get(key));
      @ ensures (\forall String key; result.containsKey(key);
      @             d1.containsKey(key) || d2.containsKey(key));
      @*/
    public static HashMap<String, Integer> addDict(HashMap<String, Integer> d1, HashMap<String, Integer> d2) {
        HashMap<String, Integer> result = new HashMap<>();
        
        /*@ loop_invariant (\forall String key; d1.containsKey(key); 
          @                    result.containsKey(key) <==> d2.containsKey(key) && result.get(key) == d1.get(key) + (d2.containsKey(key) ? d2.get(key) : 0));
          @ loop_invariant (\forall String key; d2.containsKey(key) && !d1.containsKey(key); 
          @                    !result.containsKey(key));
          @*/
        for (String key : d1.keySet()) {
            if (d2.containsKey(key)) {
                result.put(key, d1.get(key) + d2.get(key));
            } else {
                result.put(key, d1.get(key));
            }
        }
        
        /*@ loop_invariant (\forall String key; d2.containsKey(key) && !d1.containsKey(key); 
          @                    result.containsKey(key) == (d2.containsKey(key) ? true : false));
          @ loop_invariant (\forall String key; d1.containsKey(key); 
          @                    result.containsKey(key));
          @*/
        for (String key : d2.keySet()) {
            if (!d1.containsKey(key)) {
                result.put(key, d2.get(key));
            }
        }
        return result;
    }
}
