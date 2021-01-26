Here are simple instructions to create a mongodb server on your local machine
Most of the knowledge obtained in this text file came from Coders Page
https://www.youtube.com/watch?reload=9&v=o8jK5enu4L4, which utilizes\
a Flask Framework to operate an App through APIs (done for example by Postman)

1. Download mongodb from https://www.mongodb.com/try/download/community
2. Install it with all dependencies, with one exception: not as a service
3. After installation, create a folder in C:\ called 'data', and another within that one called 'db'
4. Afterwards, locate the MongoDB file within C:\Program Files\...\bin
5. Within, open CMD and type 'mongod'. This will initiate the infrastructure
6. Back again on the bin folder, open another cmd and now type 'mongo'. This creates the server connection
7. Execute the server script, which will open the application. You should not see
the print statement print("Error - Cannot Connect to DB")
If that is indeed the case and the print statement does not appear, you have successfully connected to
a mongodb database. The server however is only create once you do a POST with data to be stored.