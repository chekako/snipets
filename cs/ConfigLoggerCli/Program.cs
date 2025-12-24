using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace ConfigLoggerCli;

class Program {
	static void Main(string [] args) {
var builder = Host.CreateApplicationBuilder(args);

// 1. Load configuration from appsettings.json
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

// 2. Bind AppSettings
builder.Services.Configure<AppSettings>(
    builder.Configuration.GetSection("AppSettings"));

// 3. Configure logging (console + optional file)
builder.Logging.ClearProviders();
builder.Logging.AddConsole();
builder.Logging.AddDebug();

// Optional: Set minimum log level from config
var tempConfig = builder.Configuration.GetSection("AppSettings:Logging:Level").Get<string>();
if (Enum.TryParse<LogLevel>(tempConfig, true, out var level))
{
    builder.Logging.SetMinimumLevel(level);
}

// 4. Register ConfigurationService as Singleton with Lazy<ILogger<T>> to break circular dependency
builder.Services.AddSingleton<IConfigurationService>(provider =>
{
    var options = provider.GetRequiredService<IOptions<AppSettings>>();
    var loggerFactory = provider.GetRequiredService<ILoggerFactory>();

    var lazyLogger = new Lazy<ILogger<ConfigurationService>>(
        () => loggerFactory.CreateLogger<ConfigurationService>());

    return new ConfigurationService(options, lazyLogger);
});

// Build and run the host
using var host = builder.Build();

// Resolve services
var configService = host.Services.GetRequiredService<IConfigurationService>();
var logger = host.Services.GetRequiredService<ILogger<Program>>();

logger.LogInformation("Application started successfully");
configService.LogStartup();

Console.WriteLine($"App Name: {configService.Settings.ApplicationName}");
Console.WriteLine($"Configured Log Level: {configService.Settings.Logging.Level}");
Console.WriteLine("Press any key to exit...");
Console.ReadKey();
	}
}

