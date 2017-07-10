//Compile and link using clang -c main.c
// then clang main.o <other.o> -o test
#include <stdio.h>
extern float foo(float a); //defined in src.tial
int main(int argc, char** argv)
{
	printf("foo(1)= %f", foo(1));
	return 0;
}