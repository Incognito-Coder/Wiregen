platform=$(uname)
if [ "$platform" = "Linux" ]; then
    install_path="/usr/bin/wiregen"
fi
if [ "$platform" = "Darwin" ]; then
    install_path="/usr/local/bin/wiregen"
fi
echo "Installing to System"
cp wiregen.py "$install_path"
chmod +x "$install_path"
echo "Installed."
echo "Type wiregen to start"
