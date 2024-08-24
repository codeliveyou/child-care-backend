from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pydantic_docs import OpenAPI
#
app = Flask(__name__)
app.config["DEBUG"] = False
app.config["CACHE_TYPE"] = "null"
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
jwt = JWTManager(app)
# openapi
swagger = OpenAPI(endpoint="/docs/swagger/", ui='swagger', name="swagger", extra_props={
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    "security": [{"bearerAuth": []}]
})
swagger.register(app)
redoc = OpenAPI(endpoint="/docs/redoc/", ui='redoc', name="redoc")
redoc.register(app)
# BP REG
from src.modules.root.root_controller import root_controller
app.register_blueprint(root_controller, url_prefix='/')
from src.modules.user.user_controller import user_controller
app.register_blueprint(user_controller, url_prefix='/users')

from src.modules.admin.admin_controller import admin_controller
app.register_blueprint(admin_controller, url_prefix='/admins')

from src.modules.company.company_controller import company_controller
app.register_blueprint(company_controller, url_prefix='/companys')

from src.modules.invoice.invoice_controller import invoice_controller
app.register_blueprint(invoice_controller, url_prefix='/invoices')

from src.modules.statistics.statistics_controller import statistics_controller
app.register_blueprint(statistics_controller, url_prefix='/statistics')

from src.modules.room.room_controller import room_controller
app.register_blueprint(room_controller, url_prefix='/rooms')

# from src.modules.userdata.userdata_controller import userdata_controller
# app.register_blueprint(userdata_controller, url_prefix='/userdatas')
