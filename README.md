# Automated-Evaluation-Framework-LLM-RPG-Quest-Logic
Implementation of an automated evaluation framework for LLM‑generated RPG quest logic, including static validation and RPG simulator edge‑case testing. 
## Project Overview
Large Language Models (LLMs) can support the generation of content for role‑playing games (RPGs), including quests and objectives, but generated content may contain logical problems that affect whether a quest can be completed successfully. This creates a need for automated methods that can evaluate quest logic rather than relying only on manual inspection.

This project aimed to design, implement and evaluate an automated framework built in Python for testing the logical consistency of RPG quests produced by LLM. RPG quests were generated through an LLM API and represented as structured JSON data so that they could be processed automatically.

The framework used two testing stages:
1. **Static validation**: rule‑based checks for structural and logical conditions
2. **Simulation‑driven execution test**: lightweight RPG simulator modelling player state (location, inventory, player level)

Experiments evaluated 12 easy‑difficulty LLM‑generated quests. All quests passed static validation and completed execution inside the simulation environment.

> Dissertation artefact for University of Sunderland final‑year project.

## Contents
- Python source code for evaluation framework
- RPG quest JSON sample data
- Static validation rule implementation
- Lightweight RPG state simulator
- Experiment test samples

## Note
This repository is created for dissertation marker review.
