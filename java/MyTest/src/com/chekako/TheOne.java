package com.chekako;

public class TheOne
{
	private static TheOne ourInstance = new TheOne();

	public static TheOne getInstance()
	{
		return ourInstance;
	}

	private TheOne()
	{
	}

	public String F( String s )
	{
		return s;
	}
}
