from apscheduler.schedulers.blocking import BlockingScheduler
import main

def job():
    main.main()
    
scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='mon', hour=10, minute=0)

try:
    print("Scheduler iniciado...")
    scheduler.start()  
except (KeyboardInterrupt, SystemExit):
    pass