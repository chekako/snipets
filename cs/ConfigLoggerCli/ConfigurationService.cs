using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace ConfigLoggerCli;

public interface IConfigurationService {
	AppSettings Settings { get; }
	void LogStartup();
}

public class ConfigurationService : IConfigurationService {
	private readonly AppSettings _settings;
	private readonly Lazy< ILogger< ConfigurationService > > _logger;

	public AppSettings Settings => _settings;

	public ConfigurationService(
		IOptions< AppSettings > options,
		Lazy< ILogger< ConfigurationService > > logger ) {
		_settings = options.Value;
		_logger = logger;

		// Safe to log during construction — lazy logger resolves after DI container is built
		_logger.Value.LogInformation(
			"ConfigurationService initialized. App: {AppName}, LogLevel: {LogLevel}",
			_settings.ApplicationName,
			_settings.Logging.Level );
	}

	public void LogStartup() {
		_logger.Value.LogWarning( "Application startup event logged from ConfigurationService" );
	}
}
