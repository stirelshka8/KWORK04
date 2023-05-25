import schedule
import time


def run_send_bot():
    try:
        import scrap_hh
        scrap_hh.startup()
    except Exception:
        pass


def start_shed(time_run):
    schedule.every(time_run).seconds.do(run_send_bot)
    while True:
        schedule.run_pending()
        time.sleep(1)
