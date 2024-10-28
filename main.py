# import eventlet
# eventlet.monkey_patch()
from src.app import jwt
from apscheduler.schedulers.background import BackgroundScheduler
from src.modules.company_activity.company_activity_service import CompanyActivityService
from src.modules.system_usage.system_usage_service import SystemUsageService
from flask_cors import CORS
from constants import Constants
from src.connector import app
from src.utils.database_utils import DatabaseUtils
from src.connector import app, socketio
import werkzeug.serving


def aggregate_company_activity_job():
    # Call the aggregation service to update company activity
    print("Running scheduled job to aggregate company activity.")
    CompanyActivityService.aggregate_company_activity()

def log_system_usage_job():
    # Call the service to log system usage data
    print("Logging system usage data.")
    SystemUsageService.log_system_usage()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the job to run every hour (you can adjust the interval)
    scheduler.add_job(aggregate_company_activity_job, 'interval', hours=1)
    scheduler.add_job(log_system_usage_job, 'interval', hours=1)
    scheduler.start()

def run_server():
    CORS(app, resources={"/*": {"origins": "*"}})
    DatabaseUtils.init_cluster_db(Constants.DATABASE_URL)
    
    # werkzeug.run_simple('0.0.0.0', int(Constants.PORT),
    #                     app, use_debugger=True, use_reloader=True)
    socketio.run(app, host='0.0.0.0', port=int(Constants.PORT), debug=True, use_reloader=True)


if __name__ == '__main__':
    run_server()
