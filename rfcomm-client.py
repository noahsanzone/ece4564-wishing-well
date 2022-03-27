import bluetooth

bd_addr = "9c:b6:d0:b8:94:c8"

port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()