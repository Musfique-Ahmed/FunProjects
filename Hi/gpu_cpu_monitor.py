import psutil
import time
import datetime
import os

def monitor_performance(interval_seconds=5, duration_minutes=1, log_file="performance_log.txt"):
    """
    Monitors CPU and memory usage and logs the data to a file.

    Args:
        interval_seconds (int): The interval (in seconds) between data collection points.
        duration_minutes (int): The total duration (in minutes) for monitoring.
        log_file (str): The name of the file to log performance data.
    """
    end_time = time.time() + (duration_minutes * 60)

    print(f"Starting system performance monitoring for {duration_minutes} minutes...")
    print(f"Data will be logged to: {os.path.abspath(log_file)}")

    try:
        with open(log_file, 'a') as f:
            # Write header if the file is new or empty
            if os.stat(log_file).st_size == 0:
                f.write("Timestamp,CPU_Usage_Percent,Memory_Usage_Percent\n")

            while time.time() < end_time:
                # Get current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Get CPU usage (non-blocking, interval=None for immediate result)
                cpu_usage = psutil.cpu_percent(interval=None)

                # Get memory usage
                # psutil.virtual_memory() returns a named tuple
                # .percent gives the percentage of memory used
                memory_info = psutil.virtual_memory()
                memory_usage = memory_info.percent

                log_entry = f"{timestamp},{cpu_usage:.2f},{memory_usage:.2f}\n"
                f.write(log_entry)
                print(f"Logged: {log_entry.strip()}")

                time.sleep(interval_seconds)
        print(f"\nMonitoring complete. Data saved to {log_file}")

    except PermissionError:
        print(f"Error: Permission denied to write to {log_file}. Please check file permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    # Monitor every 5 seconds for 1 minute, logging to 'my_performance_data.txt'
    monitor_performance(interval_seconds=5, duration_minutes=1, log_file="my_performance_data.txt")

    # You can change these parameters:
    # monitor_performance(interval_seconds=10, duration_minutes=5, log_file="long_term_log.csv")
