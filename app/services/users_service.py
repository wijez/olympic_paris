class UsersService:
    def __init__(self, user_model):
        self.user_model = user_model

    def get_user(self, username):
        return self.user_model.query.filter_by(username=username).first()


