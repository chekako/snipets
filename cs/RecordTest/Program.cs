
Console.WriteLine( "Hello, World!" );



interface I {
	int P { get; init; /*set;*/ }
	int F( int i );
}

class C : I {
	public int P { get; init; }
	public int F( int i ) { return i; }
	public C() {}
	public C( int i ) : this() { P = i; }
}

struct S : I {
	public int P { get; init; }
	public int F( int i ) { return i; }
	public S() {}
	public S( int i ) : this() { P = i; }
}

record class RC : I {
	public int P { get; init; }
	public int F( int i ) { return i; }
	public RC() {}
	public RC( int i ) : this() { P = i; }
}

record struct RS : I {
	public int P { get; init; }
	public int F( int i ) { return i; }
	public RS() {}
	public RS( int i ) : this() { P = i; }
}

readonly record struct NRS : I {
	public int P { get; init; }
	public int F( int i ) { return i; }
	public NRS() {}
	public NRS( int i ) : this() { P = i; }
}


interface I2 : I {
	public int P2 { get; init; }
	public int F2( int i ) { return i; }
}

class C2 : C, I2 {
	public int P2 { get; init; }
	public int F2( int i ) { return i; }
	public C2() {}
	public C2( int i ) : this() { P = i; }
}

struct S2 : /*S,*/ I2 {
	public int P { get; init; }
	public int F( int i ) { return i; }
	public int P2 { get; init; }
	public int F2( int i ) { return i; }
	public S2() {}
	public S2( int i ) : this() { P = i; }
}

record class RC2 : RC, I2 {
	public int P2 { get; init; }
	public int F2( int i ) { return i; }
	public RC2() {}
	public RC2( int i ) : this() { P = i;
	}
}

record struct RS2 : /*RS,*/ I2 {
	public int P { get; init; }
	public int F( int i ) { return i; }
	public int P2 { get; init; }
	public int F2( int i ) { return i; }
	public RS2() {}
	public RS2( int i ) : this() { P = i; }
}

readonly record struct NRS2 : /*RS,*/ I2 {
	public int P { get; init; }
	public int F( int i ) { return i; }
	public int P2 { get; init; }
	public int F2( int i ) { return i; }
	public NRS2() {}
	public NRS2( int i ) : this() { P = i; }
}






/*
class / record / ValueObject:
Reference type; ref and in keywords are not needed.
Heap allocated; more work for GC.
Allows non-public parameterless constructor.
Allows inheritance, polymorphism and interface implementation.
Does not have to be boxed.
Use record as DTOs and immutable/value objects.
Use ValueObject when you need both immutability and, either IComparable or precise control over equality checks.

(readonly / record) struct:
Value type; can be passed as readonly reference with in keyword.
Stack allocated.
Does not allow non-public parameterless constructor.
Does not allow inheritance, polymorphism, but interface implementation.
Might have to be boxed frequently.
*/
