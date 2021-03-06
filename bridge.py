import bluetooth
import pymongo
import pika
import time
import sys


def callback(ch, method, properties, body):
    getQueue.method.message_count -= 1
    print("%r:%r" % (method.routing_key, body))
    #print("Message Count:", getQueue.method.message_count)
    if getQueue.method.message_count == 0:
        channel.stop_consuming()


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

    dbnames = connect.list_database_names()

    while True:
        print("Waiting for connection on RFCOMM channel", port)
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from", client_info)
        while True:
            # Message from bluetooth connection
            s = client_sock.recv(1024).decode()
            if not s:
                break
            action = s[0]

            #use try except
                #if it is a keyboard then sys.exit()

            # Check and perform valid action and send to mongoDB
            if action == 'p' or action == 'c':
                warehouse = s[2:s.find('+')]
                msgID = msgID = "{team}'$'{ticks}".format(team="14", ticks=time.time())
                if action == 'p':
                    collection = s[s.find('+') + 1: s.find(' ')]
                    text = s[s.find(' ') + 1:]
                else:
                    collection = s[s.find('+') + 1:]
                    text = ""
                print("[Checkpoint 01 Timestamp] Message Captured: ", text)

                if warehouse in dbnames:
                    # go to specified database
                    db = connect[warehouse]

                    colNames = db.list_collection_names()
                    print("colNames:", colNames)
                    if collection in colNames:
                        # create collection and send to MongoDB
                        myCollection = connect[warehouse][collection]
                        data = {
                            "Action": action,
                            "Place": warehouse,
                            "MsgID": msgID,
                            "Subject": collection,
                            "Message": text
                        }

                        print("[Checkpoint 02 Timestamp] Store command in MongoDB instance: ", data)
                        myCollection.insert_one(data)
                        print("[Checkpoint 03 Timestamp] Print out RabbitMQ command sent to the Repository RPi: ", s)

                        if action == 'p':
                            channel.basic_publish(exchange=warehouse,
                                                  routing_key=collection,
                                                  body=text)
                            print("[Checkpoint 04 Timestamp] Bridge Laptop prints statements generated by the RabbitMQ "
                                  "instance: ", "")
                        else:
                            getQueue = channel.queue_declare(queue=collection,
                                                             passive=True)

                            channel.queue_bind(exchange=warehouse,
                                               queue=collection,
                                               routing_key=collection)

                            print("[Checkpoint 04 Timestamp] Bridge Laptop prints statements generated by the RabbitMQ "
                                  "instance: ")
                            channel.basic_consume(queue=collection,
                                                  on_message_callback=callback,
                                                  auto_ack=True)

                            channel.start_consuming()
                    else:
                        print("ERROR: Invalid Collection")
                else:
                    print("ERROR: Invalid Database")
            else:
                print('ERROR: Incorrect Action')
else:
    print("ERROR: Invalid Input")