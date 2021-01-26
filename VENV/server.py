from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId #this is to unpack the object id into text, so json can be used

app = Flask(__name__)



#connecting to mongo database
try: #go to Mongo folder and run mongod to start a server. Afterwards, run mongo to start the the shell
    mongo = pymongo.MongoClient(host="localhost",
                                port=27017, #default port for mongo
                                serverSelectionTimeoutMS = 1000)
    db = mongo.company #company or whatever we want, this is a database
    mongo.server_info() #will trigger the exception if it cannot connect to the DB

except:
    print("Error - Cannot Connect to DB")
    pass
##################

@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        # data = db.users.find() #this command gives us all the users, but is a cursur poitning to database
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])

        return Response( #sends the error to the client as well!
                        response=json.dumps(data),
                        status=500, #internal server error
                        mimetype="application/json"
                        )
    except Exception as ex:
        print(ex)
        return Response( #sends the error to the client as well!
                        response=json.dumps({"message":"cannot read users"}),
                        status=500, #internal server error
                        mimetype="application/json"
                        )
##################

@app.route("/users", methods=["POST"])
def create_user():
    try:
        # user = {"name":"A", "lastName":"AA"} #the user is in json, and this data will be filled by Postman
        user = {"last_Name": request.form["last_Name"],
                "first_Name": request.form["first_Name"]}  # the user is in json, and this data will be filled by Postman

        dbResponse = db.users.insert_one(user) #this is pointing to the company database, and we will be inserting data
        # for attr in dir(dbResponse):
        #     print(attr)
        print(dbResponse.inserted_id) #gives us the id #600d7e5fd1a8858a1a62b1bc
        return Response(
                        response=json.dumps({"message":"user created","id":f"{dbResponse.inserted_id}"}),
                        status=200,
                        mimetype="application/json"
                        )

    except Exception as ex:
        print("*************")
        print(ex) #this way we can read the exception
        print("*************")


################## https://www.youtube.com/watch?v=o8jK5enu4L4

@app.route("/users/<id>", methods=["PATCH"])
def update_user(id): #<id> -> id
    try:
        dbResponse = db.users.update_one(
            {"_id":ObjectId(id)}, #here the id is an objectid
            {"$set":{"last_Name":request.form["last_Name"]}}
        )
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},  # here the id is an objectid
            {"$set": {"first_Name": request.form["first_Name"]}}
        )
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****") #check each attribute
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({"message": "user updated"}),
                status=200,
                mimetype="application/json"
            )
        else: #this is just to tell you if the changes you made had any impact
            return Response(
                response=json.dumps({"message": "nothing to update"}),
                status=200,
                mimetype="application/json"
            )

    except Exception as ex:
        print('***********')
        print(ex)
        print('***********')
        return Response(
            response=json.dumps({"message": "system cannot update"}),
            status=500,
            mimetype="application/json"
        )

##################
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        # for attr in dir(dbResponse): #dir lists 'files'
        #     print(f"***{attr}***")
        if db.Response.deleted_count == 1:
            return Response(
                response=json.dumps({"message": "user was deleted", "id":f"{id}"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "user was never in the database", "id": f"{id}"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print('***********')
        print(ex)
        print('***********')
        return Response(
            response=json.dumps({"message": "system cannot delete"}),
            status=500,
            mimetype="application/json"
        )

##################
#to run the app
if __name__ == "__main__":
    app.run(port=80,debug=True)






