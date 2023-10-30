from mongoengine import connect

# Replace <password> and other connection details with your MongoDB configuration
try:
    username = 'chukhanhhung'
    password = 'Abc123'
    hostname = 'cluster0.pvie75s.mongodb.net'
    database_name = 'ABE'
    print("connect db")
    #connect(host="mongodb://my_user:my_password@127.0.0.1:27017/my_db?authSource=my_db")
    connect(
        host="mongodb+srv://chukhanhhung:Abc123@cluster0.pvie75s.mongodb.net/ABE"
    )
except:
    print("connect db error")