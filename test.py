#!/usr/bin/python3
# Test script to validate responses from our Flask Restful API
import requests 
import json

API_ENDPOINT = "http://127.0.0.1:5000/"
# Register
method_url = API_ENDPOINT + 'register'
headers = {'content-type': 'application/json'}
test_data = {
	"Username": "user1",
	"Password": "password123"
}
#print (json.dumps(test_data))
r = requests.post(url = method_url, data = json.dumps(test_data),headers=headers) 
  
# extracting response text  
if '200' in r.text:
	print("Passed")
else:
	print("Failed " + r.text)
#  Store
method_url = API_ENDPOINT + 'store'
headers = {'content-type': 'application/json'}
test_data = {
	"Username": "user1",
	"Password": "password123",
	"Sentence": "Message 1"
}
#print (json.dumps(test_data))
r = requests.post(url = method_url, data = json.dumps(test_data),headers=headers) 
  
# extracting response text  
if '200' in r.text:
	print("Passed " + r.text)
else:
	print("Failed " + r.text)

#  Get/retrieve
method_url = API_ENDPOINT + 'get'
headers = {'content-type': 'application/json'}
test_data = {
	"Username": "user1",
	"Password": "password123"
}
#print (json.dumps(test_data))
r = requests.post(url = method_url, data = json.dumps(test_data),headers=headers) 
  
# extracting response text  
if '200' in r.text:
	print("Passed " + r.text)
else:
	print("Failed " + r.text)
#  Delete
method_url = API_ENDPOINT + 'delete'
headers = {'content-type': 'application/json'}
test_data = {
	"Username": "user1",
	"Password": "password123"
}
#print (json.dumps(test_data))
r = requests.post(url = method_url, data = json.dumps(test_data),headers=headers) 
  
# extracting response text  
if '200' in r.text:
	print("Passed " + r.text)
else:
	print("Failed " + r.text)