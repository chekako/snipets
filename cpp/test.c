
#include<stdio.h>

struct Q
{
	int i;
};

void p( struct Q /*const*/ * /*const*/ q )
{
	printf("i before %i\n",q->i);
	struct Q q2 = { .i=4 };
	q->i = 3; // because of the first 'const'
	q = &q2; // because of the second 'const'
	printf("i after %i\n",q->i);
}
/*
void r( struct Q &q )
{
	q.i = 3;
}
*/
int main( int argc, char **argv )
{
	printf("argc=%i\n",argc);
	for (int i = 0; i < argc; ++i)
		printf("%s\n",argv[i]);

	struct Q q = { .i=4 };
	printf("before call %i\n",q.i);
	p( &q );
	printf("after call %i\n",q.i);

	return 0;
}
