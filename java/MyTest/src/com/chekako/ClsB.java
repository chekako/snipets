package com.chekako;

public class ClsB extends ClsA
{
	public ClsB()
	{
//		super();
		System.out.println( "clsB constructor default" );
	}

	public ClsB( String name )
	{
		super( name );
		System.out.println( "clsB constructor '" + name + "'" );
	}

	public void foo() throws Exception
	{
		System.out.println( "B.foo '" + m_name + "'" );
	}
}
