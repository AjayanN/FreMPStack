from flask import Flask,request,jsonify
from flask_pymongo import PyMongo,ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/crudapp'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users

# @app.route("/")
# def index():
#     return "<h1> Hello world"

@app.route("/users", methods = ['POST'])
def createUser():
    id = db.insert_one({
        'name':request.json["name"],
        'email':request.json["email"],
        'contact':request.json["contact"],
        'address':request.json["address"]
    })
    return jsonify({"id":str(ObjectId(id.inserted_id)),'msg':"User added succesfully"})

@app.route("/users", methods = ['GET'])
def getUsers():
    users = []
    for each in db.find():
        users.append({
            '_id':str(ObjectId(each.get("_id"))),
            'name':each.get('name'),
            'email':each.get('email'),
            'contact':each.get('contact'),
            'address':each.get('address')
            })
    return jsonify(users)

@app.route("/users/<id>", methods = ['GET'])
def getUserDetails(id):
    user = db.find_one({'_id':ObjectId(id)})
    return jsonify({
            '_id':str(ObjectId(user.get("_id"))),
            'name':user.get('name'),
            'email':user.get('email'),
            'contact':user.get('contact'),
            'address':user.get('address')
            })

@app.route("/users/<id>", methods = ['DELETE'])
def deleteUserData(id):
    db.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg":"User deleted successfully"})

@app.route("/users/<id>", methods = ['PUT'])
def updateUserData(id):
    db.update_one({'_id':ObjectId(id)},{'$set':{
        'name':request.json["name"],
        'email':request.json["email"],
        'contact':request.json["contact"],
        'address':request.json["address"]
    }})
    return jsonify({"id":str(ObjectId(id)),'msg':"User updated succesfully"})

if __name__ == '__main__':
    app.run(debug=True)