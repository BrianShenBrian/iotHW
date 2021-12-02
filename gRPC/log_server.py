import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc
import paho.mqtt.client as mqtt

import threading

logging=list()

def on_message(client, obj, msg):
    logging.append(int(msg.payload))
    print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")
    print(logging)

def subscribe():
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host="localhost", port=1883)
    client.subscribe('log', 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass

class LogServicer(log_pb2_grpc.LogServicer):

    def __init__(self):
        pass

    def Get(self, request, context):
        response = log_pb2.LogResponse()
        for i in logging:
            response.data.append(i)

        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8090, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LogServicer()
    log_pb2_grpc.add_LogServicer_to_server(servicer, server)
    t = threading.Thread(target = subscribe)
    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        t.start()
        server.start()
        print(f"Run gRPC log Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass


