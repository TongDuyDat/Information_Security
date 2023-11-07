from mongoengine import Document, ReferenceField, ObjectIdField, StringField, IntField, DateTimeField
from database.new_db import Post
from datetime import datetime
class File(Document):
    original_name = StringField(required=True, max_length=255)
    path = StringField(required=True) 
    post_id = ReferenceField(Post)
    created_at = DateTimeField(required=True)
    name = StringField(required=True, max_length=255)
    type = StringField()
    meta = {'collection': 'FILES'}

    @classmethod
    def get_files_by_post_id(cls, post_id):
        file = []
        files = cls.objects(post_id = post_id)
        for f in files:
            file.append({'type':f.type,
                         'original_name':f.original_name,
                         'id': str(f.id),
                         "name": f.name,
                         })
        return file
    @classmethod
    def create_file(cls, post_id, path, original_name, name, ftype = "Image"):
        try:
            obj = File( original_name = original_name,
                        path = path,
                        post_id = post_id, 
                        created_at = datetime.now(), 
                        name = name,
                        type = ftype)
            obj.save()
            return True, obj
        except:
            return False, None
    @classmethod
    def get_file_by_id(cls, id):
        try:
            f = cls.objects.get(id = id)
            return True, {
                'path':f.path,
                'original_name':f.original_name,
                'id': str(f.id),
                "name": f.name,
                "type": f.type
                }
        except:
            return False, None

    