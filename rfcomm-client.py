import bluetooth
import sys

bd_addr = "9c:b6:d0:b8:94:c8"

port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

loop = True
while loop:
    keepLoop = input("Send another message? Y/N")
    if keepLoop == "N":
        break

    command = input("What message would you like to send?: ")

    sock.send(command)

sock.close()