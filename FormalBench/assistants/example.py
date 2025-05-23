import FormalBench

ABS_PATH = FormalBench.__path__[0] + "/assistants/examples"
class JavaExample:
    with open(f"{ABS_PATH}/java/1.java", "r") as f:
      EXAMPLE_CODE1 = f.read()

    with open(f"{ABS_PATH}/java/1_spec.java", "r") as f:
      EXAMPLE_SPEC1 = f.read()
      EXAMPLE_SPEC1 = "```\n" + EXAMPLE_SPEC1 + "\n```\n"

    with open(f"{ABS_PATH}/java/2.java", "r") as f:
      EXAMPLE_CODE2 = f.read()
    
    with open(f"{ABS_PATH}/java/2_spec.java", "r") as f:
      EXAMPLE_SPEC2 = f.read()
      EXAMPLE_SPEC2 = "```\n" + EXAMPLE_SPEC2 + "\n```\n"


    EXAMPLE_LTM_RESPONSE2 = """
Let's break down the problem step by step and generate the JML specifications for the `Abs` class.

---

### 1. **Weakest Preconditions**
The weakest preconditions for the `Abs` method are:
  - The input `num` must not be `Integer.MIN_VALUE`. This is because the absolute value of `Integer.MIN_VALUE` cannot be represented as a positive integer in Java (due to overflow).

---

### 2. **Strongest Postconditions**
The strongest postconditions for the `Abs` method are:
  - The result is always non-negative.
  - The result is equal to the absolute value of `num`, i.e., `\\result == (num < 0 ? -num : num)`.

---

### 3. **Necessary Specifications**
  - **Assertions**: No assertions are needed in this method since it is straightforward.
  - **Loop Invariants**: Not applicable here since there are no loops.
  - **Assumptions**: No additional assumptions are required beyond the precondition.
  - **Ranking Functions**: Not applicable here since there are no loops or recursion.

---

### SPECIFICATION

""" + EXAMPLE_SPEC2

    with open(f"{ABS_PATH}/java/3.java", "r") as f:
      EXAMPLE_CODE3 = f.read()
      
    with open(f"{ABS_PATH}/java/3_spec.java", "r") as f:
      EXAMPLE_SPEC3 = f.read()
      EXAMPLE_SPEC3 = "```\n" + EXAMPLE_SPEC3 + "\n```\n"

    EXAMPLE_LTM_RESPONSE3 = """
Let's break down the problem step by step and generate the JML specifications for the `BinarySearch` class.

---

### 1. **Weakest Preconditions**
The weakest preconditions for the `search` method are:
  - The input array `sortedArray` must not be `null`.
  - The length of `sortedArray` must be greater than 0 and less than `Integer.MAX_VALUE` to avoid arithmetic overflow.
  - The array must be sorted in non-decreasing order.

---

### 2. **Strongest Postconditions**
The strongest postconditions for the `Abs` method are:
  - If the `value` exists in the array, the method returns the index of the `value` in the array, and the index is within the bounds of the array.
  - If the `value` does not exist in the array, the method returns `-1`.

---

### 3. **Necessary Specifications**
  - **Loop Invariants**:
    - The indices `lo` and `hi` remain within the bounds of the array.
    - If the `value` exists in the array, it must lie between `sortedArray[lo]` and `sortedArray[hi]`.
    - All elements to the left of `lo` are less than `value`.
    - All elements to the right of `hi` are greater than `value`.
  - **Ranking Functions**:
    - The difference `hi - lo` decreases with each iteration, ensuring termination.
  - **Assertions**:
    - After the loop, if the `value` is not found, the method returns `-1`.

---

### SPECIFICATION

  """ + EXAMPLE_SPEC3


