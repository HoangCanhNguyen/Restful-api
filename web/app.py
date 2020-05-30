from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import hashlib

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Token": 5
        })

        retJson = {
            "status": 200,
            "msg": "Success to sign up"
        }

        return jsonify(retJson)


def verifyPw(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Token"]
    return tokens


class Store(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "password is wrong"
            }
            return jsonify(retJson)
        enough_tokens = countTokens(username)
        if not enough_tokens:
            retJson = {
                "status": 302,
                "msg": "not enough tokens"
            }
            return jsonify(retJson)
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "msg": "Not enough tokens"
            }
            return jsonify(retJson)
        users.update({
            "Username": username
        }, {
            "$set": {
                "Sentence": sentence,
                "Tokens": num_tokens-1
            }
        })
        retJson = {
            "status": 200,
            "msg": "Sentence saved successful"
        }
        return jsonify(retJson)


class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "password is wrong"
            }
            return jsonify(retJson)
        enough_tokens = countTokens(username)
        if not enough_tokens:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "msg": "Not enough tokens"
            }
            return jsonify(retJson)
        sentence = users.find({
            "Username": username
        })[0]["Sentence"]
        retJson = {
            "status": 200,
            "sentence": sentence
        }
        return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


if __name__ == "__main__":
    app.run(host='0.0.0.0')

# from flask import Flask, jsonify, request  # import Flask constructor
# from flask_restful import Api, Resource

# from pymongo import MongoClient

# app = Flask(__name__)
# api = Api(app)

# client = MongoClient("mongodb://db:27017")
# db = client.aNewDB
# UserNum = db["UserNum"]

# UserNum.insert({
#     'num_of_users':0
# })

# class Visit(Resource):
#     def get(self):
#         prev_num = UserNum.find({})[0]['num_of_users']
#         new_num = prev_num + 1
#         UserNum.update({}, {"$set":{"num_of_users":new_num}})
#         return str("Hello user " + str(new_num))

# def checkPostedData(postedData, functionName):
#     if (functionName == "add" or functionName =="subtract" or functionName == "multiply"):
#         if ("x" not in postedData or "y" not in postedData):
#             return 301
#         else:
#             return 200
#     elif (functionName == "divide"):
#         if ("x" not in postedData or "y" not in postedData):
#             return 301
#         elif postedData["y"] == 0:
#             return 302
#         else:
#             return 200


# class Add(Resource):
#     def post(self):
#         postedData = request.get_json()

#         status_code = checkPostedData(postedData, "add")
#         if (status_code != 200):
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code": status_code
#             }
#             return jsonify(retJson)

#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)
#         ret = x+y
#         retMap = {
#             'Message': ret,
#             'Status code': 200
#         }
#         return jsonify(retMap)


# class Subtract(Resource):
#     def post(self):
#         postedData = request.get_json()

#         status_code = checkPostedData(postedData, "subtract")
#         if (status_code != 200):
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code": status_code
#             }
#             return jsonify(retJson)

#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)
#         ret = x-y
#         retMap = {
#             'Message': ret,
#             'Status code': 200
#         }
#         return jsonify(retMap)


# class Multiply(Resource):
#     def post(self):
#         postedData = request.get_json()

#         status_code = checkPostedData(postedData, "multiply")
#         if (status_code != 200):
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code": status_code
#             }
#             return jsonify(retJson)

#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)
#         ret = x*y
#         retMap = {
#             'Message': ret,
#             'Status code': 200
#         }
#         return jsonify(retMap)


# class Divide(Resource):
#     def post(self):
#         postedData = request.get_json()

#         status_code = checkPostedData(postedData, "divide")
#         if (status_code != 200):
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code": status_code
#             }
#             return jsonify(retJson)

#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)
#         ret = (x*1.0)/y
#         retMap = {
#             'Message': ret,
#             'Status code': 200
#         }
#         return jsonify(retMap)


# @app.route('/')
# def hello_world():
#     return "Hello chạy nè, cần gì frontend đâu"


# api.add_resource(Add, "/add")
# api.add_resource(Subtract,"/subtract")
# api.add_resource(Multiply,"/multiply")
# api.add_resource(Divide,"/divide")
# api.add_resource(Visit,"/hello")

# @app.route('/hi')
# def hi():
#     return "hi"


# if __name__ == "__main__":
#     app.run(host='0.0.0.0')
