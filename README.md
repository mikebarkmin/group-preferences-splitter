# Group Preference Splitter

## Install

```bash
poetry install 
```

## Run

This will run for `-t 10` seconds and produce `-g 5 4 3` three groups with space for 5, 4 and 3 persons based on their `prerences.xlsx`.

```
poetry run python main.py preferences.xlsx -g 5 4 3 -t 10
```
