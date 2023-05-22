import schedule
import time


def run_send_bot():
    try:
        import scrap_hh
        scrap_hh.startup()
    except Exception:
        pass


schedule.every(1800).seconds.do(run_send_bot)
while True:
    schedule.run_pending()
    time.sleep(1)
