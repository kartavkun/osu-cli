#!/bin/bash

set -e

REPO="kartavkun/osu-cli"
BIN_NAME="osu-cli"
INSTALL_DIR="/usr/local/bin"

# Если нет root — ставим в ~/.local/bin
if [ "$EUID" -ne 0 ]; then
  INSTALL_DIR="$HOME/.local/bin"
  mkdir -p "$INSTALL_DIR"
fi

echo "📦 Installing $BIN_NAME latest release to $INSTALL_DIR..."

# Получаем последнюю версию
# TAG=$(curl -s "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name":' | cut -d '"' -f 4)

# if [ -z "$TAG" ]; then
# echo "❌ Failed to get latest release tag from GitHub"
# exit 1
# fi

# Формируем URL
# BIN_URL="https://github.com/${REPO}/releases/download/${TAG}/${BIN_NAME}"
BIN_URL="https://github.com/${REPO}/releases/download/v0.1/${BIN_NAME}"

# Качаем бинарник во временную директорию
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "⬇️  Downloading $BIN_NAME version $TAG..."
curl -fL "$BIN_URL" -o "$TMP_DIR/$BIN_NAME"

chmod +x "$TMP_DIR/$BIN_NAME"

# Перемещаем в $INSTALL_DIR
echo "⬆️  Installing to $INSTALL_DIR..."
mv "$TMP_DIR/$BIN_NAME" "$INSTALL_DIR/$BIN_NAME"

# Функция для создания алиасов-скриптов с передачей аргументов
install_alias() {
  local name=$1
  local cmd=$2
  echo "#!/bin/bash
$cmd \"\$@\"
" >"$INSTALL_DIR/$name"
  chmod +x "$INSTALL_DIR/$name"
}

echo "🔗 Creating launcher scripts..."
install_alias rs "$HOME/.local/bin/$BIN_NAME --rs"
install_alias osufetch "$HOME/.local/bin/$BIN_NAME --fetch"

echo "✅ $BIN_NAME installed successfully!"
echo "👉 You can now run '$BIN_NAME', 'rs' or 'osufetch' from your terminal."
