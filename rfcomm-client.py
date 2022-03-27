import bluetooth
import sys

bd_addr = "9c:b6:d0:b8:94:c8"

port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

command = input("What message would you like to send?: ")

while command:
    #keepLoop = input("Send another message? Y/N: ")
    # if keepLoop == "N":
    #     loop = False
    #     break
    #
    # command = input("What message would you like to send?: ")

    sock.send(command)
    command = input("What message would you like to send?: ")

sock.close()
