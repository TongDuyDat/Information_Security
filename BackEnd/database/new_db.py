import datetime
from mongoengine import Document, StringField, IntField, ReferenceField,  DateTimeField, Q
from database.handerror import encrypt
from database.user_db import User
from config import settings
class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    image = StringField()
    post_type = StringField(required=True)
    created = DateTimeField()
    user_id = ReferenceField(User)
    meta = {"collection": "POSTS"}

    @classmethod
    def create_post(cls, user_id, title, content, post_type, image = ""):
        user = User.objects(id = user_id).first()

        if not user:
            return None, False
        else:
            try:
                new_post = cls(
                    title = title,
                    content = content,
                    image = image,
                    post_type = post_type,
                    created = datetime.datetime.now(),
                    user_id = user_id
                )
                new_post.save()
                return new_post, True
            except:
                return None, False

    @classmethod
    def get_all_post(cls):
        # try:
            from database.file_db import File
            posts = []
            for post in cls.objects().order_by("created"):
                files = File.get_files_by_post_id(post.id)
                url_image = []
                url_file = []
                if files is not None:
                    for f in files:
                        if f["type"]!="Image":
                            file_url = settings.HOST+"api/get_file?id=" + str(f["id"])+"&download"
                            url_file.append(file_url)
                        else:
                            img_url = settings.HOST+"api/get_file?id="+str(f["id"])
                            url_image.append(img_url)
                posts.append({
                    "id": str(post.id),
                    "title": post.title,
                    "content": post.content,
                    "image": url_image,
                    "files": url_file,
                    "post_type": post.post_type,
                    # "username": post.user_id.name,
                    "created": str(post.created)
                    })
            return posts, True
        # except Exception as e:
        #     return None, False
    @classmethod
    def get_post_by_id(cls, id):
        post = cls.objects(id = id)
        return post!=None
    @classmethod
    def search_posts(cls, query):
        posts = []
        try:
            search_results = cls.objects(Q(title__icontains=query) | Q(post_type__icontains=query)).order_by("created")
            
            for post in search_results:
                posts.append({
                    "id": str(post.id),
                    "title": post.title,
                    "content": post.content,
                    "image": post.image,
                    "post_type": post.post_type,
                    "created": str(post.created),
                })
            
            return posts, True
        except Exception as e:
            return None, False
        
    @classmethod
    def update_post(cls, post_id, user_id, title, content, post_type, image=""):
        post = cls.objects(id=post_id, user_id=user_id).first()

        if post is None:
            return False

        post.title = title
        post.content = content
        post.image = image
        post.post_type = post_type
        post.save()
        return True

    @classmethod
    def delete_post(cls, post_id):
        post = cls.objects(id = post_id).first()
        if post:
            post.delete()
            return True
        else:
            return False

        