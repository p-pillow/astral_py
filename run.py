import argparse

from Objects import Game, Player, Team, Localization

"""Script for easy running of Astral.
"""

def parse_args() -> argparse.Namespace:
    """Parse arguments of run.py and returns a namespace.

    Returns:
        argparse.Namespace: Arguments of the script.
    """
    parser = argparse.ArgumentParser()

    return parser.parse_args()

def main() -> None:
    """Main function.
    """
    # args = parse_args()
    game = Game(teams=(Team("1", Player("lol")), Team("2", Player("kek"))), rounds=2, messages=Localization.RUS_TEXTS)
    game.run()

if __name__ == "__main__":
    main()
