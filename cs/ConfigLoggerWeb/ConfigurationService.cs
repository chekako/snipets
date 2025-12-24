using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace ConfigLoggerWeb;

public interface IConfigurationService
{
    AppSettings Settings { get; }
    void Reload(); // Simulate reload if needed
}

public class ConfigurationService : IConfigurationService
{
    private readonly Lazy<ILogger<ConfigurationService>> _logger;
    private AppSettings _settings;

    public AppSettings Settings => _settings;

    public ConfigurationService(
        IOptionsSnapshot<AppSettings> options,
        Lazy<ILogger<ConfigurationService>> logger) // Lazy injection breaks the cycle
    {
        _logger = logger;
        _settings = options.Value;

        // Safe to log here — logger is fully resolved, even if we log during startup
        _logger.Value.LogInformation("Configuration loaded for application '{AppName}' with log level '{LogLevel}'",
            _settings.ApplicationName,
            _settings.Logging.Level);
    }

    public void Reload()
    {
        // In a real app, reload from file/DB/etc.
        _logger.Value.LogWarning("Configuration reload requested");
    }
}

