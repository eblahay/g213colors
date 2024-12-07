# G213Colors (eblahay Fork)

A Python script to change the key colors on a Logitech G213 Prodigy Gaming Keyboard.

Forked from: SebiTimeWaster's [G213Colors](https://github.com/SebiTimeWaster/G213Colors).

## Installation
### Dependencies

* [Python](https://www.python.org/) >= 2.4 or 3.x (which is usually already installed)
* [PyUSB](https://github.com/walac/pyusb)

If you intend to run the script as root, 
then you'll need to install the dependencies system-wide (e.g. `sudo pip3 install pyusb`).

### Installation

1) copy the file `g213colors.py` to `/usr/local/bin/`
    * e.g. `sudo cp g213colors.py /usr/local/bin/g213colors`
2) change the copy's permissions
    * e.g. `sudo chmod 755 /usr/local/bin/g213colors`
3) Profit!


## Changelog

0.1.0 (WIP):
* removed random colors feature from pre-fork v0.3
    * subsequently removed dependency on randomcolors library
* defined main() method
* switched to using Python argparse library for parsing CLI args
* added Python 3 shebang: `#! /usr/bin/env python3`
* renamed script to `g213colors.py` for ease of use in CLI
* added support for abbreviated color-codes in CLI arguments
    * e.g. `-c fe0` is equivalent to `-c ffee00`

Forked from [G213Colors](https://github.com/SebiTimeWaster/G213Colors) v0.3

## Licensing

* G213Colors (eblahay Fork): [GPLv3](LICENSE.md)
    * This applies to all of the changes made in this project after having been forked from G213Colors v0.3.
* G213Colors v0.3: [MIT License](G213Colors_LICENSE.txt)
    * This is the license of the original G213Colors (v0.3) which this project was forked from. The code inherited from that project is still subject to its original license, rather than the GPL used by this fork.