import json
import os
import csv

VALIDATION_FOLDER = "validation_results"
SIMULATION_FOLDER = "results"

comparison_rows = []

for filename in os.listdir(VALIDATION_FOLDER):

    if filename.endswith("_validation.json"):

        validation_path = os.path.join(
            VALIDATION_FOLDER,
            filename
        )

        with open(validation_path, "r", encoding="utf-8") as file:
            validation_result = json.load(file)

        if not validation_result["quest_id"].startswith("G"):
            continue

        quest_number = filename.replace("_validation.json", "")

        simulation_filename = quest_number + "_result.json"
        simulation_path = os.path.join(
            SIMULATION_FOLDER,
            simulation_filename
        )

        if os.path.exists(simulation_path):

            with open(simulation_path, "r", encoding="utf-8") as file:
                simulation_result = json.load(file)

            row = {
                "quest_id": validation_result["quest_id"],
                "title": validation_result["title"],
                "static_result": validation_result["result"],
                "simulation_result": simulation_result["result"]
            }

            comparison_rows.append(row)

comparison_rows.sort(key=lambda row: row["quest_id"])

print("Quest Comparison")
print("----------------")

for row in comparison_rows:
    print(
        row["quest_id"],
        "| Static:",
        row["static_result"],
        "| Simulation:",
        row["simulation_result"]
    )


with open("comparison.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "quest_id",
        "title",
        "static_result",
        "simulation_result"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(comparison_rows)


print("\nComparison saved to comparison.csv")

total = len(comparison_rows)

static_pass = sum(
    1 for row in comparison_rows
    if row["static_result"] == "PASS"
)

simulation_pass = sum(
    1 for row in comparison_rows
    if row["simulation_result"] == "PASS"
)

static_pass_simulation_fail = sum(
    1 for row in comparison_rows
    if row["static_result"] == "PASS"
    and row["simulation_result"] == "FAIL"
)

print("\n--- Summary ---")
print("Total Quests:", total)
print("Static Validation PASS:", static_pass)
print("Simulation PASS:", simulation_pass)
print(
    "Static PASS but Simulation FAIL:",
    static_pass_simulation_fail
)