from typing import Literal
import datetime
import os


def log(
    log_content: str,
    log_type: Literal["critical", "command", "generic"] = "generic",
    print_to_console: bool = False,
):
    # Correct date format, converting datetime object into a string
    date_format = datetime.datetime.now().strftime("[%Y/%m/%d][%H.%M.%S]")
    # The layout of the log to be send
    log_format = f"{date_format} {log_content}\n"

    # Default file to open, being generic
    file_to_open = "generic.log"
    # Default file header message (if file is empty), being generic
    file_header_message = "All GENERIC logs, including logs that don't fit in CRITICAL or COMMAND logs!\n\n"

    # Set the correct file to open and header message based on the log type
    if log_type == "critical":
        file_to_open = "critical.log"
        file_header_message = (
            "All CRITICAL errors, essentially any errors with the code!\n\n"
        )
    elif log_type == "command":
        file_to_open = "command.log"
        file_header_message = (
            "All COMMAND logs, any command use will be logged here!\n\n"
        )

    # If the logs folder doesn't exist, create it
    os.makedirs("logs", exist_ok=True)

    # If the file is not empty set the header message to an empty string
    try:
        if os.path.getsize(f"logs/{file_to_open}") > 0:
            file_header_message = ""
    except FileNotFoundError:
        pass

    if print_to_console:
        print(log_content)

    # Open the specific log file
    with open("logs/" + file_to_open, "a", encoding="utf-8") as file:
        # Write the header message
        file.write(file_header_message)
        # Write the log
        file.write(log_format)
