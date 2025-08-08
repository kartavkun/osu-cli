import argparse
from osucli.fetch import fetch_user_data
from osucli.rs import recent_score_data  # на будущее

def main():
    parser = argparse.ArgumentParser(description="osu! CLI tool")
    parser.add_argument("--fetch", metavar="USER", help="Show profile info for USER (ID or username)")
    parser.add_argument("--rs", action="store_true", help="Show recent score")  # для будущего

    args = parser.parse_args()

    if args.fetch:
        fetch_user_data(args.fetch)  # Передаем никнейм или ID
    elif args.rs:
        recent_score_data()
    else:
        parser.print_help()
