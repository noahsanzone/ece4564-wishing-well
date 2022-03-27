import bluetooth
import pymongo
import pika
import time
import sys

if (len(sys.argv) == 3) and (sys.argv[1] == "-s"):
    raspIP = sys.argv[2]

    macADDR = '9c:b6:d0:b8:94:c8'

    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = 4
    server_sock.bind(("", port))
    server_sock.listen(1)

    client_sock, address = server_sock.accept()
    print("Accepted connection from ", address)

    data = client_sock.recv(1024)
    print("received [%s]" % data)

    client_sock.close()
    server_sock.close()

    # Establish RabbitMQ connection
    credentials = pika.PlainCredentials('admin', 'password')
    parameters = pika.ConnectionParameters(raspIP,
                                           5672,
                                           '/',
                                           credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    Place = 'Squires'
    Subject = 'Food'
    Message = 'This food sucks!'

    channel.exchange_declare(exchange=Place, exchange_type='direct')

    channel.basic_publish(exchange=Place,
                          routing_key=Subject,
                          body=Message)

    connection.close()

    # Send messages through mongoDB
    s1 = "p:Squires+Rooms “I like the comfortable chairs on 3rd floor”"
    s2 = "c:Goodwin+Rooms “John sucks”"
    s3 = "c:Goodwin+Rooms “Karthik is racist”"
    stringList = [s1, s2, s3]

    # Producer command
    connect = pymongo.MongoClient()
    for s in stringList:
        action = s[0]
        warehouse = s[2:s.find('+')]
        msgID = msgID = "{team}'$'{ticks}".format(team="14", ticks=time.time())

        # go to specified database
        db = connect[warehouse]

        collection = s[s.find('+') + 1: s.find(' ')]
        text = s[s.find(' ') + 1:]

        # create collection
        myCollection = connect[warehouse][collection]

        data = {
            "Action": action,
            "Place": warehouse,
            "MsgID": msgID,
            "Subject": collection,
            "Message": text
        }

        myCollection.insert_one(data)
else:
    print("ERROR: Invalid Input")



"""
try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("Received", data)
except OSError:
    pass
print("Disconnected.")
client_sock.close()
server_sock.close()
print("All done.")
"""