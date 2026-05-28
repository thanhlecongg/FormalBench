use prusti_contracts::*;

#[requires(x != i32::MIN)]
#[ensures(result == 0)]
fn abs(x: i32) -> i32 {
    if x >= 0 {
        x
    } else {
        -x
    }
}
