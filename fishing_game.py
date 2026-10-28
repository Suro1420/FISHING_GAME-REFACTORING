
"""
A small text-based fishing adventure game.

Explore different locations, collect items, manage your stamina,
and discover the legendary treasure.
"""

import random
from dataclasses import dataclass, field
from typing import TypedDict


TREASURE_CHEST = (
    "Treasure Chest you finished the game you are the GOAT of all fishermans"
)
NOTHING = "Nothing... try again"
MAX_STAMINA = 100


class Room(TypedDict):
    """Store the properties of a room."""

    description: str
    exits: dict[str, str]
    items: list[str]


@dataclass
class GameState:
    """Store the mutable state of the game."""

    location: str = "Beginner river"
    score: int = 0
    inventory: list[str] = field(default_factory=list)
    should_quit: bool = False
    stamina: int = MAX_STAMINA


# Game world - rooms and their properties
rooms: dict[str, Room] = {
    "Beginner river": {
        "description": "The river near the town of promising fishermen.",
        "exits": {
            "north": "Cave lake",
            "east": "Village swimming pool",
            "south": "lake",
        },
        "items": [
            "Normal Fish ! Continue like that !",
            NOTHING,
            "A rock... Useless",
            "Normal Fish ! Continue like that !",
            NOTHING,
            "A rock... Useless",
            'An old paper with "Hidden in the south..."',
        ],
    },
    "Cave lake": {
        "description": "A cave with a lake inside. You feel a mysterious atmosphere.",
        "exits": {
            "south": "Beginner river",
            "east": "Sacred River of the Mountain",
        },
        "items": [
            NOTHING,
            "Golden shining coin ! Congratulations, you are rich!",
            NOTHING,
            NOTHING,
            NOTHING,
            NOTHING,
        ],
    },
    "Village swimming pool": {
        "description": "The swimming pool of the village.",
        "exits": {
            "west": "Beginner river",
            "north": "Sacred River of the Mountain",
        },
        "items": ["bread", "map"],
    },
    "Sacred River of the Mountain": {
        "description": "You stand atop a high mountain. The view is breathtaking!",
        "exits": {
            "west": "Cave lake",
            "south": "Village swimming pool",
        },
        "items": ["old_treasure_chest"],
    },
    "lake": {
        "description": "A serene lake with crystal-clear water. Fish swim peacefully below.",
        "exits": {
            "north": "Beginner river",
            "hidden": "Legendary Water Well",
        },
        "items": ["fishing_rod", "fish"],
    },
    "Legendary Water Well": {
        "description": (
            "... The fishing rod in your hands begins to shine... "
            "You are the chosen one!"
        ),
        "exits": {
            "north": "Beginner river",
            "south": "Beginner river",
            "west": "Beginner river",
            "east": "Beginner river",
        },
        "items": [
            "Golden shining Fish You feel the power of the Legendary FISHING ROD",
            "Diamond of wisdom the most expensive object of all times",
            TREASURE_CHEST,
        ],
    },
}


def validate_rooms() -> None:
    """Check that all room exits lead to existing locations."""
    for room_name, room in rooms.items():
        if not room["items"]:
            raise ValueError(f"Room '{room_name}' has no items.")

        for destination in room["exits"].values():
            if destination not in rooms:
                raise ValueError(
                    f"Invalid destination '{destination}' in room '{room_name}'."
                )


def display_location(player_location: str) -> None:
    """Display the current location and available exits."""
    current_room = rooms[player_location]

    print("\n" + "=" * 50)
    print(f"LOCATION: {player_location.upper()}")
    print("=" * 50)
    print(current_room["description"])

    exits = current_room["exits"]
    print(f"\nExits: {', '.join(exits)}")


def move_player(direction: str, game_state: GameState) -> None:
    """Move the player if the chosen direction is available."""
    current_room = rooms[game_state.location]
    destination = current_room["exits"].get(direction)

    if destination is None:
        print("You cannot go in that direction.")
        return

    game_state.location = destination
    print(f"You're going to the {direction}.")


def fishing(game_state: GameState) -> None:
    """Catch a random item and consume stamina."""
    current_room = rooms[game_state.location]
    available_items = current_room["items"]

    loot = random.choice(available_items)
    stamina_cost = random.randint(1, 15)

    game_state.stamina = max(0, game_state.stamina - stamina_cost)

    if loot != NOTHING:
        game_state.inventory.append(loot)
        game_state.score += 1

    print(loot)


