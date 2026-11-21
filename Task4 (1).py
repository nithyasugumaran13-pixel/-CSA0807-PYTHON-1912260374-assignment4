
from pathlib import Path

# Find the Q4 folder and create input/output folders
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# PART 1: ORIGINAL FAULTY PROGRAM
# --------------------------------------------------

def save_returns_faulty(books):
    # Defect 1: "w" overwrites the previous contents
    log = open(OUTPUT_DIR / "flawed_returns.log", "w")

    # Defect 2: No newline is added after each book
    for book in books:
        log.write(book)

    log.close()


def process_faulty(day_file):
    try:
        # Read the day's books
        books = open(day_file).read().split("\n")
        save_returns_faulty(books)

    except FileNotFoundError:
        print("missing")


# --------------------------------------------------
# PART 2: CORRECTED PROGRAM
# --------------------------------------------------

def write_error(message):
    """Save an error message in the error log."""
    error_file = OUTPUT_DIR / "error_log.txt"

    with open(error_file, "a", encoding="utf-8") as file:
        file.write(message + "\n")


def save_returns(books):
    """Add returned books without deleting earlier records."""

    log_file = OUTPUT_DIR / "returns.log"

    # "a" adds new data without deleting old data
    with open(log_file, "a", encoding="utf-8") as file:
        for book in books:
            if book.strip():
                file.write(book.strip() + "\n")


def process(day_file):
    """Read one day's file and save its returned books."""

    try:
        # with automatically closes the input file
        with open(day_file, "r", encoding="utf-8") as file:
            books = file.read().splitlines()

        save_returns(books)
        print(f"Successfully processed: {Path(day_file).name}")

    except FileNotFoundError as error:
        message = f"File not found: {day_file} | {error}"
        print(message)
        write_error(message)

    except PermissionError as error:
        message = f"Permission denied: {day_file} | {error}"
        print(message)
        write_error(message)

    except UnicodeDecodeError as error:
        message = f"Encoding error: {day_file} | {error}"
        print(message)
        write_error(message)

    except OSError as error:
        message = f"File processing error: {day_file} | {error}"
        print(message)
        write_error(message)


# --------------------------------------------------
# PART 3: RUN THREE-DAY TESTS
# --------------------------------------------------

if __name__ == "__main__":

    day_files = [
        INPUT_DIR / "day1.txt",
        INPUT_DIR / "day2.txt",
        INPUT_DIR / "day3.txt"
    ]

    # Remove old output files to make the test repeatable
    for filename in [
        "flawed_returns.log",
        "returns.log",
        "error_log.txt"
    ]:
        output_file = OUTPUT_DIR / filename
        if output_file.exists():
            output_file.unlink()

    print("=" * 55)
    print("FILE AND EXCEPTION FORENSICS")
    print("=" * 55)

    # Run the original faulty program
    print("\n1. ORIGINAL FAULTY PROGRAM")
    print("-" * 55)

    for day_file in day_files:
        process_faulty(day_file)

    flawed_file = OUTPUT_DIR / "flawed_returns.log"

    print("\nFaulty log contents:")
    print(flawed_file.read_text(encoding="utf-8"))

    # Run the corrected program
    print("\n2. CORRECTED PROGRAM")
    print("-" * 55)

    for day_file in day_files:
        process(day_file)

    corrected_file = OUTPUT_DIR / "returns.log"

    print("\nCorrected log contents:")
    print(corrected_file.read_text(encoding="utf-8"))

    # Test a missing file
    print("\n3. MISSING FILE TEST")
    print("-" * 55)

    missing_file = INPUT_DIR / "day4.txt"
    process(missing_file)

    # Display the saved error log
    error_file = OUTPUT_DIR / "error_log.txt"

    print("\nSaved error log:")
    print(error_file.read_text(encoding="utf-8"))

    print("\nALL TESTS COMPLETED.")
    print("Output files are saved in the Q4/output folder.")
