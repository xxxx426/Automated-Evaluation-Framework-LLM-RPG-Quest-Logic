# LLM RPG Quest Evaluation Framework

This repository contains the practical artefact developed for the dissertation project:

**Evaluating LLM-Generated RPG Quest Logic Through Automated Rule-Based Testing**

The project implements a lightweight Python framework for generating structured RPG quests using a Large Language Model (LLM), validating the generated quests using predefined rules, executing them in a simplified RPG simulation environment, and comparing the results of the two testing stages.

## Project Overview

The framework consists of four main stages:

1. Quest generation using the Gemini API
2. Static rule-based validation
3. Execution-based RPG simulation
4. Comparison of validation and simulation results

Generated quests are stored in JSON format so that the same structured quest data can be processed automatically by both the validator and simulator.

## Project Structure

- `quest_generator.py` - Generates structured RPG quests using the Gemini API.
- `game_rules.py` - Defines the rules and game-world values used by the framework.
- `validator.py` - Performs static rule-based validation of generated quests.
- `simulator.py` - Executes quests in a lightweight RPG simulation environment.
- `compare_results.py` - Compares static validation and simulation results.
- `generated_quests/` - Contains the quests used in the final experiment.
- `validation_results/` - Contains static validation results.
- `results/` - Contains simulation results.
- `comparison.csv` - Contains the comparison between validation and simulation outcomes.
- `generation_log.csv` - Records quest generation attempts and their outcomes.
- `requirements.txt` - Lists the external Python package required by the project.

## Final Dataset

The final experiment used 12 easy-difficulty RPG quests:

`gemini_easy_001.json` to `gemini_easy_012.json`

All 12 quests passed static validation and all 12 completed successfully during simulation.

The final dataset was limited to easy-difficulty quests because API usage limits prevented the planned larger dataset containing medium and hard quests from being completed.

## Requirements

The project requires Python and the Google Gen AI Python package.

Install the required package using:

    pip install -r requirements.txt

The `requirements.txt` file contains:

    google-genai==2.18.1

## API Configuration

Quest generation requires a Gemini API key.

The API key is not included in this repository for security reasons.

The environment variable `GEMINI_API_KEY` must be configured before running `quest_generator.py`.

The generated quest files already included in this repository can be used to run the validation, simulation and comparison stages without generating new quests.

## Running the Framework

The main scripts can be executed in the following order:

    python quest_generator.py
    python validator.py
    python simulator.py
    python compare_results.py

If the existing generated quest dataset is used, `quest_generator.py` does not need to be run again.

## Experimental Results

The final experiment produced the following results:

- Static validation: 12 PASS, 0 FAIL
- RPG simulation: 12 PASS, 0 FAIL
- Static PASS / Simulation FAIL: 0

These results relate only to the final dataset used in this project and should not be interpreted as evidence that all LLM-generated RPG quests are logically valid.

## Notes

The framework is a proof-of-concept implementation developed for academic research.

The simulator represents a simplified RPG environment and supports only the game states and rules required for this experiment.