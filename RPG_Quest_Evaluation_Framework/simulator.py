import json
import os

from game_rules import ITEM_LOCATIONS

QUEST_FOLDER = "generated_quests"
RESULT_FOLDER = "results"


def simulate_quest(quest):
    player = {
        "location": quest["start_location"],
        "level": quest["required_level"],
        "inventory": []
    }

    simulation_errors = []

    for objective in quest["objectives"]:
        action = objective["action"]
        target = objective["target"]

        if action == "travel":
            player["location"] = target

        elif action == "return":
            player["location"] = target

        elif action == "collect":
            if target in ITEM_LOCATIONS:
                required_location = ITEM_LOCATIONS[target]

                if player["location"] == required_location:
                    player["inventory"].append(target)
                else:
                    error = {
                        "type": "UNREACHABLE_OBJECTIVE",
                        "step": objective["step"],
                        "message": "Item cannot be collected at current location"
                    }
                    simulation_errors.append(error)

            else:
                error = {
                    "type": "UNKNOWN_ITEM",
                    "step": objective["step"],
                    "message": "Unknown item"
                }
                simulation_errors.append(error)

        else:
            error = {
                "type": "UNKNOWN_ACTION",
                "step": objective["step"],
                "message": "Unknown action: " + action
            }
            simulation_errors.append(error)

    result_data = {
        "quest_id": quest["quest_id"],
        "title": quest["title"],
        "result": "PASS" if len(simulation_errors) == 0 else "FAIL",
        "errors": simulation_errors
    }

    return result_data


os.makedirs(RESULT_FOLDER, exist_ok=True)

for filename in os.listdir(QUEST_FOLDER):

    if filename.endswith(".json"):
        quest_path = os.path.join(QUEST_FOLDER, filename)

        with open(quest_path, "r", encoding="utf-8") as file:
            quest = json.load(file)

        result = simulate_quest(quest)

        print(
            quest["quest_id"],
            "-",
            quest["title"],
            "=>",
            result["result"]
        )
        if result["errors"]:
            print("Errors:", result["errors"])

        result_filename = filename.replace(".json", "_result.json")
        result_path = os.path.join(RESULT_FOLDER, result_filename)

        with open(result_path, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)

print("\nBatch simulation completed.")