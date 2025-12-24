using Microsoft.Extensions.Options;

namespace ConfigLoggerWeb;
public class Program
{
	public static void Main( string[] args ) {
var builder = WebApplication.CreateBuilder(args);

// 1. Bind configuration from appsettings.json (and environment, etc.)
builder.Services.Configure<AppSettings>(
    builder.Configuration.GetSection("AppSettings"));

// 2. Add logging (standard Microsoft.Extensions.Logging)
builder.Logging.ClearProviders();
builder.Logging.AddConsole();
builder.Logging.AddDebug();

// Optional: dynamically set minimum log level from config (runs after build)
builder.Services.PostConfigure<LoggerFilterOptions>(options =>
{
    var config = builder.Configuration.GetSection("AppSettings:Logging:Level").Get<string>();
    if (Enum.TryParse<LogLevel>(config, true, out var level))
    {
        options.MinLevel = level;
    }
});

// 3. Register our configuration service as Singleton
//    Use Lazy<ILogger<T>> to break circular reference
builder.Services.AddSingleton<IConfigurationService, ConfigurationService>(
    provider =>
    {
        var options = provider.GetRequiredService<IOptionsSnapshot<AppSettings>>();
        var loggerFactory = provider.GetRequiredService<ILoggerFactory>();
        var logger = new Lazy<ILogger<ConfigurationService>>(
            () => loggerFactory.CreateLogger<ConfigurationService>());

        return new ConfigurationService(options, logger);
    });

// 4. Add controllers (for demo)
builder.Services.AddControllers();

var app = builder.Build();

app.MapControllers();

// Demo endpoint to show both services working
app.MapGet("/status", (IConfigurationService config, ILogger<Program> logger) =>
{
    logger.LogInformation("Status endpoint called");
    config.Reload();
    return new
    {
        AppName = config.Settings.ApplicationName,
        LogLevel = config.Settings.Logging.Level,
        Message = "Services are running"
    };
});

app.Run();
		
	}
}



/*
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapGet("/weatherforecast", () =>
{
    var forecast =  Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast");

app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
*/

