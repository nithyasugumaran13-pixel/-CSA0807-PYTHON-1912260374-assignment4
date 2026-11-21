from pathlib import Path

from fest_registration import (
    process_registrations,
    write_outputs
)


def main():

    base_dir = Path(__file__).resolve().parent

    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    print("=" * 55)
    print("COLLEGE FEST REGISTRATION DESK")
    print("=" * 55)

    print("\nProcessing department registration files...\n")

    # Step 1: Process all registrations
    result = process_registrations(input_dir)

    # Step 2: Generate all output files
    write_outputs(result, output_dir)

    # Step 3: Display master registration details
    print("VALID REGISTRATIONS")
    print("-" * 55)

    for record in result["master_records"]:

        print(
            f"{record['register']} | "
            f"{record['name']} | "
            f"{record['department']}"
        )

    # Step 4: Display event-wise counts
    print("\nEVENT-WISE PARTICIPANT COUNT")
    print("-" * 55)

    for event, participants in result["event_participants"].items():

        print(f"{event}: {len(participants)} participants")

    # Step 5: Display processing summary
    print("\nPROCESSING SUMMARY")
    print("-" * 55)

    print(
        "Valid registrations:",
        len(result["master_records"])
    )

    print(
        "Duplicate registrations:",
        result["duplicate_count"]
    )

    print(
        "Invalid registrations:",
        result["invalid_count"]
    )

    print(
        "Missing department files:",
        result["missing_file_count"]
    )

    print("\nAll output files have been generated.")
    print("Check the Q6/output folder.")


if __name__ == "__main__":
    main()