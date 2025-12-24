package com.chekako;

public class MyException extends Exception
{
	public MyException( int error )
	{
//		super();
		this.error = error;
	}

	public MyException( String error )
	{
		super( error );
	}

	int error;
}
