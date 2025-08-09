# osu-cli

A simple CLI tool for osu! statistics, that works locally.

## Installation

### Arch Linux

```bash
yay -S osu-cli
```

### Other distros

```bash
curl -s https://raw.githubusercontent.com/kartavkun/osufetch/main/install.sh | bash
```

## To-do

- Add support for PP info:
  - ~~PP if SS~~
  - PP if FC
  - ~~PP on failed scores~~
  - Make it more accurate
- Generate an image showing your most recent score
- Publish as an AUR package
- Set up CI/CD (possibly via a custom repo for pacman, APT, and DNF)
- Add more features based on user feedback
- ~~Integrate [osufetch](https://github.com/kartavkun/osufetch) as part of `osu-cli`~~