class CExample:
    with open(f"{ABS_PATH}/c/1.c", "r") as f:
      EXAMPLE_CODE1 = f.read()

    with open(f"{ABS_PATH}/c/1_spec.c", "r") as f:
      EXAMPLE_SPEC1 = f.read()
      EXAMPLE_SPEC1 = "```\n" + EXAMPLE_SPEC1 + "\n```\n"

    with open(f"{ABS_PATH}/c/2.c", "r") as f:
      EXAMPLE_CODE2 = f.read()

    with open(f"{ABS_PATH}/c/2_spec.c", "r") as f:
      EXAMPLE_SPEC2 = f.read()
      EXAMPLE_SPEC2 = "```\n" + EXAMPLE_SPEC2 + "\n```\n"

    EXAMPLE_LTM_RESPONSE2 = """
Let's break down the problem step by step and generate the ACSL specifications for the `bubbleSort` function.

### 1. **Preconditions** (`requires`):
The weakest preconditions for the `bubbleSort` function are:
- Ensures the array `a` points to a valid memory block of at least `n` elements. Since the function accesses and modifies all elements of `a`, this condition is necessary for memory safety.
- Assumes that the input array is non-empty. This prevents undefined behavior due to iteration over zero-length arrays.

---

### 2. **Postconditions** (`ensures`)
The strongest postconditions for the `bubbleSort` function are:
- Ensures that the array is sorted in non-decreasing order after execution by comparing all pairs of indices to ensure the ordering property.

### 3. **Necessary Specifications**

- **Outer Loop**
  - Ensure that that the loop variable `i` stays within the appropriate range of array indices.
  - Ensure the segment from index `i` to `n - 1` is sorted in non-decreasing order. This invariant becomes stronger as the algorithm progresses.
  - Ensures transitional order: the maximum value in the unsorted prefix does not exceed the minimum value in the sorted suffix.
  - Declares which variables and memory regions may be modified by the loop body.
  - Specifies a decreasing variant ensures that the loop will eventually terminate.

- **Inner Loop**
  - Ensures the loop variable `j` stays within bounds during iteration over the unsorted section.
  - Reiterates that ordering between the unsorted and sorted segments is preserved, even as elements are being swapped.
  - Specifies modifications to variables and memory within the active segment.
  - Specifies a decreasing variant ensures that the loop will eventually terminate.

---

### SPECIFICATION

  """ + EXAMPLE_SPEC2

    with open(f"{ABS_PATH}/c/3.c", "r") as f:
      EXAMPLE_CODE3 = f.read()

    with open(f"{ABS_PATH}/c/3_spec.c", "r") as f:
      EXAMPLE_SPEC3 = f.read()
      EXAMPLE_SPEC3 = "```\n" + EXAMPLE_SPEC3 + "\n```\n"

    EXAMPLE_LTM_RESPONSE3 = """
Let's break down the problem step by step and generate the ACSL specifications for the `checkArrayEquality` function.

---

### 1. **Preconditions** (`requires`):

The weakest preconditions for the `checkArrayEquality` function are:
- Guarantees that the function is not invoked on an empty array, thereby avoiding iteration over an invalid range.
- Ensures that all elements of the input array `a` within the index range `[0, n-1]` are readable.
- Ensures that all elements of the array `b` within the same index range are also readable.
- Ensure that this function does not modify any memory location, which reflects its observational (pure) nature.

---

### 2. **Postconditions** (`ensures`):

The strongest postconditions for the `checkArrayEquality` function are partitioned into *behaviors*, depending on the equality of the input arrays:

- **Behavior `equal`**: If all elements of `a` and `b` are pairwise equal across the entire index range so that the function returns `1` to signify equality.
- **Behavior `not_equal`**: If there exists at least one index where the corresponding elements differ, so that the function returns `0` to signify inequality.

These behaviors are mutually exclusive and collectively exhaustive, meaning they cover all possible input scenarios without overlap.

---

### 3. **Necessary Specifications**

- **Loop Annotations**: The function employs a `for` loop to iterate over the elements of the arrays. The associated loop specifications are as follows:
  - Ensures the loop index `i` always remains within valid bounds throughout execution.
  - Specifies that the only variable modified during each iteration is the loop index `i`.

---

### SPECIFICATION

  """ + EXAMPLE_SPEC3

_UNSUPPORTED_SUMNUMPRODUCT_QUANTIFIER_DESC = """
OpenJML does not fully support JML's inductive quantifiers like \\num_of, \\sum, and \\product in specifications. These operators require inductive reasoning (e.g., counting elements, summing values over a range, or computing products), which is difficult for SMT solvers (the engines behind OpenJML and most of deductive verification tools) to handle.
"""

