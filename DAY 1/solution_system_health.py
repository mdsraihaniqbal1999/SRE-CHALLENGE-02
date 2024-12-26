import os
import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time


def check_disk_usage():
    """Check the disk usage on the system."""
    usage = psutil.disk_usage('/')
    return f"Disk Usage: {usage.percent}% used of total {usage.total / (1024 ** 3):.2f} GB"


def monitor_services():
    """List running services."""
    try:
        services = [p.info for p in psutil.process_iter(['name', 'status']) if p.info['status'] == psutil.STATUS_RUNNING]
        running_services = "\n".join([f"Service: {s['name']}" for s in services])
        return f"Running Services:\n{running_services}" if running_services else "No running services found."
    except Exception as e:
        return f"Error monitoring services: {e}"


def assess_memory_usage():
    """Check memory usage."""
    memory = psutil.virtual_memory()
    return f"Memory Usage: {memory.percent}% of total {memory.total / (1024 ** 3):.2f} GB"


def evaluate_cpu_usage():
    """Check CPU usage."""
    cpu_percent = psutil.cpu_percent(interval=1)
    return f"CPU Usage: {cpu_percent}%"


def send_email_report():
    """Send a comprehensive system report via email."""
    sender_email = "rockrocking1995@gmail.com"
    recipient_email = "raihaniqbal@kpmg.com"
    password = " "  # Replace this with your app-specific password for Gmail

    # Create the email
    subject = f"System Health Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    body = (
        f"{check_disk_usage()}\n\n"
        f"{monitor_services()}\n\n"
        f"{assess_memory_usage()}\n\n"
        f"{evaluate_cpu_usage()}"
    )
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        print("Report sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")


def display_menu():
    """Display a menu for the system health check script."""
    print("System Health Check Menu:")
    print("1. Check Disk Usage")
    print("2. Monitor Running Services")
    print("3. Assess Memory Usage")
    print("4. Evaluate CPU Usage")
    print("5. Send Comprehensive Report via Email (Every 4 Hours)")
    print("6. Exit")


def main():
    """Main function to drive the menu-based tool."""
    while True:
        display_menu()
        try:
            choice = int(input("\nEnter your choice (1-6): "))
            if choice == 1:
                print(check_disk_usage())
            elif choice == 2:
                print(monitor_services())
            elif choice == 3:
                print(assess_memory_usage())
            elif choice == 4:
                print(evaluate_cpu_usage())
            elif choice == 5:
                print("Sending report every 4 hours. Press Ctrl+C to stop.")
                while True:
                    send_email_report()
                    time.sleep(4 * 3600)  # Sleep for 4 hours
            elif choice == 6:
                print("Exiting the program. Stay Healthy!")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
