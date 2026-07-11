import schedule
import time
import threading
from src.utils.logger import setup_logger

logger = setup_logger('scheduler', 'logs/scheduler.log')

class JobScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, task_func, interval_minutes):
        logger.info(f"Adding job: {task_func.__name__} every {interval_minutes} minutes")
        job = schedule.every(interval_minutes).minutes.do(task_func)
        self.jobs.append(job)

    def run_pending(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start(self):
        logger.info("Starting scheduler...")
        scheduler_thread = threading.Thread(target=self.run_pending)
        scheduler_thread.daemon = True
        scheduler_thread.start()
