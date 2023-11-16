from mongoengine import Document, StringField, IntField
from database.handerror import encrypt
from datetime import datetime

class User(Document):
    username = StringField(required=True, max_length=50)
    password = StringField(required=True)
    email = StringField(required=True)
    fullname = StringField(required=True)
    dob = StringField(required=True)
    sex = StringField(required=True)
    hometown = StringField(required=True)
    group = StringField(required=True)
    phonenumber = StringField()
    citizenshipid = StringField()
    key_id = StringField()
    meta = {"collection": "USERS"}
    
    def login(username, passwd):
        user =  User.objects(username = username).first()
        if user and (user.password == encrypt(username+passwd)):
            return True
        return False
    
    def register(username, password, email, fullname, dob, sex, hometown, group, phonenumber="", citizenshipid="", key_id=""):
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
                group= group,
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
                "sex": user.sex,
                "hometown": user.hometown,
                "group": user.group,
                "citizenshipid": user.citizenshipid,
                "phonenumber": user.phonenumber
                })
        return users, True
    
    def update_user(_id, fullname, dob, sex, hometown, group, phonenumber="", citizenshipid=""):
        user = User.objects(id = _id).first()
        if user is None:
            return False
        user.fullname = fullname
        user.dob = dob
        user.sex = sex
        user.hometown = hometown
        user.group = group
        user.phonenumber = phonenumber
        user.citizenshipid = citizenshipid
        user.save()
        return True
    
    def delete_user(_id):
        user = User.objects(id = _id).first()
        if user:
            user.delete()
            return True
        return False
    
    @staticmethod
    def map_values(value, value_mapping):
        return value_mapping.get(value, None)

    def get_attributes_by_id(_id):
        user = User.objects(id=_id).first()
        if user:
            sex_mapping = {"Nam": 1, "Nữ": 2}
            hometown_mapping = {
                "Bá Thước": 3,
                "Cẩm Thủy": 4,
                "Đông Sơn": 5,
                "Hà Trung": 6,
                "Hậu Lộc": 7,
                "Hoằng Hóa": 8,
                "Lang Chánh": 9,
                "Nga Sơn": 10,
                "Ngọc Lặc": 11,
                "Như Xuân": 12,
                "Nông Cống": 13,
                "Quan Hóa": 14,
                "Quảng Xương": 15,
                "Thạch Thành": 16,
                "Thiệu Hóa": 17,
                "Thọ Xuân": 18,
                "Thường Xuân": 19,
                "Tĩnh Gia": 20,
                "Vĩnh Lộc": 21,
                "Yên Định": 22
            } 
            group_maping = {
                "Tự nhiên": 23,
                "Xã hội": 24,
                "Thể dục": 25,
                "Ngoại ngữ": 26
            }

            user_attributes = [
                sex_mapping.get(user.sex, None),
                hometown_mapping.get(user.hometown, None),
                group_maping.get(user.group, None)
            ]

            return user_attributes, True

        return None, False

    