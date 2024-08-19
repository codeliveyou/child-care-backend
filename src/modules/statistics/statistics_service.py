from src.modules.statistics.statistics_dtos import CreateStatisticsBody, UpdateStatisticsBody


class StatisticsService:

    @staticmethod
    def create(body: CreateStatisticsBody):
        return f"create Statistics"

    @staticmethod
    def get_one(id):
        return "get one Statistics"

    @staticmethod
    def get_all():
        return "get all statisticss"

    @staticmethod
    def update_one(id, body: UpdateStatisticsBody):
        return "update one Statistics"

    @staticmethod
    def delete_one(id):
        return "delete one Statistics"

    @staticmethod
    def delete_all():
        return "delete all statistics"
