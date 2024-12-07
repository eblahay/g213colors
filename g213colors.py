#! /usr/bin/env python3

'''
    G213Colors (eblahay Fork)
    Copyright (C) 2024  Ethan Blahay

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
'''
  *  The MIT License (MIT)
  *
  *  G213Colors v0.3 Copyright (c) 2016, 2017, 2018 SebiTimeWaster
  *
  *  Permission is hereby granted, free of charge, to any person obtaining a copy
  *  of this software and associated documentation files (the "Software"), to deal
  *  in the Software without restriction, including without limitation the rights
  *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  *  copies of the Software, and to permit persons to whom the Software is
  *  furnished to do so, subject to the following conditions:
  *
  *  The above copyright notice and this permission notice shall be included in all
  *  copies or substantial portions of the Software.
  *
  *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  *  SOFTWARE.
'''


import sys
import usb.core
import usb.util
import binascii
from argparse import ArgumentParser

idVendor         = 0x046d           # The id of the Logitech company
idProduct        = 0xc336           # The id of the G213
bEndpointAddress = 0x82             # Endpoint to read data back from
bmRequestType    = 0x21             # --.
bmRequest        = 0x09             #    \ The controll transfer
wValue           = 0x0211           #    / configuration for the G213
wIndex           = 0x0001           # --'
colorCommand     = '11ff0c3a{}01{}0200000000000000000000'   # binary commands in hex format, always 20 byte long
breatheCommand   = '11ff0c3a0002{}{}006400000000000000'
cycleCommand     = '11ff0c3a0003ffffff0000{}64000000000000'
device           = ''               # device resource
isDetached       = False            # If kernel driver needs to be reattached

# Backend

def connectG():
    global device, isDetached
    # find G product
    device = usb.core.find(idVendor = idVendor, idProduct = idProduct)
    # if not found exit
    if device is None:
        print('USB device not found!')
        sys.exit(1)
    # if a kernel driver is attached to the interface detach it, otherwise no data can be send
    if device.is_kernel_driver_active(wIndex):
        device.detach_kernel_driver(wIndex)
        isDetached = True

def disconnectG():
    # free device resource to be able to reattach kernel driver
    usb.util.dispose_resources(device)
    # reattach kernel driver, otherwise special keys will not work
    if isDetached:
        device.attach_kernel_driver(wIndex)

def checkColorHex(colorHex):
    try:
        if len(colorHex) != 6:
            raise ValueError()
        int(colorHex, 16)
    except:
        pass
        print('Not a valid hexadecimal color!')
        return False
    return True

def checkSpeedNum(numStr):
    try:
        num = int(numStr)
        if num < 32 or num > 65535:
            raise ValueError()
    except:
        pass
        print('Not a valid time in milliseconds!')
        return False
    return True

def sendData(dataHex):
    # convert hex data to binary and send it
    device.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(dataHex))
    # read back one 20-byte word, otherwise commands may not be completely executed
    device.read(bEndpointAddress, 20)

def sendColorCommand(colorHex, field = 0):
    if checkColorHex(colorHex):
        # convert number to hex
        fieldHex = format(field, '02x')
        commandHex = colorCommand.format(fieldHex, colorHex)
        sendData(commandHex)

def sendBreatheCommand(colorHex, speed):
    if checkColorHex(colorHex) and checkSpeedNum(speed):
        # convert number to hex
        speedHex = format(int(speed), '04x')
        commandHex = breatheCommand.format(colorHex, speedHex)
        sendData(commandHex)

def sendCycleCommand(speed):
    if checkSpeedNum(speed):
        # convert number to hex
        speedHex = format(int(speed), '04x')
        commandHex = cycleCommand.format(speedHex)
        sendData(commandHex)

# Frontend

def convColorCode(code):
    """ 
        translates more User-Friendly colors codes into 
        the format expected by the backend
    """

    # handle case-sensitivity
    code = code.lower()

    # handle abbreviated codes
    if len(code) == 3:
        code = code[0] + code[0] + code[1] + code[1] + code[2] + code[2]

    return code


def main():
    # parse arguments
    parser = ArgumentParser(
        epilog="""
            Please Note:
                COLOR is a hexadecimal code in the format, 'RRGGBB'.
                i.e. ff0000 is red, 00ff00 is green and so on.
                Alternatively, COLOR can be an abbreviated format, 'RGB',
                which will be expanded by duplicating each hexadigit of the code.
                i.e. 'f0a' -> 'ff00aa'.
                Color-Codes are also Case-Insensitive.
        """
    )

    parser.add_argument(
        "--version",
        version="G213Colors (eblahay Fork) 0.1.0-dev",
        action="version"
    )

    parser.add_argument(
        '-c', '--colors',
        help='sets the color(s) to be used on the keyboard; supports 1 OR 5 specified colors',
        nargs='+',
        default=['ffb4aa'],
        metavar='COLOR'
    )

    parser.add_argument(
        '-b', '--breathe',
        help='sets a color breathing animation (in milliseconds, 32—65535)',
        type=int,
        metavar='TIME'
    )

    parser.add_argument(
        '-x', '--cycle',
        help='sets a color cycling animation (in milliseconds, 32—65535)',
        type=int,
        metavar='TIME'
    )

    args = parser.parse_args()

    # END: parse args

    connectG() # reqs sudo privs

    if args.cycle != None:
        sendCycleCommand(args.cycle)
    elif args.breathe != None:
        if len(args.colors) > 1:
            print("ERROR: Breathing Animation can ONLY be used with a SINGLE COLOR!")
        else:
            sendBreatheCommand(convColorCode(args.colors[0]), args.breathe)
    else:
        if len(args.colors) == 1:
            sendColorCommand(convColorCode(args.colors[0]))
        elif len(args.colors) == 5:
            for i in range(0, 5):
                sendColorCommand(convColorCode(args.colors[i]), i + 1)
        else:
            print(
                'ERROR: Either 1 OR 5 colors must be specified!\n',
                'i.e.\n',
                '\t-c COLOR\n',
                '\t-c COLOR COLOR COLOR COLOR COLOR\n'
            )
        

    disconnectG()

if __name__ == "__main__":
    main()