_UNSUPPORTED_SUMNUMPRODUCT_QUANTIFIER_GUIDANCE =""" 
To avoid the use of \\sum, \\num_of, and \\product quantifiers in your JML specifications, you can express your specifications using induction steps to help OpenJML's verifiers to reason about your code. You can do this by define mathematical functions and lemmas through model methods. 
For example, you can should not use \\product quantifier in the following specifications:

```
//@ requires 0 <= n && n <= 20;
//@ ensures \\result >= 1 && \\result <= Long.MAX_VALUE;
//@ ensures \\result == (\\product int i; 1 <= i && i <= n; i);
public /*@ pure @*/ long factorial(int n)
{
  int c;
  long fact = 1;

if (n == 0) {         
  return fact;
  }

  //@ maintaining c >= 1 && c <= n+1;
  //@ maintaining fact > 0;
  //@ maintaining fact <= Long.MAX_VALUE; 
  //@ maintaining fact == (\\product int i; 1 <= i && i <= c; i);
  //@ decreases n - c;
      for (c = 1; c <= n; c++) { 
            fact = fact*c;
          }	 

      return fact;
  }
```
Instead, you can define a model method `spec_factorial` to help OpenJML's verifiers to reason about your code. Here is an example of how you can define a model method to replace the \product quantifier in the factorial method:

```   
//@ requires 0 <= n && n <= 20;
//@ ensures \\result >= 1 && \\result <= Long.MAX_VALUE;
//@ ensures \\result == spec_factorial(n);
  public /*@ pure @*/ long factorial(int n)
  {
    int c;
    long fact = 1;

//@ assert spec_factorial(0) == 1;
if (n == 0) {         
          return fact;
}

//@ maintaining c >= 1 && c <= n+1;
//@ maintaining fact > 0;
//@ maintaining fact <= Long.MAX_VALUE; 
//@ maintaining spec_factorial(c - 1) == fact;
//@ decreases n - c;
    for (c = 1; c <= n; c++) { 
          fact = fact*c;
        }	 

    return fact;
}

/*@ 	
requires n > 0 && n <= 20;
  ensures 0 <= \\result && \\result <= Long.MAX_VALUE;
  ensures n > 0 ==> \\result == n * spec_factorial(n-1);
also
  requires n == 0;
  ensures \\result == 1;
public model static pure long spec_factorial(int n) { 
if (n == 0) {
  return 1; 
}
else {
  assert n * spec_factorial(n-1) <= Long.MAX_VALUE;
  return n * spec_factorial(n-1);
}
    }
@*/
}
```
"""

_UNSUPPORTED_MINMAX_QUANTIFIER_DESC = """
OpenJML does not fully support JML's inductive quantifiers like \\min, \\max in specifications. These operators require inductive reasonings, which is difficult for SMT solvers (the engines behind OpenJML and most of deductive verification tools) to handle.
"""

_UNSUPPORTED_MINMAX_QUANTIFIER_GUIDANCE ="""
To avoid the use of \\min and \\max quantifiers in your JML specifications, you can use the \\forall quantifier to express your specifications. 
For example, you should not use \\max quantifier in the following specifications:

```
/*@
  @ public normal_behavior
  @ requires a != null;
  @ ensures \\result >= (\\max int j; j >= 0 && j < a.length; a[j]);
  @*/
public static /*@ pure @*/ int max(int[] a) {
    if (a.length == 0) return 0;
    int max = a[0], i = 1;
    /*@
      @ loop_invariant i >= 1 && i <= a.length;
      @ loop_invariant max >= (\\max int j; j >= 0 && j < i; a[j]);
      @ decreases a.length - i;
      @*/
    while (i < a.length) {
        if (a[i] > max) max = a[i];
        ++i;
    }
    return max;
}
```
Instead, you can use the \\forall quantifier to express the same specification without using \\max quantifier:

```
/*@
  @ public normal_behavior
  @ requires a != null;
  @ ensures (\\forall int j; j >= 0 && j < a.length; \\result >= a[j]);
  @*/
public static /*@ pure @*/ int max(int[] a) {
  if (a.length == 0) return 0;
  int max = a[0], i = 1;
  /*@
  @ loop_invariant i >= 1 && i <= a.length;
  @ loop_invariant (\\forall int j; j >= 0 && j < i; max >= a[j]);
  @ decreases a.length - i;
  @*/
  while (i < a.length) {
    if (a[i] > max) max = a[i];
    ++i;
  }
  return max;
}
"""
  
_LOOP_INVARIANT_DESC = """
This error occurs when the loop invariant—a condition that must hold true before the loop begins and remain true after each iteration—is not properly established or maintained. This semantic error typically arises when verifiers fail to confirm the correctness of the synthesized loop invariant. The causes of this error include: (1) an incorrect loop invariant, (2) wrong/weak preconditions that prevent the invariant from holding at the start of the loop, or (3) incomplete reasoning about the loop, leading to insufficient information for the verifier to verify the invariant.
"""
  
