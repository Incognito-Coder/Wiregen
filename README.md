# Surfshark WireGuard
A script for generating WireGuard configs from Surfshark VPN. \
*You must have `python3` and `wireguard-tools` available on your machine.*

## Usage
Currently we support only Unix based systems, __Windows__ is not supported yet. \
To use the script:
``` bash
python wiregen.py -u EMAIL -p PASSWORD
```
If above command doesn't work, try:
``` bash
python3 wiregen.py --user EMAIL --pass PASSWORD
```
