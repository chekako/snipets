package com.chekako;

import java.io.Console;
import java.text.DateFormat;
import java.text.MessageFormat;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Calendar;
import java.util.Currency;
import java.util.Set;
import java.util.UUID;

public class Main
{
	public static void main( String[] args )
			throws javax.xml.parsers.ParserConfigurationException, org.xml.sax.SAXException, java.io.IOException
	{
		System.out.println( "testing ..." );
		for ( String s : args )
		{
			System.out.println( s );
		}
/*	DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		dbf.setNamespaceAware(true);

		// Step 2: create a DocumentBuilder
		DocumentBuilder db = dbf.newDocumentBuilder();

		// Step 3: parse the input file to get a Document object
		Document doc = db.parse(new File("D:\\MyTest.xml"));
*/
		JdbcExample.main2( null );

		try
		{
			UUID g = UUID.randomUUID();
			String sg = g.toString();

			System.out.println( "args:" );
			for ( int arg = 0; arg < args.length; ++arg )
				System.out.println( MessageFormat.format( "[{0}]=\"{1}\"", arg, args[arg] ) );

			DateFormat dateFormat = new SimpleDateFormat( "yyyy-MM-dd HH:mm:ss.SSS" );

			LocalDateTime ldt = LocalDateTime.now();
			Set< String > zones = ZoneId.getAvailableZoneIds();
			ZonedDateTime zdtUTC = ZonedDateTime.now( ZoneId.of( "UTC" ) );
			ZonedDateTime zdtGMT = ZonedDateTime.now( ZoneId.of( "GMT" ) );
			ZonedDateTime zdtZulu = ZonedDateTime.now( ZoneId.of( "Zulu" ) );
			ZonedDateTime zdt1 = ZonedDateTime.of( 2015, 1, 1, 0, 0, 0, 0, ZoneId.of( "America/Chicago" ) );
			ZonedDateTime zdt2 = ZonedDateTime.of( 2015, 7, 1, 0, 0, 0, 0, ZoneId.of( "America/Chicago" ) );
//			OffsetDateTime odt = zdt1..plusDuration( )

			System.out.println( dateFormat.format( Calendar.getInstance().getTime() ) );

			int threadCount = args.length > 0 ? Integer.parseInt( args[0] ) : 1;
			long max = 1_000_000_000L;
			MyThread[] threadArray = new MyThread[threadCount];
			for ( int threadIdx = 0; threadIdx < threadCount; ++threadIdx )
			{
				MyThread t = new MyThread( max );
				threadArray[threadIdx] = t;
				t.start();
			}

			for ( int threadIdx = 0; threadIdx < threadCount; ++threadIdx )
				threadArray[threadIdx].join();

			System.out.println( dateFormat.format( Calendar.getInstance().getTime() ) );

			double sum = 0;
			for ( int threadIdx = 0; threadIdx < threadCount; ++threadIdx )
				sum += threadArray[threadIdx].sum;
			double average = sum / max / threadCount;

			System.out.println( average );

			TheOne o = TheOne.getInstance();
			String s = o.F( TheOne.getInstance().F( "s" ) );
			System.out.println( s );

			long l0 = 0x0123_4567_89AB_CDEFL;
			long l1 = 0xFEDC_BA98_7654_3210L;
			long l = l0 ^ l1;

			ClsA a;
//			a = new ClsA();
			a = new ClsA( "A" );
			a.foo();
			ClsB b;
//			b = new ClsB();
			b = new ClsB( "B" );
			b.foo();
			ClsA rA;
			rA = a;
			rA.foo();
			rA = b;
			rA.foo();
			ClsB rB;
//			rB = a; // error
//			rB.foo();
			rB = b;
			rB.foo();

			char c = 'a';
			short s16 = 0x0123;
			int i32 = 0x0123_4567;
			long l64 = 0x0123_4567_89AB_CDEFL;
			long l2 = 1;
			long l3 = l64 + l2;
			byte b1 = 1;
			byte b2 = 2;
			byte b3 = (byte) ( b1 + b2 );
			short s1 = 1;
			short s2 = 2;
			short s3 = (short) ( s1 + s2 );

			for ( int idx = 0; idx < 10; ++idx )
			{

			}

//			System.out.println(idx);

			Currency currency = Currency.getInstance( "USD" );
		}
		catch ( MyException e )
		{
			System.out.println( "catch " + e.getMessage() + " " + e.error );
		}
		catch ( Exception e )
		{
			System.out.println( "catch " + e.getMessage() );
		}
		finally
		{
			System.out.println( "finally" );
		}
		ClsBase q = new ClsBase();
		int i = q.F( 51 );
		System.out.println( "result is " + i );
		for ( int iIdx = 0; iIdx < 1000000; ++iIdx )
		{
			double d = ( Math.sqrt( 5 ) + 1 ) / 2;
		}
		System.out.println( "done." );
		System.out.println( "args.length is " + args.length );
		for ( int iArg = 0; iArg < args.length; ++iArg )
			System.out.println( args[iArg] );
		System.out.println( "just testing ..." );
		SimpleThread st1 = new SimpleThread( "thread one" );
		st1.start();
		new SimpleThread( "test thread 2" ).start();
		new SimpleThread( "support thread 3" ).start();
//		new Reminder(15);
	}
}
