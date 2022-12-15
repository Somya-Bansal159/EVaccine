import Registration.views
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

scheduler.add_job(Registration.views.reset_tables,
                  'interval', hours=24)
scheduler.start()
