g = 0; # global

def first(a, b, c)
	l = a + b + c ; #local sum 
	g = l*l;
	return l;

 def second(a)
 	g =  g / a;
 	return g;

# comments !!
 def third(g)
 	g = g  * 2; # after line comment
 	return g / 2;

v1 = first(5, 10, 15);
v2 = second(v1);
v3 = third(4); 
