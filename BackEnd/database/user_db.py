from mongoengine import Document, StringField, IntField
from database.handerror import encrypt

class User(Document):
    username = StringField(required=True, max_length=50)
    password = StringField(required=True)
    email = StringField(required=True)
    fullname = StringField(required=True)
    dob = StringField(required=True)
    sex = StringField(required=True)
    hometown = StringField(required=True)
    phonenumber = StringField()
    citizenshipid = StringField()
    key_id = StringField()
    meta = {"collection": "USERS"}
    
    def login(username, passwd):
        user =  User.objects(username = username).first()
        if user and (user.password == encrypt(username+passwd)):
            return True
        return False
    
    def register(username, password, email, fullname, dob, sex, hometown, phonenumber="", citizenshipid="", key_id=""):
        user = User.objects(username = username).first()
        if user is not None:
            return None, False
        else:
            try:
                user = User(
                username=username,
                password= encrypt(username+password),
                email= email,
                fullname= fullname,
                dob= dob,
                sex = sex,
                hometown= hometown,
                phonenumber= "",
                citizenshipid = "",
                key_id=""
                )
                user.save()
                return user.to_json(), True
            except:
                return None, False
            
    def get_user_by_user_name(user_name):
        user = User.objects(username = user_name).first()
        return str(user.id)
    
    def get_all_user():
        users = []
        for user in User.objects().order_by("created"):
            users.append({
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "fullname": user.fullname,
                "dob": user.dob,
                "citizenshipid": user.citizenshipid,
                "hometown": user.hometown,
                "phonenumber": user.phonenumber
                })
        return users, True
    
    def update_user(_id, fullname, dob, sex, hometown, phonenumber="", citizenshipid=""):
        user = User.objects(id = _id).first()
        if user is None:
            return False
        user.fullname = fullname
        user.dob = dob
        user.sex = sex
        user.citizenshipid = citizenshipid
        user.hometown = hometown
        user.phonenumber = phonenumber
        user.save()
        return True
    
    def delete_user(_id):
        user = User.objects(id = _id).first()
        if user:
            user.delete()
            return True
        return False
