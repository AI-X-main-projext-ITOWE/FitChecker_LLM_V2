# scheduler_setup.py
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

# Scheduler 초기화A
scheduler = BackgroundScheduler()

# scheduler.start()