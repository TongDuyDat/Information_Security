import datetime
from mongoengine import Document, StringField, IntField, ReferenceField,  DateTimeField, Q
from database.handerror import encrypt
from database.user_db import User
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
        posts = []
        # try:
        for post in cls.objects().order_by("created"):
            posts.append({
                "id": str(post.id),
                "title": post.title,
                "content": post.content,
                "image": post.image,
                "post_type": post.post_type,
                # "username": post.user_id.name,
                "created": str(post.created)
                })
        return posts, True
        # except Exception as e:
        #     return None, False

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

        