#   MIT No Attribution
#
#   Copyright 2023 Persune
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this
#   software and associated documentation files (the "Software"), to deal in the Software
#   without restriction, including without limitation the rights to use, copy, modify,
#   merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#   permit persons to whom the Software is furnished to do so.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#   PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#   HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#   OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#   SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import struct
import argparse

parser = argparse.ArgumentParser(description="Packs an iNES NROM file incrementally into two main binary ROM blobs, each for PRG and CHR data.")
parser.add_argument("ROM_0", help="path to input iNES NROM file 1", type=str)
parser.add_argument("ROM_1", help="path to input iNES NROM file 2", type=str)
parser.add_argument("ROM_2", help="path to input iNES NROM file 3", type=str)
parser.add_argument("ROM_3", help="path to input iNES NROM file 4", type=str)
parser.add_argument("ROM_4", help="path to input iNES NROM file 5", type=str)
parser.add_argument("ROM_5", help="path to input iNES NROM file 6", type=str)
parser.add_argument("ROM_6", help="path to input iNES NROM file 7", type=str)
parser.add_argument("ROM_7", help="path to input iNES NROM file 8", type=str)
parser.add_argument("ROM_8", help="path to input iNES NROM file 9", type=str)
parser.add_argument("ROM_9", help="path to input iNES NROM file 10", type=str)
parser.add_argument("ROM_A", help="path to input iNES NROM file 11", type=str)
parser.add_argument("ROM_B", help="path to input iNES NROM file 12", type=str)
parser.add_argument("ROM_C", help="path to input iNES NROM file 13", type=str)
parser.add_argument("ROM_D", help="path to input iNES NROM file 14", type=str)
parser.add_argument("ROM_E", help="path to input iNES NROM file 15", type=str)
parser.add_argument("ROM_F", help="path to input iNES NROM file 16", type=str)
args = parser.parse_args()

print("NROM 256 x16 ROM packer by Persune")

# read nes file
def ROMRead(ROMPath: str):
    errormsg = "Error: "
    message = "file: " + ROMPath + "\n"
    with open(ROMPath, mode="rb") as ROMFile:
        with open("MainPRG.bin", 'ab') as MainPRG:
            with open("MainCHR.bin", 'ab') as MainCHR:
                with open("NROM256x16_List.txt", "a", encoding="utf-8") as MainROMList:
                    # read header
                    ROMHeader = ROMFile.read(16)

                    # $4E $45 $53 $1A
                    if (struct.unpack("cccc", ROMHeader[:4]) != (b'\x4E', b'\x45', b'\x53', b'\x1A')):
                        errormsg += "Not a valid iNES ROM file."
                        print(errormsg)
                        return

                    # check if mapper is NROM
                    ROMMapper = ((ROMHeader[6] & 0xF0) >> 4) | (ROMHeader[7] & 0xF0)

                    if (ROMMapper != 0):
                        errormsg += " Mapper not NROM. (mapper is " + str(ROMMapper) + ")"
                        print(errormsg)
                        return

                    # read amount of PRG ROM based on header data
                    PRGSize = ROMHeader[4] * pow(2, 14)
                    message += "PRG size: " + str(PRGSize) + " bytes"

                    if (ROMHeader[4] == 1):
                        message += " (duplicated to " + str(PRGSize * 2) + ")"
                    message += "\n"

                    if (PRGSize <= 0):
                        errormsg += "PRG size is 0."
                        print(errormsg)
                        return
                    if (PRGSize > pow(2, 15)):
                        errormsg += "PRG size is bigger than 32K."
                        print(errormsg)
                        return

                    # read amount of CHR ROM based on header data
                    CHRSize = ROMHeader[5] * pow(2, 13)
                    message += "CHR size: " + str(CHRSize) + " bytes"

                    if (CHRSize<= 0):
                        message += " (no CHR ROM, padded with $FF)"
                    message += "\n"

                    if (CHRSize > pow(2, 13)):
                        errormsg += "CHR size is bigger than 8K."
                        print(errormsg)
                        return

                    ROMTrainerOffset = (ROMHeader[6] & 0x04) * 512

                    message += "Trainer offset: "+ str(ROMTrainerOffset) + " bytes"
                    ROMFile.read(ROMTrainerOffset)

                    PRGBuffer = bytearray(ROMFile.read(PRGSize))
                    if (PRGSize < pow(2, 15)):
                        # mirror PRG ROM to 32K
                        PRGBuffer.extend(PRGBuffer)
                    MainPRG.write(PRGBuffer)

                    CHRBuffer = bytearray(ROMFile.read(CHRSize))
                    if (CHRSize <= 0):
                        # pad CHR ROM to 8K with 0s
                        for bytes in range (pow(2, 13)):
                            CHRBuffer += bytearray([0xFF])
                    MainCHR.write(CHRBuffer)

                    # done
                    print(message)
                    MainROMList.writelines(ROMPath + "\n")

ROMList = (
    args.ROM_0,
    args.ROM_1,
    args.ROM_2,
    args.ROM_3,
    args.ROM_4,
    args.ROM_5,
    args.ROM_6,
    args.ROM_7,
    args.ROM_8,
    args.ROM_9,
    args.ROM_A,
    args.ROM_B,
    args.ROM_C,
    args.ROM_D,
    args.ROM_E,
    args.ROM_F)

for ROMFile in ROMList:
    ROMRead(ROMFile)
