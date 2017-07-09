; Function Attrs: nounwind uwtable
define i32 @foo(i32 %a, i32 %b){
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %c = alloca i32, align 4
  store i32 %a, i32* %1, align 4
  store i32 %b, i32* %2, align 4
  %3 = load i32, i32* %1, align 4
  %4 = mul nsw i32 %3, 10
  %5 = load i32, i32* %2, align 4
  %6 = mul nsw i32 %5, 10
  %7 = add nsw i32 %4, %6
  store i32 %7, i32* %c, align 4
  %8 = load i32, i32* %c, align 4
  %9 = load i32, i32* %2, align 4
  %10 = add nsw i32 %8, %9
  ret i32 %10
}
