; ModuleID = 'main.c'

@.str = private unnamed_addr constant [6 x i8] c"%s%d\0A\00", align 1
@.str.1 = private unnamed_addr constant [6 x i8] c"HELLO\00", align 1

; Function Attrs: nounwind uwtable
define i32 @main(i32 %argc, i8** %argv){
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i8**, align 8
  %a = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 %argc, i32* %2, align 4
  store i8** %argv, i8*** %3, align 8
  %4 = call i32 @foo(i32 10, i32 40)
  store i32 %4, i32* %a, align 4
  %5 = load i32, i32* %a, align 4
  %6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.1, i32 0, i32 0), i32 %5)
  ret i32 0
}

declare i32 @foo(i32, i32) #1

declare i32 @printf(i8*, ...) #1

