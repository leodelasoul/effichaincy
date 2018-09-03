from app.auth import routes as auth_user


class Groups:


    def __init__(self, group_id):
        self.group_id = group_id


class Users(Groups):

    def __init__(self, id, name):
        super(Groups, self).__init__()
        self.id = id
        self.name = name



