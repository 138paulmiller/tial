g = 0; # global

def first(a, b, c)
	l = a + b + c ; #local sum 
	g = l*l;
	return l;

def second(a)
	g = g / a;
	return g;


def third()
	g = a  + 5;
	return g;

v1 = first(1, 10, 100);
v2 = second(v1);
v3 = third(); 
