import json
import os

from game_rules import (
    MIN_LEVEL,
    MAX_LEVEL,
    VALID_LOCATIONS,
    VALID_ACTIONS
)

QUEST_FOLDER = "generated_quests"
VALIDATION_RESULT_FOLDER = "validation_results"


def validate_quest(quest):
    errors = []

    # Rule 1: Check required level
    if quest["required_level"] < MIN_LEVEL or quest["required_level"] > MAX_LEVEL:
        errors.append("INVALID_LEVEL")

    # Rule 2: Check objectives exist
    if len(quest["objectives"]) == 0:
        errors.append("MISSING_OBJECTIVES")

    # Rule 3: Check objective step order
    expected_step = 1

    for objective in quest["objectives"]:
        if objective["step"] != expected_step:
            errors.append("INVALID_STEP_ORDER")
            break

        expected_step += 1

    # Rule 4: Check start location
    if quest["start_location"] not in VALID_LOCATIONS:
        errors.append("INVALID_LOCATION")

    # Rule 5: Check actions
    for objective in quest["objectives"]:
        if objective["action"] not in VALID_ACTIONS:
            errors.append("INVALID_ACTION")
            break

    result = "PASS" if len(errors) == 0 else "FAIL"

    return {
        "quest_id": quest["quest_id"],
        "title": quest["title"],
        "result": result,
        "errors": errors
    }
os.makedirs(VALIDATION_RESULT_FOLDER, exist_ok=True)

for filename in os.listdir(QUEST_FOLDER):

    if filename.endswith(".json"):
        quest_path = os.path.join(QUEST_FOLDER, filename)

        with open(quest_path, "r", encoding="utf-8") as file:
            quest = json.load(file)

        result = validate_quest(quest)

        print(
            result["quest_id"],
            "-",
            result["title"],
            "=>",
            result["result"]
        )

        if result["errors"]:
            print("Errors:", result["errors"])

        result_filename = filename.replace(".json", "_validation.json")
        result_path = os.path.join(VALIDATION_RESULT_FOLDER, result_filename)

        with open(result_path, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)

print("\nBatch static validation completed.")