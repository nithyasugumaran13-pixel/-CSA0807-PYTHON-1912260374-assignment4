from pathlib import Path
from datetime import datetime


# Month to be processed
MONTH = "2026-10"


def process_attendance(input_folder, output_folder):

    # Create output folder if it does not exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Store attendance counts for each student
    attendance = {}

    # Store damaged records
    damaged_records = []

    # Find all daily files for the selected month
    files = sorted(Path(input_folder).glob(
        f"attendance_{MONTH}-*.txt"
    ))

    if not files:
        print("No attendance files found for", MONTH)

    # Process each daily file
    for file_path in files:

        try:
            with open(file_path, "r", encoding="utf-8") as file:

                # Read one line at a time
                for line_number, line in enumerate(file, start=1):

                    try:
                        # Separate the three fields
                        parts = line.strip().split(",")

                        # Check whether exactly 3 fields are present
                        if len(parts) != 3:
                            raise ValueError(
                                "Expected 3 fields"
                            )

                        register_number = parts[0].strip()
                        date_text = parts[1].strip()
                        status = parts[2].strip().upper()

                        # Check register number
                        if not register_number:
                            raise ValueError(
                                "Register number is missing"
                            )

                        # Check date format
                        try:
                            record_date = datetime.strptime(
                                date_text, "%Y-%m-%d"
                            )
                        except ValueError as error:
                            raise ValueError(
                                "Invalid date format"
                            ) from error

                        # Check that the record belongs to the selected month
                        if record_date.strftime("%Y-%m") != MONTH:
                            raise ValueError(
                                "Record is outside the selected month"
                            )

                        # Check attendance status
                        if status not in ("P", "A"):
                            raise ValueError(
                                "Status must be P or A"
                            )

                        # Create a dictionary entry for a new student
                        if register_number not in attendance:
                            attendance[register_number] = {
                                "present": 0,
                                "absent": 0
                            }

                        # Update the attendance count
                        if status == "P":
                            attendance[register_number]["present"] += 1
                        else:
                            attendance[register_number]["absent"] += 1

                    except ValueError as error:

                        # Record the file name, line number and reason
                        damaged_records.append(
                            f"{file_path.name}, Line {line_number}: "
                            f"{line.strip()} | {error}"
                        )

        except FileNotFoundError:
            damaged_records.append(
                f"{file_path.name}: File not found"
            )

        except PermissionError:
            damaged_records.append(
                f"{file_path.name}: Permission denied"
            )

        except UnicodeDecodeError:
            damaged_records.append(
                f"{file_path.name}: Encoding error"
            )

        except OSError as error:
            damaged_records.append(
                f"{file_path.name}: File error - {error}"
            )

    # Create the attendance report
    report_file = Path(output_folder) / "attendance_report.txt"

    with open(report_file, "w", encoding="utf-8") as report:

        report.write("MONTHLY ATTENDANCE REPORT\n")
        report.write("=" * 65 + "\n")
        report.write(f"Month: {MONTH}\n\n")

        report.write(
            f"{'Register Number':<18}"
            f"{'Present':<10}"
            f"{'Absent':<10}"
            f"{'Percentage':<12}\n"
        )

        report.write("-" * 65 + "\n")

        below_75 = []

        # Calculate percentage for every student
        for register_number, counts in sorted(attendance.items()):

            present = counts["present"]
            absent = counts["absent"]
            total_days = present + absent

            percentage = (present / total_days) * 100

            report.write(
                f"{register_number:<18}"
                f"{present:<10}"
                f"{absent:<10}"
                f"{percentage:.2f}%\n"
            )

            if percentage < 75:
                below_75.append(
                    (register_number, percentage)
                )

        # Write the list of students below 75%
        report.write("\nSTUDENTS BELOW 75% ATTENDANCE\n")
        report.write("-" * 65 + "\n")

        if below_75:
            for register_number, percentage in below_75:
                report.write(
                    f"{register_number} - {percentage:.2f}%\n"
                )
        else:
            report.write("No students below 75%.\n")

    # Create the damaged records log
    error_file = Path(output_folder) / "damaged_records.txt"

    with open(error_file, "w", encoding="utf-8") as error_log:

        error_log.write("DAMAGED ATTENDANCE RECORDS\n")
        error_log.write("=" * 65 + "\n")

        if damaged_records:
            for record in damaged_records:
                error_log.write(record + "\n")
        else:
            error_log.write("No damaged records found.\n")

    # Display the report in the terminal
    print("\nMONTHLY ATTENDANCE REPORT")
    print("=" * 45)

    for register_number, counts in sorted(attendance.items()):

        present = counts["present"]
        absent = counts["absent"]
        total_days = present + absent
        percentage = (present / total_days) * 100

        print(
            f"{register_number} | "
            f"Present: {present} | "
            f"Absent: {absent} | "
            f"Attendance: {percentage:.2f}%"
        )

    print("\nSTUDENTS BELOW 75%")
    print("-" * 45)

    if below_75:
        for register_number, percentage in below_75:
            print(f"{register_number}: {percentage:.2f}%")
    else:
        print("No students below 75%.")

    print("\nDAMAGED RECORDS")
    print("-" * 45)

    if damaged_records:
        for record in damaged_records:
            print(record)
    else:
        print("No damaged records found.")

    print("\nReports successfully saved!")
    print("Attendance report:", report_file)
    print("Damaged records:", error_file)


# Main program
if __name__ == "__main__":

    # Find the Q2 folder
    folder = Path(__file__).parent

    input_folder = folder / "input"
    output_folder = folder / "output"

    process_attendance(input_folder, output_folder)