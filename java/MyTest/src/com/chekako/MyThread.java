package com.chekako;

import java.util.Random;
import java.util.UUID;

public class MyThread extends Thread
{
	long max;
	double sum = 0;

	MyThread( long max )
	{
		this.max = max;
	}

	public void run()
	{
		Random r = new Random( UUID.randomUUID().hashCode() );
		for ( long idx = 0; idx < max; ++idx )
			sum += r.nextDouble();
	}
}
