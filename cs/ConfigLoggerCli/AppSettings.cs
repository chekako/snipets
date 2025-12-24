namespace ConfigLoggerCli;

public class AppSettings
{
    public string ApplicationName { get; set; } = "ConsoleDemo";
    public LoggingSettings Logging { get; set; } = new();
}

public class LoggingSettings
{
    public string Level { get; set; } = "Information";
    public bool EnableFileLogging { get; set; } = false;
}

