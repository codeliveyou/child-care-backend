from src.modules.admin.admin_dtos import CreateAdminBody, UpdateAdminBody


class AdminService:

    @staticmethod
    def create(body: CreateAdminBody):
        return f"create Admin"

    @staticmethod
    def get_one(id):
        return "get one Admin"

    @staticmethod
    def get_all():
        return "get all admins"

    @staticmethod
    def update_one(id, body: UpdateAdminBody):
        return "update one Admin"

    @staticmethod
    def delete_one(id):
        return "delete one Admin"

    @staticmethod
    def delete_all():
        return "delete all admin"
