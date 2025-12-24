using System;
using System.Runtime.Remoting.Contexts;
using System.Threading.Tasks;
using SCG = System.Collections.Generic;
using SCC = System.Collections.Concurrent;
using System.ComponentModel;
using System.Data.SqlClient;
using System.IO;
using System.Net;
using System.Threading;

namespace MyTestVariance
{
	internal interface IVariant< out TO, in TI >
	{
		TO GetSomething();
		void SetSomething( TI ti );
		TO GetSetSometings( TI ti );
	}

	class C : IVariant< Object, String >
	{
		private String s;
		private Object o;

		public object GetSomething()
		{
			return this.s;
		}

		public void SetSomething( string s )
		{
			this.s = s;
			this.o = s.Length;
		}

		public object GetSetSometings( string s )
		{
			object r = this.s;
			this.s = s;
			this.o = s.Length;
			return r;
		}
	}

	[Synchronization ()]
	internal class Program
	{
		private static readonly Func< Object > f = fS;
		private static readonly Action< String > a = aS;

		[Synchronization]
		private static void Main()
		{
			Thread t = new Thread( fS );
			t.Suspend();
			System.Data.SqlClient.SqlCommand s = new SqlCommand();
			var i = s.BeginExecuteNonQuery();
			i = new WaitHandle();
			s.EndExecuteNonQuery( i );
			var q = new SCG.Queue< int >();
			q.Enqueue( 3 );
			int i = q.Dequeue();
			SCC.BlockingCollection< string >
			SCC.ConcurrentDictionary< int, string > c = new SCC.ConcurrentDictionary< int, string >();
			c.AddOrUpdate();
			Mutex m = new Mutex();
			m.WaitOne();
			BackgroundWorker bw = new BackgroundWorker();
			Task< int > t = new Task< int >( fS );
			IAsyncResult ar;
			lock ( q )
			{
				
			}

			Object o = f();
			String s = String.Empty;
			a( s );
		}

		private static String fS()
		{
			return String.Empty;
		}

		private static void aS( Object o )
		{
		}
	}
}
