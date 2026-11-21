
from pathlib import Path
from decimal import Decimal, InvalidOperation


def process_mess_file(filename, report_filename):

    total = Decimal("0.00")
    rejected_lines = []

    # Create output folder if it does not exist
    Path(report_filename).parent.mkdir(
        parents=True, exist_ok=True
    )

    try:
        # Open input and output files safely
        with open(filename, "r", encoding="utf-8") as file, \
             open(report_filename, "w", encoding="utf-8") as report:

            # Read one line at a time
            for line_number, line in enumerate(file, start=1):

                # Skip empty lines
                if not line.strip():
                    continue

                try:
                    # Split the record into fields
                    parts = line.strip().split(",")

                    # Check the number of fields
                    if len(parts) != 3:
                        raise ValueError(
                            f"Expected 3 fields, found {len(parts)}"
                        )

                    register_number = parts[0].strip()
                    name = parts[1].strip()
                    amount_text = parts[2].strip()

                    # Check for missing details
                    if not register_number or not name:
                        raise ValueError(
                            "Register number or name is empty"
                        )

                    # Convert amount into Decimal
                    try:
                        amount = Decimal(amount_text)
                    except InvalidOperation as error:
                        raise ValueError(
                            f"Invalid amount '{amount_text}'"
                        ) from error

                    # Check for invalid special values
                    if not amount.is_finite():
                        raise ValueError(
                            "Amount must be a finite number"
                        )

                    # Calculate total
                    total += amount

                    # Create and save report line
                    report_line = (
                        f"{register_number}, {name}, "
                        f"Rs. {amount:.2f}\n"
                    )

                    report.write(report_line)
                    print(report_line.strip())

                except ValueError as error:

                    # Store rejected records
                    rejected_lines.append(
                        (line_number, line.strip(), str(error))
                    )

    except FileNotFoundError:
        print("Error: Input file not found.")
        return None, rejected_lines

    except PermissionError:
        print("Error: Permission denied.")
        return None, rejected_lines

    except OSError as error:
        print("File processing error:", error)
        return None, rejected_lines

    # Display final results
    print("\nTotal Mess Bill: Rs.", f"{total:.2f}")

    print("\nRejected Records:")

    for record in rejected_lines:
        print(record)

    return total, rejected_lines


# Main program
if __name__ == "__main__":

    # Get the current task folder
    folder = Path(__file__).parent

    # Define input and output paths
    input_file = folder / "input" / "mess_oct.txt"
    output_file = folder / "output" / "mess_report.txt"

    # Execute the function
    total, rejected = process_mess_file(
        input_file,
        output_file
    )

    if total is not None:
        print("\nReport successfully saved!")
        print("Output file:", output_file)
