package com.chekako;

public class ClsA
{
	String m_name;

	public ClsA()
	{
//		super();
		System.out.println( "clsA constructor default" );
	}

	public ClsA( String name )
	{
		super();
		m_name = name;
		System.out.println( "clsA constructor '" + name + "'" );
	}

	public void foo() throws Exception
	{
		System.out.println( "A.foo '" + m_name + "'" );
//		throw new Exception( "test exception" );
//		throw new MyException( 51 );
//		throw new MyException( "test exception" );
	}
}
