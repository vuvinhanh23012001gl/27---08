import threading
import time
import queue

class ManagerSerial:
    def __init__(self,queue_rx_arm,queue_tx_arm):
        from serial_communication import Serial_Com 
        # Khởi tạo lớp giao tiếp Serial
        self.serial_com = Serial_Com()

        self.tx_queue = queue_tx_arm
        self.rx_queue = queue_rx_arm

        # Cờ chạy luồng
        self.running_tx = True
        self.running_rx = True

        # Khởi tạo và chạy luồng nhận dữ liệu
        self.rx_thread = threading.Thread(target=self._listen_serial, name="SerialListener")
        self.rx_thread.daemon = True
        self.rx_thread.start()

        # Khởi tạo và chạy luồng gửi dữ liệu
        self.tx_thread = threading.Thread(target=self._send_serial, name="SerialSender")
        self.tx_thread.daemon = True
        self.tx_thread.start()

        print("✅ ManagerSerial đã sẵn sàng.")
    def _listen_serial(self):
        """
        Luồng lắng nghe dữ liệu từ Serial và đưa vào hàng đợi nhận.
        Tự động thử kết nối lại nếu mất kết nối.
        """
        while self.running_rx:
            try:
                # Nếu chưa kết nối thì thử kết nối lại
                if not self.serial_com.status_connect:
                    self.serial_com.try_connect()
                    print("🔄 Chờ 1s kết nối lại với thiết bị…")
                    time.sleep(1)
                    continue

                # Đã kết nối → đọc dữ liệu
                data = self.serial_com.receive_data()
                if data:
                    try:
                        self.rx_queue.put_nowait(data)
                        print(f"[RX Queue] ⬅ {data}")
                    except queue.Full:
                        print("⚠️ Hàng đợi nhận đầy, bỏ dữ liệu!")
                else:
                    # Không có dữ liệu, nghỉ một chút để CPU không 100%
                    time.sleep(0.01)

            except Exception as e:
                print("❌ Lỗi trong luồng nhận:", e)
                time.sleep(0.5)   # Tránh spam lỗi

    def send_data(self, data):
        """Đưa dữ liệu vào hàng đợi gửi"""
        try:
            self.tx_queue.put(data)
            print(f"[TX Queue] ➜ {data}")
        except queue.Full:
            print("⚠️ Hàng đợi gửi đầy. Không thể gửi:", data)
  
    def find_port(self):
        return self.serial_com.find_port()

    def get_data_from_queue(self):
        """Lấy dữ liệu đã nhận ra khỏi hàng đợi"""
        if not self.rx_queue.empty():
            return self.rx_queue.get()
        return None


    def _send_serial(self):
        while self.running_tx:
            if self.serial_com.status_connect:
                try:
                    # block tối đa 0.1s để chờ data, tránh busy-wait
                    data = self.tx_queue.get(timeout=0.1)
                    self.serial_com.send_data(data)
                except queue.Empty:
                    continue  # không có gì để gửi, quay lại vòng lặp

    def stop(self):
        print("🛑 Dừng các luồng và đóng cổng Serial.")
        self.running_rx = False
        self.running_tx = False
        self.rx_thread.join()
        self.tx_thread.join()
        self.serial_com.close_port()
        print("✅ Đã dừng thành công.")
    # def clear_rx_queue(self):
    #     """Xóa tất cả dữ liệu trong hàng đợi nhận"""
    #     cleared = 0
    #     while not self.rx_queue.empty():
    #         self.rx_queue.get_nowait()
    #         cleared += 1
    #     print(f"🗑️ Đã xóa {cleared} mục trong hàng đợi nhận.")

    # def clear_tx_queue(self):
    #     """Xóa tất cả dữ liệu trong hàng đợi gửi"""
    #     cleared = 0
    #     while not self.tx_queue.empty():
    #         self.tx_queue.get_nowait()
    #         cleared += 1
    #     print(f"🗑️ Đã xóa {cleared} mục trong hàng đợi gửi.")
    def get_rx_queue_size(self):
        """Trả về số lượng phần tử trong hàng đợi nhận"""
        size = self.rx_queue.qsize()
        print(f"📥 Số lượng phần tử trong rx_queue: {size}")
        return size
    def get_tx_queue_size(self):
        """Trả về số lượng phần tử trong hàng đợi gửi"""
        size = self.tx_queue.qsize()
        print(f"📦 Số lượng phần tử trong tx_queue: {size}")
        return size
    def clear_rx_queue(self):
        """Xóa sạch toàn bộ hàng đợi nhận"""
        with self.rx_queue.mutex:
            size = len(self.rx_queue.queue)
            self.rx_queue.queue.clear()
        print(f"🗑️ Đã xóa {size} mục trong hàng đợi nhận (clear sạch).")

    def clear_tx_queue(self):
            """Xóa sạch toàn bộ hàng đợi gửi"""
            with self.tx_queue.mutex:
                size = len(self.tx_queue.queue)
                self.tx_queue.queue.clear()
            print(f"🗑️ Đã xóa {size} mục trong hàng đợi gửi (clear sạch).")
    # -------------------------------
# Ví dụ chạy trực tiếp
# -------------------------------
# if __name__ == "__main__":
#     ms = ManagerSerial()

#     try:
#         while True:
#             user_input = input("Nhập dữ liệu gửi ('exit' để thoát): ")
#             if user_input.lower() == 'exit':
#                 break
#             ms.send_data(user_input)

#             # Nếu có phản hồi từ ESP32 thì in ra
#             response = ms.get_data_from_queue()
#             if response:
#                 print("📥 ESP32:", response)

#     except KeyboardInterrupt:
#         print("\n⛔ Dừng bằng Ctrl+C.")
#     finally:
#         ms.stop()

# data = ManagerSerial(queue_tx_arm,queue_rx_arm)
# data.send_data("200OK")
# try:
#     while True:
#         time.sleep(1)
        
# except KeyboardInterrupt as e:
#     data.stop()
#     print("Thoat chuong trinh")

