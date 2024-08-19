from flask import Blueprint
from flask_pydantic import validate
from src.modules.statistics.statistics_service import StatisticsService
from src.modules.statistics.statistics_dtos import CreateStatisticsBody, UpdateStatisticsBody
from src.utils.responder import Responder
from flask_pydantic_docs import openapi_docs

statistics_controller = Blueprint('statisticss', __name__)


@statistics_controller.post('/')
@openapi_docs()
@validate()
def create_statistics(body: CreateStatisticsBody):
    return StatisticsService.create(body)

@statistics_controller.get('/<id>')
@openapi_docs()
@validate()
def get_one_statistics(id):
    return StatisticsService.get_one(id)

@statistics_controller.get('/')
@openapi_docs()
@validate()
def get_all_statisticss():
    return StatisticsService.get_all()

@statistics_controller.put('/<id>')
@openapi_docs()
@validate()
def update_one_statistics(id, body: UpdateStatisticsBody):
    return StatisticsService.update_one(id, body)

@statistics_controller.delete('/<id>')
@openapi_docs()
@validate()
def delete_one_statistics(id):
    return StatisticsService.delete_one(id)

@statistics_controller.delete('/')
@openapi_docs()
@validate()
def delete_all_statisticss():
    return StatisticsService.delete_all()

