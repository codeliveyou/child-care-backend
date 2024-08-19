from flask import Flask
from flask_pymongo import PyMongo
from app.routes.company_routes import company_blueprint
from app.routes.user_routes import user_blueprint
from app.routes.statistics_routes import statistics_blueprint
from app.routes.admin_routes import admin_blueprint
from app.routes.invoice_routes import invoice_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize PyMongo
mongo = PyMongo(app)

# Register Blueprints
app.register_blueprint(company_blueprint, url_prefix='/api/companies')
app.register_blueprint(user_blueprint, url_prefix='/api/users')
app.register_blueprint(statistics_blueprint, url_prefix='/api/statistics')
app.register_blueprint(admin_blueprint, url_prefix='/api/admins')
app.register_blueprint(invoice_blueprint, url_prefix='/api/invoices')

if __name__ == "__main__":
    app.run(debug=True)
