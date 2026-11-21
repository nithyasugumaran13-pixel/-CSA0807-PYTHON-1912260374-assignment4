import os
import tempfile
from pathlib import Path


# Custom exception for damaged attendance records
class InvalidRecord(Exception):
    """Raised when an attendance line has an invalid format."""


# Custom exception for file-related errors
class AttendanceFileError(Exception):
    """Raised when an attendance file cannot be processed."""


# Function to validate one attendance line
def parse_line(line):

    parts = line.strip().split(",")

    # TODO 1: Check whether exactly 3 fields are present
    if len(parts) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(parts)}"
        )

    register_number = parts[0].strip()
    date = parts[1].strip()
    status = parts[2].strip()

    # Check that register number and date are not empty
    if not register_number or not date:
        raise InvalidRecord("register number or date is missing")

    # Check whether status is P or A
    if status not in ("P", "A"):
        raise InvalidRecord(
            f"invalid status '{status}'"
        )

    # Return the three fields as a tuple
    return register_number, date, status


# Function to process the attendance file
def summarise(path):

    present = 0
    absent = 0
    errors = []

    try:

        try:
            # TODO 2: Open the file safely
            with open(path, "r", encoding="utf-8") as file:

                # Read one line at a time
                for line_number, line in enumerate(file, start=1):

                    try:
                        # Validate the line
                        register_number, date, status = parse_line(line)

                        # Count present and absent students
                        if status == "P":
                            present += 1
                        else:
                            absent += 1

                    except InvalidRecord as error:

                        # Store the line number and error message
                        errors.append(
                            (line_number, str(error))
                        )

        except FileNotFoundError as error:
            raise AttendanceFileError(
                f"File not found: {path}"
            ) from error

        except PermissionError as error:
            raise AttendanceFileError(
                f"Permission denied: {path}"
            ) from error

        except UnicodeDecodeError as error:
            raise AttendanceFileError(
                f"Wrong file encoding: {path}"
            ) from error

        except OSError as error:
            raise AttendanceFileError(
                f"File processing error: {error}"
            ) from error

    except AttendanceFileError as error:

        # Handle file-related errors inside summarise()
        errors.append((0, str(error)))

    else:
        # Runs when file processing completes without a file-level error
        print("File processing completed successfully.")

    finally:
        # Runs whether processing succeeds or fails
        print("File processing attempt finished.")

    return present, absent, errors


# Demonstration of the broad-exception misuse
def misuse_experiment():

    print("\nMISUSE EXPERIMENT")
    print("-" * 40)

    present = 0

    try:
        # Intentional typing mistake:
        # 'presnt' is written instead of 'present'
        presnt += 1

    except Exception:
        # This hides the programming error
        pass

    print("Present count after hidden error:", present)


# Main program
if __name__ == "__main__":

    # Sample data given in the assignment
    data = (
        "192311001,2026-10-08,P\n"
        "192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n"
        "192311004,2026-10-08,L\n"
    )

    # Create a temporary sample file
    with tempfile.NamedTemporaryFile(
        "w",
        suffix=".csv",
        delete=False,
        encoding="utf-8"
    ) as tmp:

        tmp.write(data)
        temporary_filename = tmp.name

    try:
        # Process the temporary file
        result = summarise(temporary_filename)

        print("\nATTENDANCE SUMMARY")
        print("-" * 40)
        print(result)

    finally:
        # Delete the temporary file after testing
        os.remove(temporary_filename)

    # Test the missing-file condition
    print("\nMISSING FILE TEST")
    print("-" * 40)

    missing_result = summarise(
        "file_that_does_not_exist.csv"
    )

    print(missing_result)

    # Demonstrate why broad exception handling is dangerous
    misuse_experiment()