namespace MyTestAsync; 

class Base {public string Name { get; set; } }
class Coffee : Base { }
class Egg : Base { }
class Bacon : Base { }
class Toast : Base { }
class Juice : Base { }

static class Program {
	static async Task Main( string[] args ) {
		// this thread is not needed for the program, just to test fore- vs back-ground.
		// explicitly created threads are foreground by default, thread-pool threads are background.
		// the process stays until all foreground threads finish, then remaining background threads are killed.
		new Thread( () => { 
			Thread.CurrentThread.IsBackground = true;
			Console.WriteLine( $"is back {Thread.CurrentThread.IsBackground}" );
		} ).Start();

		Console.WriteLine( $"Main t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground}" );
		Coffee cup = PourCoffee();
		Console.WriteLine( "coffee is ready" );

		Task< Egg > eggsTask = FryEggsAsync( 2 );
		Task< Bacon > baconTask = FryBaconAsync( 3 );
		Task< Toast > toastTask = MakeToastWithButterAndJamAsync( 2 );
		Console.WriteLine( "tasks created" );

		var breakfastTasks = new List< Task > { eggsTask, baconTask, toastTask };
		while ( breakfastTasks.Count > 0 ) {
			Task finishedTask = await Task.WhenAny( breakfastTasks );

			if ( finishedTask == eggsTask )
				Console.WriteLine( "eggs are ready" );
			else if ( finishedTask == baconTask )
				Console.WriteLine( "bacon is ready" );
			else if ( finishedTask == toastTask )
				Console.WriteLine( "toast is ready" );

			breakfastTasks.Remove( finishedTask );
		}

		Juice oj = PourOJ();
		Console.WriteLine( "oj is ready" );
		Console.WriteLine( "Breakfast is ready!" );
	}

	static async Task< Toast > MakeToastWithButterAndJamAsync( int number ) {
		Console.WriteLine( $"MTWBJ 0 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Toast toast = await ToastBreadAsync( number );
		Console.WriteLine( $"MTWBJ 1 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		ApplyButter( toast );
		ApplyJam( toast );

		return toast;
	}

	private static Juice PourOJ() {
		Console.WriteLine( $"OJ t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( "Pouring orange juice" );
		return new Juice() {Name = "Orange Juice"};
	}

	private static void ApplyJam( Toast toast ) {
		Console.WriteLine( $"Jam t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( "Putting jam on the toast" );
	}

	private static void ApplyButter( Toast toast ) {
		Console.WriteLine( $"Butter t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( "Putting butter on the toast" );
	}

	private static async Task< Toast > ToastBreadAsync( int slices ) {
		Console.WriteLine( $"Toast 0 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		for ( int slice = 0; slice < slices; slice++ )
			Console.WriteLine( "Putting a slice of bread in the toaster" );

		Console.WriteLine( "Start toasting..." );
		await Task.Delay( 3000 );
		Console.WriteLine( $"Toast 1 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( "Remove toast from toaster" );

		return new Toast() {Name = "Toast"};
	}

	private static async Task< Bacon > FryBaconAsync( int slices ) {
		Console.WriteLine( $"Bacon 0 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( $"putting {slices} slices of bacon in the pan" );
		Console.WriteLine( "cooking first side of bacon..." );
		await Task.Delay( 3000 );
		Console.WriteLine( $"Bacon 1 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		for ( int slice = 0; slice < slices; slice++ ) {
			Console.WriteLine( "flipping a slice of bacon" );
		}

		Console.WriteLine( "cooking the second side of bacon..." );
		await Task.Delay( 3000 );
		Console.WriteLine( $"Bacon 2 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( "Put bacon on plate" );

		return new Bacon() {Name = "Bacon"};
	}

	private static async Task< Egg > FryEggsAsync( int howMany ) {
		Console.WriteLine( $"Eggs 0 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( "Warming the egg pan..." );
		await Task.Delay( 3000 );
		Console.WriteLine( $"Eggs 1 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( $"cracking {howMany} eggs" );
		Console.WriteLine( "cooking the eggs ..." );
		await Task.Delay( 3000 );
		Console.WriteLine( $"Eggs 2 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( "Put eggs on plate" );

		return new Egg() {Name = "egg"};
	}

	private static Coffee PourCoffee() {
		Console.WriteLine( $"Coffee 0 t{Thread.CurrentThread.ManagedThreadId} {Thread.CurrentThread.IsBackground} {DateTime.Now}" );
		Console.WriteLine( "Pouring coffee" );
		return new Coffee() {Name = "coffee"};
	}
}


/*
Main t1
Coffee 0 t1 15:16:33
Eggs 0 t1 15:16:33
Bacon 0 t1 15:16:33
MTWBJ 0 t1 15:16:33
Toast 0 t1 15:16:33
Bacon 1 t8 15:16:36
Toast 1 t4 15:16:36
Eggs 1 t14 15:16:36
MTWBJ 1 t4 15:16:36
Butter t4 15:16:36
Jam t4 15:16:36
Bacon 2 t14 15:16:39
Eggs 2 t4 15:16:39
OJ t14 15:16:39
*/

/*
Main t1 False
is back True
Coffee 0 t1 False 12/3/2025 7:39:52 AM
Pouring coffee
coffee is ready
Eggs 0 t1 False 12/3/2025 7:39:52 AM
Warming the egg pan...
Bacon 0 t1 False 12/3/2025 7:39:52 AM
putting 3 slices of bacon in the pan
cooking first side of bacon...
MTWBJ 0 t1 False 12/3/2025 7:39:52 AM
Toast 0 t1 False 12/3/2025 7:39:52 AM
Putting a slice of bread in the toaster
Putting a slice of bread in the toaster
Start toasting...
tasks created
Eggs 1 t4 True 12/3/2025 7:39:55 AM
cracking 2 eggs
cooking the eggs ...
Bacon 1 t4 True 12/3/2025 7:39:55 AM
flipping a slice of bacon
flipping a slice of bacon
flipping a slice of bacon
cooking the second side of bacon...
Toast 1 t4 True 12/3/2025 7:39:55 AM
Remove toast from toaster
MTWBJ 1 t4 True 12/3/2025 7:39:55 AM
Butter t4 True 12/3/2025 7:39:55 AM
Putting butter on the toast
Jam t4 True 12/3/2025 7:39:55 AM
Putting jam on the toast
toast is ready
Bacon 2 t4 True 12/3/2025 7:39:58 AM
Put bacon on plate
Eggs 2 t13 True 12/3/2025 7:39:58 AM
Put eggs on plate
bacon is ready
eggs are ready
OJ t4 True 12/3/2025 7:39:58 AM
Pouring orange juice
oj is ready
Breakfast is ready!
*/
