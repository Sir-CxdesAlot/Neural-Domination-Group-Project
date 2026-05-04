# data

This folder contains the project data assets, including raw source files and cleaned sample output.

## Data structure

- `data/raw/`: raw input assets in the agreed CSV format.
- `data/processed/`: cleaned, preprocessed sample output ready for analysis.

## Data requirements

All raw assets must:

- be CSV files with a header row
- use UTF-8 encoding
- preserve original source values in `data/raw/`
- include consistent field names matching the schema below
- omit personally identifiable information unless explicitly authorized

## Data schema

The sample dataset uses the following schema:

- `game_id` (integer): unique session or match identifier
- `timestamp` (datetime, ISO 8601): event timestamp for the game log entry
- `player_id` (string): unique player identifier
- `action` (string): action type taken by the player (e.g. `move`, `attack`, `defend`, `heal`)
- `target` (string): optional target identifier for actions such as `attack` or `heal`
- `score_change` (integer): numeric change in score resulting from the action
- `position_x` (float): x-coordinate of the player position at the event
- `position_y` (float): y-coordinate of the player position at the event

The cleaned output adds derived fields:

- `is_combat_action` (boolean): `True` when action is one of `attack`, `defend`, or `heal`
- `normalized_x` (float): `position_x` normalized to [0,1]
- `normalized_y` (float): `position_y` normalized to [0,1]

## Assumptions

- The raw file `data/raw/player_game_logs_raw.csv` is a representative sample collected from game sessions.
- Missing or invalid `score_change` values are replaced with `0` during preprocessing.
- Missing `target` values are stored as empty strings.
- Missing positions are filled with median coordinates.
- Position normalization assumes a fixed game field range of `x = [0, 20]` and `y = [0, 30]`.

## Deliverables

- Data dictionary and assumptions in this file.
- Preprocessing notebook at `notebooks/02_preprocessing.ipynb`.
- Cleaned sample output at `data/processed/player_game_logs_processed.csv`.
