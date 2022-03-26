import bluetooth
import pymongo
import pika
import time
import sys

if (len(sys.argv) == 3) and (sys.argv[1] == "-s"):
    raspIP = sys.argv[2]

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


macADDR = '9c:b6:d0:b8:94:c8'


# bluetooth connection
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "E106A78C-63F2-11E8-A4C3-9829A6584161"
bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )
print("Waiting for connection on RFCOMM channel", port)
client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)
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