_LOOP_INVARIANT_GUIDANCE = """
To resolve the error, please consider the following steps:
1. Carefully review the loop invariant to ensure it correctly captures the necessary conditions that hold true before and after each iteration of the loop.
2. Carefully examine preconditions to ensure they are strong enough to establish the loop invariant at the beginning of the loop.
3. Add additional assertions or assumptions within the loop to help the verifier reason about the loop invariant.

For example, consider the following code snippet with a loop invariant failure:
```
/*@ public normal_behaviour
  @   requires a != null && b != null;
  @   requires a != b;
  @   requires a.length == b.length;
  @   requires (\\forall int x; 0 <= x && x < a.length; 0 <= a[x] && a[x] < a.length);
  @   assignable b[*];
  @
  @   ensures (\\forall int x; 0 <= x && x < b.length; b[a[x]] == x);
  @*/
public static void invert(int[] a, int[] b) {
    
    /*@ loop_invariant 0 <= i && i <= a.length && (\\forall int x; 0 <= x && x < i; b[a[x]] == x);
      @  decreases a.length - i;
      @*/
    for(int i = 0; i < a.length; i++) {
        b[a[i]] = i;
    }
}
```

In this example, the loop invariant is correctly defined to ensure that the mapping between arrays a and b is established correctly. However, it lacks a precondition to guarantee that the elements of array a are unique, which is essential for the invariant to hold. To fix this issue, you can add a precondition to ensure the uniqueness of elements in array a as follows:

```
/*@ public normal_behaviour
  @   requires a != null && b != null;
  @   requires a != b;
  @   requires a.length == b.length;
  @   requires (\\forall int x; 0 <= x && x < a.length; 0 <= a[x] && a[x] < a.length);
  @   requires (\\forall int x, y; 0 <= x && x < y && y < a.length; a[x] != a[y]); // New precondition for uniqueness
  @   assignable b[*];
  @
  @   ensures (\\forall int x; 0 <= x && x < b.length; b[a[x]] == x);
  @*/
public static void invert(int[] a, int[] b) {
    
    /*@ loop_invariant 0 <= i && i <= a.length && (\\forall int x; 0 <= x && x < i; b[a[x]] == x);
      @  decreases a.length - i;
      @*/
    for(int i = 0; i < a.length; i++) {
        b[a[i]] = i;
    }
}
```
"""

_POSTCONDITION_DESC = """
This error occurs when the postcondition—a condition that must hold true after the execution of a program or function—is not satisfied. This type of semantic error typically arises when verifiers are unable to confirm that the program’s logic guarantees the postcondition under all valid inputs and scenarios. The causes of this error include: (1) an incorrect or incomplete postcondition, (2) wrong/weak preconditions that prevent the program from reaching a state where the postcondition holds, or (3) incomplete reasoning about the programs, leading to insufficient information for the verifier to verify the postcondition.
"""

_POSTCONDITION_GUIDANCE = """
To resolve the error, please consider the following steps:
1. Review the postcondition to ensure it correctly captures the expected behavior of the program or function.
2. Check the preconditions to ensure they are strong enough to reach a state where the postcondition holds.
3. Add additional assertions or assumptions within the program or function to help the verifier reason about the postcondition.

For example, consider the following code snippet with a postcondition failure:
```
/*@ public normal_behaviour
  @   requires a != null && b != null;
  @   requires a != b;
  @   requires a.length == b.length;
  @   requires (\\forall int x; 0 <= x && x < a.length; 0 <= a[x] && a[x] < a.length);
  @   requires (\\forall int x, y; 0 <= x && x < y && y < a.length; a[x] != a[y]); // New precondition for uniqueness
  @   assignable b[*];
  @
  @   ensures (\\forall int x; 0 <= x && x < b.length; b[a[x]] == x);
  @*/
public static void invert(int[] a, int[] b) {
    
    //@ decreases a.length - i;
    for(int i = 0; i < a.length; i++) {
        b[a[i]] = i;
    }
}
```

In this example, the postcondition specifies that the array b should be the inverse of array a. However, verifiers failed to confirm this postcondition due to the lack of a proper loop invariant for reasoning about behaviors of loop. To fix this issue, you can add a loop invariant to ensure that the mapping between arrays a and b is correctly established as follows:

```
/*@ public normal_behaviour
  @   requires a != null && b != null;
  @   requires a != b;
  @   requires a.length == b.length;
  @   requires (\\forall int x; 0 <= x && x < a.length; 0 <= a[x] && a[x] < a.length);
  @   requires (\\forall int x, y; 0 <= x && x < y && y < a.length; a[x] != a[y]); // New precondition for uniqueness
  @   assignable b[*];
  @
  @   ensures (\\forall int x; 0 <= x && x < b.length; b[a[x]] == x);
  @*/
public static void invert(int[] a, int[] b) {
    
    /*@ loop_invariant 0 <= i && i <= a.length && (\\forall int x; 0 <= x && x < i; b[a[x]] == x);
      @  decreases a.length - i; 
      @*/
    for(int i = 0; i < a.length; i++) {
        b[a[i]] = i;
    }
}
```
"""

