#define M
#define N

namespace PubSubEvent;

public static class Program {
	public static int Main( string[] args ) {
		C c = new ();
#if M
		c.MyDelegate += ( sender, e ) => { Console.WriteLine( $"delegate lambda main {sender} {e}" ); };
		c.MyHandler += ( sender, e ) => { Console.WriteLine( $"handler lambda main {sender} {e}" ); };
		c.MyEvent += ( sender, e ) => { Console.WriteLine( $"event lambda main {sender} {e}" ); };
		c.MyEventWithHandlerField += ( sender, e ) => { Console.WriteLine( $"event with hadler field lambda main {sender} {e}" ); };
#endif
		c.F( "c.F" );
		c.MyHandler.Invoke( "c.MyHandler.Invoke", "c.MyHandler.Invoke" );
		c.MyDelegate.Invoke( "c.MyDelegate.Invoke", "c.MyDelegate.Invoke" );
//		c.MyEvent.Invoke( "c.MyEvent.Invoke", "c.MyEvent.Invoke" ); not allowed; only from inside C.

		return 0;
	}
}


class C {
	public delegate void MySig( object sender, object e ); // signature declaration

	public MySig MyDelegate; // object
	public EventHandler< object > MyHandler; // object
	public event EventHandler< object > MyEvent; // object

	private EventHandler< object >? _handler; // private object backing field for MyEventWithHandlerField
	public event EventHandler< object > MyEventWithHandlerField { // object
		add {
			using var autoLock = new AutoLock( true );
//			if ( _handler is null ) return;
			_handler += value;
		}
		remove {
			using var autoLock = new AutoLock( true );
//			if ( _handler is null ) return;
			_handler -= value;
		}
	}


	public C() {
#if N
		MyDelegate += ( sender, e ) => { Console.WriteLine( $"delegate lambda {sender} {e}" ); };
		MyHandler += ( sender, e ) => { Console.WriteLine( $"handler lambda {sender} {e}" ); };
		MyEvent += ( sender, e ) => { Console.WriteLine( $"event lambda {sender} {e}" ); };
#endif
	}

	public void F( object o ) {
		MyDelegate.Invoke( "Fd", o ); // or ...
		foreach ( Delegate @delegate in MyDelegate.GetInvocationList() )
			@delegate.DynamicInvoke( "Fd'", o );
		
		MyHandler.Invoke( "Fh", o ); // or ...
		foreach ( Delegate @delegate in MyHandler.GetInvocationList() )
			@delegate.DynamicInvoke( "Fh'", o );
		
		MyEvent.Invoke( "Fe", o ); // or ...
		foreach ( Delegate @delegate in MyEvent.GetInvocationList() )
			@delegate.DynamicInvoke( "Fe'", o );

		using var autoLock = new AutoLock(); // read lock the _hadler field so it cannot be un/subsubscribed by other threads
		if ( _handler is null ) return;
		foreach ( Delegate @delegate in _handler.GetInvocationList() ) // _handler cannot be un/subscribed by other threads because of the read lock
			@delegate.DynamicInvoke( "F'", o );
	}
}

class AutoLock : IDisposable {
	private static readonly ReaderWriterLockSlim Lock;
	private readonly bool _write;

	static AutoLock() {
		Lock = new();
	}

	public AutoLock( bool write = false ) {
		_write = write;
		if ( _write ) Lock.EnterWriteLock();
	  else Lock.EnterReadLock();
	}
	public void Dispose() {
		if ( _write ) Lock.ExitWriteLock();
		else Lock.ExitReadLock();
	}
}