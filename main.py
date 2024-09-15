from apscheduler.schedulers.background import BackgroundScheduler
from src.modules.company_activity.company_activity_service import CompanyActivityService
from flask_cors import CORS
from constants import Constants
from src.connector import app
from src.utils.database_utils import DatabaseUtils
import werkzeug.serving

def aggregate_company_activity_job():
    # Call the aggregation service to update company activity
    print("Running scheduled job to aggregate company activity.")
    CompanyActivityService.aggregate_company_activity()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the job to run every hour (you can adjust the interval)
    scheduler.add_job(aggregate_company_activity_job, 'interval', hours=1)
    scheduler.start()

def run_server():
    cors = CORS(app)
    DatabaseUtils.init_cluster_db(Constants.DATABASE_URL)
    start_scheduler()  # Start the scheduler when the app starts
    werkzeug.run_simple('0.0.0.0', int(Constants.PORT), app, use_debugger=True, use_reloader=True)

if __name__ == '__main__':
    run_server()
