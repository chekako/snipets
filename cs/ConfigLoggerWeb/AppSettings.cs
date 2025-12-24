namespace ConfigLoggerWeb;

public class AppSettings
{
    public LoggingSettings Logging { get; set; } = new();
    public string ApplicationName { get; set; } = "MyApp";
}

public class LoggingSettings
{
    public string Level { get; set; } = "Information";
    public bool EnableFileLogging { get; set; } = false;
}

