from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC/build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse
import json
import grpc
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc
import paho.mqtt.client as mqtt
# Create your views here.

class FibView(APIView):
	permission_classes = (permissions.AllowAny,)

	def __init__(self):
		self.client = mqtt.Client()
		self.client.connect(host="localhost",port=1883)	

	def post(self, request):
		host = "localhost:8080"
		print(host)
		with grpc.insecure_channel(host) as channel:
			stub = fib_pb2_grpc.FibCalculatorStub(channel)
			fibrequest = fib_pb2.FibRequest()
			fibrequest.order = json.loads(request.body)["order"]
			response = stub.Compute(fibrequest)
			print(response.value)
			self.client.publish(topic='log', payload=json.loads(request.body)["order"])
		return Response(data={"fib":response.value}, status=200)

class LogView(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		host = "localhost:8090"
		print(host)
		with grpc.insecure_channel(host) as channel:
			stub = log_pb2_grpc.LogStub(channel)
			logrequest = log_pb2.LogRequest()
			response = stub.Get(logrequest)
			print(response.data)
		return Response(data={"log":response.data[:]}, status=200)