def check_win_condition(game_state: GameState) -> bool:
    """Return whether the player has collected the legendary treasure."""
    return TREASURE_CHEST in game_state.inventory


def display_stats(game_state: GameState) -> None:
    """Display the player's current statistics."""
    stamina = game_state.stamina

    if stamina <= 10:
        stamina_description = "Exhausted"
    elif stamina <= 20:
        stamina_description = "Very tired"
    elif stamina <= 30:
        stamina_description = "Sleepy"
    elif stamina <= 50:
        stamina_description = "A little tired"
    elif stamina <= 80:
        stamina_description = "Feeling good"
    else:
        stamina_description = "Full of energy"

    print(
        f"Current location: {game_state.location}",
        f"Player items: {game_state.inventory}",
        f"Score: {game_state.score}",
        f"Energy: {stamina}/{MAX_STAMINA} ({stamina_description})",
        sep="\n",
    )


def sleep_action(game_state: GameState) -> None:
    """Restore the player's stamina."""
    game_state.stamina = MAX_STAMINA
    print("ZzZZzzzzzzzZZz...")


def show_diary(player_inventory: list[str]) -> None:
    """Display the player's fishing history."""
    print(f"You're opening your fishing diary: {player_inventory}")


def use_item(item_name: str, game_state: GameState) -> None:
    """Remove an item from the player's inventory."""
    if item_name not in game_state.inventory:
        print(f"You don't have '{item_name}' in your inventory.")
        return

    game_state.inventory.remove(item_name)
    print(f"You used {item_name}... You will never forget it. RIP!")


def check_lose_condition(game_state: GameState) -> bool:
    """Return whether the player has run out of stamina."""
    return game_state.stamina <= 0


def show_help() -> None:
    """Display available commands."""
    print("\n=== AVAILABLE COMMANDS ===")
    print("go <direction>     - Move in a direction")
    print("fishing            - Try to catch something")
    print("diary              - Show your items")
    print("use <item>         - Use an inventory item")
    print("sleep              - Recover your energy")
    print("look               - Look around your current location")
    print("stats              - Check your stats")
    print("help               - Show this help message")
    print("quit               - Exit the game")


def process_command(command: str, game_state: GameState) -> None:
    """Read and execute a player command."""
    parts = command.strip().split(maxsplit=1)

    if not parts:
        return
    action = parts[0].lower()
    argument = parts[1].strip() if len(parts) > 1 else ""

    match action:
        case "go":
            if argument:
                move_player(argument.lower(), game_state)
            else:
                print("Usage: go <direction>")

        case "fishing":
            fishing(game_state)

        case "diary":
            show_diary(game_state.inventory)

        case "use":
            if argument:
                use_item(argument, game_state)
            else:
                print("Usage: use <item>")

        case "look":
            display_location(game_state.location)

        case "stats":
            display_stats(game_state)

        case "sleep":
            sleep_action(game_state)

        case "help":
            show_help()

        case "quit":
            print("\nThanks for playing!")
            game_state.should_quit = True

        case _:
            print(
                "\nI don't understand that command. "
                "Type 'help' for available commands."
            )


def main() -> None:
    """Initialize the game and run the main event loop."""
    validate_rooms()

    game_state = GameState()

    print("=" * 60)
    print("         WELCOME TO THE ADVENTURE GAME!")
    print("=" * 60)
    print("\nYour goal is to explore the world and find the treasure!")
    print("Type 'help' at any time to see available commands.")

    display_location(game_state.location)

    while not game_state.should_quit:
        try:
            command = input("\n> What do you want to do? ")
        except (EOFError, KeyboardInterrupt):
            print("\nThanks for playing!")
            break

        process_command(command, game_state)

        if game_state.should_quit:
            break

        if check_win_condition(game_state):
            print("\n🎉 CONGRATULATIONS! YOU WON! 🎉")
            print("You became the best and completed your adventure!")
            break

        if check_lose_condition(game_state):
            print("\n💀 GAME OVER 💀")
            print("You overworked yourself...")
            break

    print("\n" + "=" * 50)
    print(f"Final Score: {game_state.score}")
    print(f"Items Collected: {len(game_state.inventory)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