_ARITHMETIC_DESC = """
This error occurs when arithmetic overflows cause computations to exceed the allowable range of values. 
"""

_ARITHMETIC_GUIDANCE = """
To resolve the error, you should consider the following steps:
1. Review the arithmetic operations in your code to identify potential overflow scenarios.
2. Use appropriate data types that can accommodate the expected range of values.
3. Add explicit preconditions or assumptions to ensure that the inputs to arithmetic operations are within the valid range.

For example, consider the following code snippet with an arithmetic operation range error:

```
//@ ensures \\result == a + b;
public static int add(int a, int b) {
    return a + b;
}
```

In this example, the postcondition specifies that the result of the `add` method should be equal to the sum of `a` and `b`. However, if the sum of `a` and `b` exceeds the range of `int`, an arithmetic overflow will occur, leading to incorrect results. To fix this issue, you can add explicit preconditions to ensure that the inputs to the `add` method are within the valid range as follows:

```
//@ requires Integer.MIN_VALUE <= a + b && a + b <= Integer.MAX_VALUE; // Precondition to avoid arithmetic overflow
//@ ensures \\result == a + b;
public static int add(int a, int b) {
    return a + b;
}
```
"""

_NULL_POINTER_DESC = """
This error occurs when a null pointer is dereferenced, leading to undefined behavior or runtime failures. These issues typically arise due to the absence of preconditions ensuring the non-nullness of objects, such as arrays.
"""

_NULL_POINTER_GUIDANCE = """
To resolve the error, you should consider the following steps:
1. Review the code to identify potential dereference of null pointers.
2. Add explicit preconditions to ensure that objects are not null before dereferencing them.

For example, consider the following code snippet with a null dereference error:

```
//@ ensures \\result == a.length;
public static int getLength(int[] a) {
    return a.length;
}
```

In this example, the postcondition specifies that the result of the `getLength` method should be equal to the length of the input array `a`. However, if `a` is null, dereferencing it to access its length will result in a null pointer dereference error. To fix this issue, you can add an explicit precondition to ensure that `a` is not null before accessing its length as follows:

```
//@ requires a != null; // Precondition to ensure a is not null
//@ ensures \\result == a.length;
public static int getLength(int[] a) {
    return a.length;
}
```
"""

_DIVISION_BY_ZERO_DESC = """
This error occurs when a division operation attempts to divide by zero, leading to undefined behavior. These issues typically arise due to missing or incomplete specifications on the values of variables. The root causes can vary and include insufficient preconditions, missing loop invariants, or the absence of assertions to enforce non-zero denominators.
"""

_DIVISION_BY_ZERO_GUIDANCE = """
To resolve the error, you should consider the following steps:
1. Review the code to identify potential division operations that could result in division by zero.
2. Add explicit preconditions or assertions to ensure that denominators are non-zero before performing division operations.

For example, consider the following code snippet with a division by zero error:

```
//@ ensures \\result == a / b;
public static int divide(int a, int b) {
    return a / b;
}
```

In this example, the postcondition specifies that the result of the `divide` method should be equal to the division of `a` by `b`. However, if `b` is zero, a division by zero error will occur, leading to undefined behavior. To fix this issue, you can add an explicit precondition to ensure that `b` is non-zero before performing the division operation as follows:

```
//@ requires b != 0; // Precondition to avoid division by zero
//@ ensures \\result == a / b;
public static int divide(int a, int b) {
    return a / b;
}
```
"""

