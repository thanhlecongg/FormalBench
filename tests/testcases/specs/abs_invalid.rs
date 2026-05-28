#[requires(x != i32::MIN)]
fn abs(x: i32) -> i32 {
    if x >= 0 {
        x
    } else {
        -x
    }
}
