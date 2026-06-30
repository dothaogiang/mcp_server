# sync/scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from sync.fetch_archives import sync_all_archives

scheduler = BlockingScheduler()

# Chạy ngay 1 lần khi khởi động, sau đó mỗi 1 tiếng chạy lại
@scheduler.scheduled_job("interval", hours=1, id="sync_archives")
def job():
    sync_all_archives()

if __name__ == "__main__":
    print("Scheduler khởi động — sync ngay lần đầu...")
    sync_all_archives()  # chạy ngay không chờ 1 tiếng
    print("Scheduler chạy, tự động sync mỗi 1 tiếng. Ctrl+C để dừng.")
    scheduler.start()