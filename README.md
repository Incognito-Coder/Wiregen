# Surfshark WireGuard
A script for generating WireGuard configs from Surfshark VPN. \
*You must have `python3` and `wireguard-tools` available on your machine.*
## Usage
Compatible with : __Linux , Darwin , Windows__.
### System-Wide
``` bash
sudo ./installer.sh
```
#### ArchLinux
Now Wiregen available in [AUR](https://aur.archlinux.org/)
``` bash
yay -S surfshark-wireguard
```

now you can use `wiregen` anywhere on your computer.
### Portable
To use the script:
``` bash
python wiregen.py -u EMAIL -p PASSWORD
```
If above command doesn't work, try:
``` bash
python3 wiregen.py --user EMAIL --pass PASSWORD
```
Also we have Terminal user interface. \
Simply run python file. \
![Screenshot](https://raw.githubusercontent.com/Incognito-Coder/Wiregen/master/img/main.png "Application")
# Credits
Developer : Incognito Coder \
if you enjoy my content, consider to buy me a coffee here:
1. Donate [ZarinPal](https://zarinp.al/@incognito)