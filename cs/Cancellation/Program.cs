
namespace Cancellation;

static class Program
{
	static async Task Main()
	{
		var cts = new CancellationTokenSource();

		Task longRunningTask = DoWorkAsync(cts.Token);

		Console.WriteLine("Press any key to cancel...");
		Console.ReadKey();

		await cts.CancelAsync();

		try
		{
			await longRunningTask;
			Console.WriteLine("Task completed successfully 2.");
		}
		catch (OperationCanceledException)
		{
			Console.WriteLine("Task was canceled (via exception) 2.");
		}
		catch (Exception ex)
		{
			Console.WriteLine($"Task faulted 2: {ex.Message}");
		}
	}

	static async Task DoWorkAsync(CancellationToken token)
	{
		Console.WriteLine("Work started...");
		HttpClient client = new HttpClient();
		
		try
		{
			// Simulate work in chunks (e.g., processing items, polling, etc.)
			for (int i = 0; i < 100; i++)
			{
				// Check for cancellation request - this avoids throwing
				if (token.IsCancellationRequested)
				{
//					token.ThrowIfCancellationRequested(); // Now throws if requested
					Console.WriteLine("Cancellation requested. Cleaning up and exiting gracefully...");
					// Perform any cleanup here if needed
					return; // Exit the method cleanly
				}
				_ = await client.GetStringAsync("http://www.httpbin.org/delay/1", CancellationToken.None); // or ct to trigger exception
				// or simulate some work
//				await Task.Delay(100, CancellationToken.None); // Use None here to avoid auto-throw
//				Thread.Sleep(100); // won't allow cancellation if there is no a-sync code in the function
//				await Task.Delay(100, token); // cancel via exception

				Console.WriteLine($"Progress: {i + 1}/100");
			}

//			await longRunningTask;
			Console.WriteLine("Task completed successfully.");
		}
		catch (OperationCanceledException)
		{
			Console.WriteLine("Task was canceled (via exception).");
			throw;
		}
		catch (Exception ex)
		{
			Console.WriteLine($"Task faulted: {ex.Message}");
			throw;
		}

		Console.WriteLine("All work completed normally.");
	}
}
