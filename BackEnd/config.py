import os
path = os.getcwd()
print(path)
class settings:
    SECRET_KEY: str = "ATTT"
    JWT_ALGORITHM: str = "HS256"
    UPLOAD_FOLDER: str = "{}/Uploaded".format(path)
    HOST: str = "http://127.0.0.1:5000/"