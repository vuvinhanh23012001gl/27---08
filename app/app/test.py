import threading
import time

def task():
    while True:
        print("Thread đang chạy...")
        time.sleep(1)

# Daemon thread
t1 = threading.Thread(target=task, daemon=True)
t1.start()

# # Non-daemon thread
# t2 = threading.Thread(target=task, daemon=False)
# t2.start()

print("Chương trình chính kết thúc")
