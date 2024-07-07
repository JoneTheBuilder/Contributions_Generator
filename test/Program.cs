using System;
using System.Diagnostics;
using System.IO;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length != 6)
        {
            Console.WriteLine("Usage: generate_contributions <start_year> <start_month> <start_day> <end_year> <end_month> <end_day>");
            return;
        }

        try
        {
            // Parse command-line arguments
            int startYear = int.Parse(args[0]);
            int startMonth = int.Parse(args[1]);
            int startDay = int.Parse(args[2]);
            int endYear = int.Parse(args[3]);
            int endMonth = int.Parse(args[4]);
            int endDay = int.Parse(args[5]);

            DateTime startDate = new DateTime(startYear, startMonth, startDay);
            DateTime endDate = new DateTime(endYear, endMonth, endDay);

            // Iterate over date range
            foreach (var date in DateRange(startDate, endDate))
            {
                int commitsCount = new Random().Next(3, 100);

                for (int i = 0; i < commitsCount; i++)
                {
                    string commitMessage = GetRandomString(8);

                    // Write random commit message to file
                    File.AppendAllText("file.txt", commitMessage + Environment.NewLine);

                    // Format the date for Git
                    string formattedDate = date.ToString("ddd MMM dd HH:mm:ss yyyy +0000");

                    // Add and commit using Git
                    ExecuteGitCommand("add .");
                    ExecuteGitCommand($"commit -m \"{commitMessage}\" --date=\"{formattedDate}\"", formattedDate);
                }
            }

            // Push changes to the repository
            ExecuteGitCommand("push -u origin main");

            // Clean up temporary file
            if (File.Exists("file.txt"))
            {
                File.Delete("file.txt");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }

    static IEnumerable<DateTime> DateRange(DateTime start, DateTime end)
    {
        for (var date = start; date <= end; date = date.AddDays(1))
        {
            yield return date;
        }
    }

    static string GetRandomString(int length)
    {
        const string chars = "abcdefghijklmnopqrstuvwxyz";
        var random = new Random();
        var builder = new StringBuilder();

        for (int i = 0; i < length; i++)
        {
            builder.Append(chars[random.Next(chars.Length)]);
        }

        return builder.ToString();
    }

    static void ExecuteGitCommand(string command, string committerDate = null)
    {
        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = "git",
                Arguments = command,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            }
        };

        // Set the GIT_COMMITTER_DATE environment variable if provided
        if (!string.IsNullOrEmpty(committerDate))
        {
            process.StartInfo.Environment["GIT_COMMITTER_DATE"] = committerDate;
        }

        process.Start();

        string output = process.StandardOutput.ReadToEnd();
        string error = process.StandardError.ReadToEnd();

        process.WaitForExit();

        if (process.ExitCode != 0)
        {
            Console.WriteLine($"Error: {error}");
        }
    }
}
