#!/usr/bin/python3
"""
A simple JSON based REST API to 
 -register a user
 -validate authentication from mongodb
 -add a record in the db
 -update a record in the db
 - allows adding upto 5 sentences per user


"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://127.0.0.1:27017")
# create a new db
db = client.Messages
# Create a collection
users = db["Users"]


def verifyUser(username, password):
    
    db_pw_check = users.find({
        "Username": username
    })[0]["Password"]
    hashed_pw = bcrypt.hashpw(password.encode('utf8'), db_pw_check)
    if not db_pw_check:
        print ("User not found " + username)
        return False
    elif hashed_pw == db_pw_check:
        return True
    else:
        print("Password did not match " + str(hashed_pw) + " db = " + str(db_pw_check))
        return False

def userExists(username):
    user_check =  users.find_one({
        "Username" : username
        })
    
    if not user_check:
        return False
    else:
        return True

def countTokens(username):
    db_count = users.find({
        "Username": username
    })[0]["Tokens"]

    if not db_count:
        return -1
    else:
        print ("User " + username + " has " + str(db_count) + " tokens")
        return int(db_count)


class Register(Resource):
    def post(self):
        postedData = request.get_json()
        #print (json.dumps(postedData))
        # get the user pass
        username = postedData["Username"]
        password = postedData["Password"]
        if userExists(username):
            retJson = {
            "status": 201,
            "msg": "user already exists"
            }
            return jsonify(retJson)

        # hash the password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #store in db
        print ("Adding user " + username + " password " + str(hashed_pw))
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": [],
            "Tokens": 5
        })
        # return code
        retJson = {
            "status": 200,
            "msg": "user has been registered"
        }
        return jsonify(retJson)


class Store(Resource):
    def post(self):
        postedData = request.get_json()
        # get the user pass
        username = postedData["Username"]
        password = postedData["Password"]
        sentence = postedData["Sentence"]

        # validate user
        user_validated = verifyUser(username, password)
        # token check
        num_tokens = countTokens(username)
        if not user_validated:
            retJson = {
                "status": 302,
                "msg": "Incorrect userid or password"
            }
            return jsonify(retJson)
        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "msg": "Not enough tokens left. Token count = " + str(num_tokens)
            }
            return jsonify(retJson)
        # update the user in the database
        
        print ("Updating user " + username + " token = " + str(num_tokens))
        users.update(
            {"Username": username},
            {"$set":
             {
              "Tokens": num_tokens -1
              },
              "$push": {
                "Sentence": sentence
              }
             }
        )
        retJson = {
            "status": 200,
            "msg": "Sentence saved successfully, tokens left =  " + str(num_tokens)
        }
        return jsonify(retJson)

class Retreive(Resource):
    def post(self):
        postedData = request.get_json()
        # get the user pass
        username = postedData["Username"]
        password = postedData["Password"]
        # validate user
        user_validated = verifyUser(username, password)
        if not user_validated:
            retJson = {
                "status": 302,
                "msg": "Incorrect userid or password"
            }
            return jsonify(retJson)
        sentences = users.find({
            "Username": username
            })[0]["Sentence"]
        retJson = {
                "status": 200,
                "msg": str(sentences)
            }
        return jsonify(retJson)

class Delete(Resource):
    def post(self):
        postedData = request.get_json()
        # get the user pass
        username = postedData["Username"]
        password = postedData["Password"]
        # validate user
        user_validated = verifyUser(username, password)
        if not user_validated:
            retJson = {
                "status": 302,
                "msg": "Incorrect userid or password"
            }
            return jsonify(retJson)
        users.update({
            "Username": username
            }, 
                {"$set": 
                    {
                        "Sentence": [],
                        "Tokens": 5
                    }
                }
            )

        retJson = {
                "status": 200,
                "msg": "Deleted all sentences and reset Tokens to default"
            }
        return jsonify(retJson)

@app.route('/')
def hello_world():
    return "Simple API. /, /register, /store, /get, /delete"


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Retreive, '/get')
api.add_resource(Delete, '/delete')


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(host='127.0.0.1', port=5000)
