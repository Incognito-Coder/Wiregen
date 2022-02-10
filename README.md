# Surfshark WireGuard
A script for generating WireGuard configs from Surfshark VPN. \
*You must have `python3` available on your machine.*

## Usage
Currently we support only Unix based systems, __Windows__ is not supported yet. \
To use the scrpt:
``` bash
python wiregen.py -u USERNAME -p PASSWORD
```
If above command doesn't work, try:
``` bash
python3 wiregen.py --user USERNAME --pass PASSWORD
```
