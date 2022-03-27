import bluetooth
import pymongo
import pika
import time
import sys


def callback(ch, method, properties, body):
    print("%r:%r" % (method.routing_key, body))


if (len(sys.argv) == 3) and (sys.argv[1] == "-s"):
    raspIP = sys.argv[2]

    # Establish bluetooth connection
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 4
    server_sock.bind(("", port))
    server_sock.listen(1)

    # Establish RabbitMQ connection
    credentials = pika.PlainCredentials('admin', 'password')
    parameters = pika.ConnectionParameters(raspIP,
                                           5672,
                                           '/',
                                           credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Establish MongoDB connection
    connect = pymongo.MongoClient()

    while True:
        print("Waiting for connection on RFCOMM channel", port)
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from", client_info)
        while True:
            # Message from bluetooth connection
            s = client_sock.recv(1024)
            print("received [%s]" % data)
            if not s:
                break
            action = s[0]

            # Check and perform valid action and send to mongoDB
            if action == 'p' or action == 'c':
                warehouse = s[2:s.find('+')]
                collection = s[s.find('+') + 1: s.find(' ')]
                text = s[s.find(' ') + 1:]
                msgID = msgID = "{team}'$'{ticks}".format(team="14", ticks=time.time())

                # go to specified database
                db = connect[warehouse]

                # create collection and send to MongoDB
                myCollection = connect[warehouse][collection]
                data = {
                    "Action": action,
                    "Place": warehouse,
                    "MsgID": msgID,
                    "Subject": collection,
                    "Message": text
                }
                myCollection.insert_one(data)

                if action == 'p':
                    channel.exchange_declare(exchange=warehouse,
                                             exchange_type='direct')

                    channel.basic_publish(exchange=warehouse,
                                          routing_key=collection,
                                          body=text)
                else:
                    channel.queue_bind(exchange=warehouse,
                                       queue=collection,
                                       routing_key=collection)

                    channel.basic_consume(callback,
                                          queue=collection,
                                          no_ack=True)

                    channel.start_consuming()
            else:
                print('ERROR: Incorrect Action')
else:
    print("ERROR: Invalid Input")