namespace ConfigLoggerCli;

public interface IConfigurationService
{
    AppSettings Settings { get; }
    void LogStartup();
}

