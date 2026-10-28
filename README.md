# Fishing Game

A text-based Python adventure refactored to improve readability, type safety and maintainability.

Explore locations, collect random fishing loot and rest to recover stamina. Find treasure to win; running out of stamina ends the game.

## Files

| File | Purpose |
| --- | --- |
| [code_1.py](fishing_game.py) | Initial code I made around 1 year ago |
| [code_2.py](fishing_game.py) | Code after simply using "Format document"|
| [code_3.py](fishing_game.py) | Code after fixiung all pylint warning|
| [fishing_game.py](fishing_game.py) | Final playable script |
| [fishing_game_report.pdf](fishing_game_report.pdf) | One-page assignment report |

## Run the game

The script requires Python 3.9 or later and uses only the standard library.
From the folder containing the script, run:

```bash
python fishing_game.py
```

| Command | Action |
| --- | --- |
| `go <direction>` | Follow an exit displayed for the current location |
| `fishing` | Catch a random item and spend 1–15 stamina |
| `diary` | View collected items |
| `sleep` | Restore stamina to 100 |
| `look` | Show the current location and its exits |
| `stats` | Show location, inventory and energy status |
| `help` | List available commands |
| `quit` | Exit the game |

The lake includes a `hidden` exit: use `go hidden` from that location.

## Static analysis results

### Pylint progression

The original analysis logs refer to the script as `game.py`.

| Stage | Score | Change |
| --- | ---: | ---: |
| Initial analysis | **6.25/10** | — |
| After formatting | **8.20/10** | +1.95 |
| After manual corrections | **10.00/10** | +1.80 |

Formatting resolved indentation and whitespace issues, but long lines and several code-quality findings remained. Manual corrections addressed those remaining findings.

### Main findings and corrections

| Finding | Pylint code | Correction and benefit |
| --- | --- | --- |
| Incorrect indentation | W0311 | Use consistent indentation to make block structure clear. |
| Lines longer than 100 characters | C0301 | Wrap long expressions and strings to improve readability. |
| Trailing whitespace and missing final newline | C0303, C0304 | Remove excess whitespace and add a final newline. |
| Missing module and function docstrings | C0114, C0116 | Explain the script and each function's responsibility. |
| Local `sleep` name shadowing an outer function | W0621 | Use `sleep_action` for the action and `energy_message` for display text. |
| Inconsistent return statements | R1710 | Keep return contracts consistent: predicates return `bool`; action functions return `None`. |
| Unnecessary `pass` | W0107 | Remove redundant statements. |
| Unused parameter | W0613 | Remove parameters that serve no purpose where applicable. |
| f-string without interpolation | W1309 | Use a plain string when no value is inserted. |

### Mypy

The reported result was:

```text
Success: no issues found in 1 source file
```

No initial mypy result was recorded. Therefore, this project does not claim an initial error count or a measured reduction in mypy errors.

## Refactoring

- **GameState dataclass:** replaces positional state-list access with named attributes such as `location`, `inventory` and `stamina`.
- **Independent inventories:** `field(default_factory=list)` creates a separate inventory for each game state.
- **Room TypedDict:** defines the expected types of `description`, `exits` and `items`.
- **Function annotations:** document parameter and return types so mypy can check their use.
- **Separate data and display text:** stamina remains an integer, while `energy_message` holds a string.

### Before and after

Before:

```python
def sleep_action(game_state):
    game_state[5] = 100
```

After:

```python
def sleep_action(game_state: GameState) -> None:
    """Recover your stamina"""
    game_state.stamina = 100
```

The named attribute explains what is being updated. The annotations make the expected input and return type explicit.

## Final consistency checks

The delivered revision also fixes exits pointing to nonexistent room names, recognizes both treasure items as winning items, checks inventory membership before removing an item, and handles end-of-input or keyboard interruption gracefully.

The delivered script was checked separately from the historical runs:

- **Pylint:** 10.00/10.
- **Mypy:** `Success: no issues found in 1 source file`.
- **Behavior checks:** all room exits, every possible loot outcome, independent inventories, stamina loss and recovery, both winning items, command handling, quitting and end-of-input passed.

These checks cover specific behaviors, not every possible interactive playthrough.

## Repeat the static checks

Install the analysis tools:

```bash
python -m pip install mypy pylint
```

Run them from the script's folder:

```bash
python -m mypy fishing_game.py
python -m pylint fishing_game.py
```

Results may differ with tool versions and configuration.

## Reflection

Mypy checks type consistency, while Pylint checks style, suspicious constructs and maintainability. They complement each other, but neither proves the game is correct. For example, a room destination can be a valid string and still refer to a nonexistent location. Runtime checks are necessary alongside static analysis.
