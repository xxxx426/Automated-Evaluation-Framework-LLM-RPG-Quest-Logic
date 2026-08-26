import csv
import json
import os
import time
from google import genai

# Gemini client reads GEMINI_API_KEY from environment
client = genai.Client()

OUTPUT_FOLDER = "generated_quests"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
LOG_FILE = "generation_log.csv"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "quest_id",
            "difficulty",
            "filename",
            "status",
            "attempts"
        ])

# Small test batch first
DIFFICULTIES = {
    "easy": 20,
    "medium": 20,
    "hard": 20
}

MODEL_NAME = "gemini-3.5-flash"


def create_prompt(difficulty, quest_id):
    if difficulty == "easy":
        difficulty_rule = """
Create exactly 3 objectives.
Use no more than 2 locations.
Use simple travel, collect and return actions.
"""
    elif difficulty == "medium":
        difficulty_rule = """
Create 4 or 5 objectives.
Use at least 2 locations.
Include at least one collect action.
The quest should require multiple state changes.
"""
    else:
        difficulty_rule = """
Create between 6 and 8 objectives.
Use at least 3 locations.
Include at least two collect actions or other dependent objectives.
The quest should contain a longer sequence of dependent actions.
"""

    prompt = f"""
Generate ONE RPG quest for an automated game-logic testing experiment.

Quest ID: {quest_id}
Difficulty: {difficulty}

Return ONLY valid JSON.
Do not include Markdown.
Do not include explanations.

The JSON must follow exactly this structure:

{{
  "quest_id": "{quest_id}",
  "title": "Quest title",
  "difficulty": "{difficulty}",
  "required_level": 1,
  "start_location": "Village",
  "objectives": [
    {{
      "step": 1,
      "action": "travel",
      "target": "Forest"
    }}
  ],
  "reward": {{
    "experience": 100
  }}
}}

Rules:

required_level:
integer from 1 to 10

Valid locations:
Village
Forest
Cave
Castle

Valid actions:
travel
collect
return

Valid items:
Lost Sword
Key
Health Potion
Magic Stone

Item locations:
Lost Sword = Forest
Key = Castle
Health Potion = Village
Magic Stone = Cave

Difficulty requirements:
{difficulty_rule}

The objective step numbers must start at 1 and increase by 1.

Generate the quest independently.
Do not copy the example exactly.

Return only the JSON object.
"""

    return prompt


quest_counter = 1

for difficulty, amount in DIFFICULTIES.items():

    for number in range(1, amount + 1):

        quest_id = f"G{quest_counter:03d}"

        filename = f"gemini_{difficulty}_{number:03d}.json"
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        # Skip quests that were already generated successfully
        if os.path.exists(output_path):
            print(f"Skipping existing file: {output_path}")
            quest_counter += 1
            continue

        print(
            f"\nGenerating {quest_id} "
            f"({difficulty}, {number}/{amount})..."
        )

        prompt = create_prompt(difficulty, quest_id)

        max_retries = 5
        response = None

        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )
                break

            except Exception as error:
                error_message = str(error)

                print(
                    f"Attempt {attempt}/{max_retries} failed:",
                    error_message
                )


                if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                    print("Quota exhausted. Stopping the generation process.")
                    raise SystemExit

                # Temporary API errors: retry after waiting
                if attempt < max_retries:
                    wait_time = attempt * 10
                    print(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print("Maximum retries reached.")

        if response is None:
            with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    quest_id,
                    difficulty,
                    filename,
                    "FAILED_API",
                    max_retries
                ])

            quest_counter += 1
            continue
        text = response.text.strip()

        # Remove Markdown fences if returned
        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            quest = json.loads(text)

            # Force experiment identifiers to remain consistent
            quest["quest_id"] = quest_id
            quest["difficulty"] = difficulty

            with open(
                    output_path,
                    "w",
                    encoding="utf-8"
            ) as file:

                json.dump(
                    quest,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print("Saved:", output_path)
            with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    quest_id,
                    difficulty,
                    filename,
                    "SUCCESS",
                    attempt
                ])

        except json.JSONDecodeError:
            with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    quest_id,
                    difficulty,
                    filename,
                    "INVALID_JSON",
                    attempt
                ])
            print(
                "ERROR:",
                quest_id,
                "did not return valid JSON."
            )

        quest_counter += 1

        # Small pause between API requests
        time.sleep(2)


print("\nQuest generation completed.")