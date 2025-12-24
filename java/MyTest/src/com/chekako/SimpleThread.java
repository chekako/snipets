package com.chekako;

public class SimpleThread extends Thread
{
	public SimpleThread( String str )
	{
		super( str );
	}

	public void run()
	{
		for ( int i = 0; i < 3; ++i )
		{
			System.out.println( i + " " + getName() );
			try
			{
				sleep( (long) ( Math.random() * 1000 ) );
			} catch ( InterruptedException e )
			{
				System.out.println( "InterruptedException in SimpleThread.run" );
			}
		}
		System.out.println( "DONE! " + getName() );
	}
}
