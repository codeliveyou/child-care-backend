from src.modules.user_activity.user_activity_dtos import CreateUser_activityBody, UpdateUser_activityBody


class User_activityService:

    @staticmethod
    def create(body: CreateUser_activityBody):
        return f"create User_activity"

    @staticmethod
    def get_one(id):
        return "get one User_activity"

    @staticmethod
    def get_all():
        return "get all user_activitys"

    @staticmethod
    def update_one(id, body: UpdateUser_activityBody):
        return "update one User_activity"

    @staticmethod
    def delete_one(id):
        return "delete one User_activity"

    @staticmethod
    def delete_all():
        return "delete all user_activity"
