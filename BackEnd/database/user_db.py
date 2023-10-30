from mongoengine import Document, StringField, IntField
from database.handerror import encrypt
class User(Document):
    
    username = StringField(required=True, max_length=50)
    password = StringField(required=True)
    fullname = StringField()
    dob = StringField()
    citizenshipid = StringField()
    hometown = StringField()
    phonenumber = StringField()
    key_id = StringField()
    meta = {"collection": "USERS"}
    
    def login(username, passwd):
        user =  User.objects(username = username).first()
        if user and (user.password == encrypt(username+passwd)):
            return True
        return False
    
    def register(username, password, fullname, dob="", citizenshipid="", hometown="", phonenumber="", key_id=""):
        user = User.objects(username = username).first()
        if user is not None:
            return None, False
        else:
            try:
                user = User(
                username=username,
                password= encrypt(username+password),
                fullname= fullname,
                dob="",
                citizenshipid="",
                hometown="",
                phonenumber="",
                key_id=""
                )
                user.save()
                return user.to_json(), True
            except:
                return None, False
    def get_user_by_user_name(user_name):
        user = User.objects(username = user_name).first()
        return str(user.id)