_ARRAY_INDEX_INDEX_DESC = """
This error occurs when an array index exceeds its valid bounds, leading to potential runtime failures. These issues typically arise due to missing conditions or specifications regarding the array's length or the bounds of the index.
"""

_ARRAY_INDEX_GUIDANCE = """
To resolve the error, you should consider the following steps:
1. Review the code to identify potential array index operations that could exceed the valid bounds.
2. Add explicit preconditions or assertions to ensure that array indices are within the valid range.

For example, consider the following code snippet with a too large index error:

```
//@ ensures \\result == a[index];
public static int getElement(int[] a, int index) {
    return a[index];
}
```

In this example, the postcondition specifies that the result of the `getElement` method should be equal to the element at the given index in the input array `a`. However, if the `index` exceeds the bounds of the array `a`, an array index out of bounds error will occur. To fix this issue, you can add an explicit precondition to ensure that the `index` is within the valid range before accessing the array element as follows:

```
//@ requires a != null; // Precondition to ensure a is not null
//@ requires 0 <= index && index < a.length; // Precondition to ensure index is within bounds
//@ ensures \\result == a[index];
public static int getElement(int[] a, int index) {
    return a[index];
}
```
"""

_LOOP_DECREASES_DESC = """
This error occurs when the ranking function in a loop does not properly ensure a decrease in non-negative values, potentially leading to an infinite loop or incorrect behavior. This issue typically arises from using an incorrect or improperly defined ranking function for the loop.
"""

_LOOP_DECREASES_GUIDANCE = """
To resolve the error, you should revise the loop decreases clause to ensure that the specified ranking function decreases with each iteration of the loop. The ranking function should be a non-negative integer expression that decreases towards the loop exit condition.
"""

_BAD_ARRAY_ASSIGNMENT_DESC = """
This error occurs when there is a mismatch in the expected type of array elements, leading to incorrect assignments. These issues typically arise from insufficient reasoning about the data types of array elements. To resolve this, preconditions should be added to ensure the correct data types are used for each element in the array.
"""

_BAD_ARRAY_ASSIGNMENT_GUIDANCE = """
To resolve the error, you should consider the following steps:
1. Review the code to identify potential array assignments with mismatched types.
2. Add explicit preconditions or assertions to ensure that the assigned values match the expected data types.

For example, consider the following code snippet with a bad array assignment error:

```
class MyObjectArray {
    class Address {
        public int address;
        
        //@ ensures this.address == address;
        //@ pure
        public Address(int address) {
                this.address = address;
        }
    }
    
    //@ requires addresses != null;
    //@ requires addresses.length == 100;
    //@ ensures (\\forall int i; i >= 0 && i < 100; addresses[i] != null);
    public MyObjectArray(Address[] addresses) {
        //@ maintaining i >= 0 && i <= 100;
        //@ decreasing 100 - i;
        //@ maintaining (\\forall int j; j >=0 && j < i; addresses[j] != null);
        for (int i = 0; i < 100; ++i) {
            addresses[i] = new Address(88);
        }

        //@ maintaining i >= 0 && i <= 100;
        //@ decreasing 100 - i;
        //@ maintaining (\\forall int j; j >=0 && j < i; addresses[j].address == 99);
        for (int i = 0; i < 100; ++i) {
            addresses[i].address = 99;
        }
    }
}
```

In this example, each element of the addresses array is assigned an instance of the Address class. As a result, OpenJML must verify that the dynamic type of the right-hand side is a subclass of the element type of the dynamic type on the left-hand side. To address this issue, you can include a precondition to ensure that the Address class is a subclass of the element type of the addresses array, as shown below:

```
class MyObjectArray {
    class Address {
        public int address;
        
        //@ ensures this.address == address;
        //@ pure
        public Address(int address) {
                this.address = address;
        }
    }
    
    //@ requires addresses != null;
    //@ requires addresses.length == 100;
    //@ requires \\type(Address) <: \\elemtype(\\typeof(addresses)); // Precondition to ensure Address is a subclass of the element type
    //@ ensures (\\forall int i; i >= 0 && i < 100; addresses[i] != null);
    public MyObjectArray(Address[] addresses) {
        //@ maintaining i >= 0 && i <= 100;
        //@ decreasing 100 - i;
        //@ maintaining (\\forall int j; j >=0 && j < i; addresses[j] != null);
        for (int i = 0; i < 100; ++i) {
            addresses[i] = new Address(88);
        }

        //@ maintaining i >= 0 && i <= 100;
        //@ decreasing 100 - i;
        //@ maintaining (\\forall int j; j >=0 && j < i; addresses[j].address == 99);
        for (int i = 0; i < 100; ++i) {
            addresses[i].address = 99;
        }
    }
}
```
"""

