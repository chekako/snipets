package com.chekako;

public class ClsBase implements IDoIt2, IDoIt3
{
	@Override
	public int F( int i )
	{
		return i + 1;
	}

	@Override
	public String S( double d )
	{
		return null;
	}

	@Override
	public boolean Is( String s )
	{
		return false;
	}
}
