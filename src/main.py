import asyncio
from apscheduler.schedulers.blocking import BlockingScheduler
from note import note
from reply import runner
import logging

logging.basicConfig(level=logging.DEBUG)
asyncio.get_event_loop().run_until_complete(runner())


sched = BlockingScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True

@sched.scheduled_job('cron', id='note', minute='*/10')
def cron_note():
    note()
    
if __name__ == "__main__":
    sched.start()