_ASSERTION_FAILURE_DESC = """
This error occurs when an assertion—a condition that must hold true at a specific point in the program—evaluates to false during execution. This type of error typically arises due to (1) incorrect assertions, (2) incomplete reasoning about program behavior, leading to insufficient information for the verifier to verify the assertions, or (3) insufficient preconditions that fail to guarantee the assertion. To resolve this issue, ensure that the assertion is correctly formulated and that all necessary conditions are met before reaching the assertion.
"""

_ASSERTION_FAILURE_GUIDANCE = """
To resolve the error, you should consider the following steps:
1. Review the assertion to ensure it correctly captures the expected behavior of the program at that point.
2. Check the preconditions to ensure they are strong enough to reach the assertion point.
3. Add additional assertions or assumptions within the program to help the verifier reason about the assertion.

For example, consider the following code snippet with an assertion failure:

```
public static int calculate(int n) {
    if (n == 1 || n == 2) {
        return 1;
    } else {
        //@ assert n > 2;
        return n * 5;
    }
}
```

In this example, the assertion specifies that `n` should be greater than 2. However, this assertions only hold if the input `n` is positive. To fix this issue, you can add a precondition to ensure that `n` is positive before reaching the assertion as follows:

```
//@ requires n > 0; // Precondition to ensure n is positive
public static int calculate(int n) {
    if (n == 1 || n == 2) {
        return 1;
    } else {
        //@ assert n > 2;
        return n * 5;
    }
}
```
"""

_SYNTAX_ERROR_GUIDANCE = """
To resolve the syntax error, you should consider the following steps:
1. Identify whether the error is due to a Java syntax issue or a JML syntax issue.
2. Review the code to identify the specific location and nature of the syntax error.
3. Correct the syntax error based on the language rules and conventions.
"""

_LARGE_SHIFT_DESC = """
In Java shift expressions (a << b, a >> b, a >>> b), only the lower 5 bits (for 32-bit operations) of the shift value (b) are used. That is, a << 32 is equivalent to no shift, not to a shift of all the bits of a 32-bit value. Though values of b larger than 31 are not illegal, they can be confusing. OpenJML warns if the value of the right-hand-side is greater or equal to the number of bits in the promoted type of the left-hand-side.	
"""

_LARGE_SHIFT_GUIDANCE = """
To avoid large shift values, you should consider the following steps:
1. Review the code to identify potential shift expressions with large shift values.
2. Ensure that the shift values are within the valid range of 0 to 31 for 32-bit operations.
3. Use explicit preconditions, assertions or loop invariants to enforce the valid range of shift values.

For example, consider the following code snippet with a large shift value warning:

```
public static int calculate(int n) {
    int count = 0;
    for (int i = 0; i < 32; i++) {
        if (((n >> i) & 1) == 1) {
            count++;
        }
    }
    return count;
}
```

In this example, the code iterates over the bits of the input `n` using a shift operation. However, if the shift value `i` exceeds the valid range of 0 to 31, the behavior of the shift operation may not be as expected. To fix this issue, you can add an explicit loop invariant to help verify to reason that the shift values are within the valid range as follows:


```
public static int calculate(int n) {
    int count = 0;
    //@ loop_invariant 0 <= i && i < 32;
    for (int i = 0; i < 32; i++) {
        if (((n >> i) & 1) == 1) {
            count++;
        }
    }
    return count;
}
```
"""


_PRECONDITION_DESC = """
This error occurs when the precondition—a condition that must hold true before the execution of a program or function—is not satisfied. This type of semantic error typically arises when verifiers are unable to confirm that the program's logic guarantees the precondition under all valid inputs and scenarios. The causes of this error include: (1) an incorrect or incomplete precondition, (2) incomplete reasoning about the programs, leading to insufficient information for the verifier to verify the precondition, especially in recursive or mutually recursive methods.
"""

