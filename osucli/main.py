import argparse
from osucli.fetch import fetch_user_data
from osucli.rs import print_score_data  # на будущее

def main():
    parser = argparse.ArgumentParser(description="osu! CLI tool")
    parser.add_argument("--fetch", action="store_true", help="Show profile info")
    parser.add_argument("--rs", action="store_true", help="Show recent score")
    parser.add_argument("user", nargs="?", default=None, help="User ID or nickname (optional)")
    parser.add_argument("-v", "--version", action="version", version=f"v0.2")

    args = parser.parse_args()

    if args.fetch:
        fetch_user_data(args.user)  # Передаем None или ник/ID
    elif args.rs:
        print_score_data()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