_PRECONDITION_GUIDANCE = """
To resolve the error, you should consider the following steps:
1. Review the precondition to ensure it correctly captures the necessary conditions that must hold true before the program or function executes.
2. Check the program's logic to ensure it guarantees the precondition under all valid inputs and scenarios.
3. Add additional assertions or assumptions within the program or function to help the verifier reason about the precondition.

For example, consider the following code snippet with a precondition failure:

```
class Gcd {
    /*@ requires x > 0 || y > 0; 
      @*/
    public static int gcd(int x, int y) {
        if (y == 0) {
            return x;
        } else {
            return gcd(y, x % y);
        }
    }
}
```

In this example, the precondition specifies that either `x` or `y` should be greater than 0. However, the recursive call to the `gcd` method does not guarantee that the precondition holds for all valid inputs. To fix this issue, you need (1) add a precondition to ensure that both `x` and `y` are non-negative, and (2) add a assertion to ensure the recursive call satisfies the precondition as follows:

```
class Gcd {
    
    /*@ requires x >= 0 && y >= 0;
      @ requires x > 0 || y > 0; 
      @*/
    public static int gcd(int x, int y) {
        if (y == 0) {
            return x;
        } else {
            //@ assert y > 0;
            return gcd(y, x % y);
        }
    }
}
```
"""

_BAD_CAST_DESC = """
This error occurs when an invalid cast operation is performed, leading to runtime failures or incorrect behavior. These issues typically arise from incorrect assumptions about the types of objects or variables being cast. 
"""

_BAD_CAST_GUIDANCE = """
To resolve the error, you should consider the following steps:
1. Review the code to identify potential cast operations that could result in invalid type conversions.
2. Ensure that the types being cast are compatible and that the cast operation is valid.
3. Add explicit preconditions or assertions to ensure that the cast operation is safe and correct.
"""


_GUIDANCE = {
  "UnsupportedSumNumOfProductQuantifierExpression": {
    "description": _UNSUPPORTED_SUMNUMPRODUCT_QUANTIFIER_DESC,
    "guidance": _UNSUPPORTED_SUMNUMPRODUCT_QUANTIFIER_GUIDANCE
  },
  "UnsupportedMinMaxQuantifierExpression": {
    "description": _UNSUPPORTED_MINMAX_QUANTIFIER_DESC,
    "guidance": _UNSUPPORTED_MINMAX_QUANTIFIER_GUIDANCE
  },
  "LoopInvariantFailure": {
    "description": _LOOP_INVARIANT_DESC,
    "guidance": _LOOP_INVARIANT_GUIDANCE
  },
  "PostconditionFailure": {
    "description": _POSTCONDITION_DESC,
    "guidance": _POSTCONDITION_GUIDANCE
  },
  "ArithmeticOperationRange": {
    "description": _ARITHMETIC_DESC,
    "guidance": _ARITHMETIC_GUIDANCE
  },
  "AssertFailure": {
    "description": _ASSERTION_FAILURE_DESC,
    "guidance": _ASSERTION_FAILURE_GUIDANCE
  },
  "NullDeReference": {
    "description": _NULL_POINTER_DESC,
    "guidance": _NULL_POINTER_GUIDANCE
  },
  "DivideByZero": {
    "description": _DIVISION_BY_ZERO_DESC,
    "guidance": _DIVISION_BY_ZERO_GUIDANCE
  },
  "ArrayIndex": {
    "description": _ARRAY_INDEX_INDEX_DESC,
    "guidance": _ARRAY_INDEX_GUIDANCE
  },
  "BadArrayAssignment": {
    "description": _BAD_ARRAY_ASSIGNMENT_DESC,
    "guidance": _BAD_ARRAY_ASSIGNMENT_GUIDANCE
  },
  "RankingFunctionFailure": {
    "description": _LOOP_DECREASES_DESC,
    "guidance": _LOOP_DECREASES_GUIDANCE
  },
  "SyntaxError": {
    "description": "",
    "guidance": _SYNTAX_ERROR_GUIDANCE
  },
  "LargeShift": {
    "description": _LARGE_SHIFT_DESC,
    "guidance": _LARGE_SHIFT_GUIDANCE
  },
  "PreconditionFailure": {
    "description": _PRECONDITION_DESC,
    "guidance": _PRECONDITION_GUIDANCE
  },
  "BadCast": {
    "description": _BAD_CAST_DESC,
    "guidance": _BAD_CAST_GUIDANCE
  }
}