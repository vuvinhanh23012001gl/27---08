
import time 
import serial.tools.list_ports
class Serial_Com:
    BAUDRATE = 115200
    PARITY = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    BYTESIZE = serial.EIGHTBITS
    TIMEOUT = 1  
    DEVICE = "Serial Device"
    # DEVICE = "CP210x USB"
    def __init__(self):
        self.ser = None 
        self.port = None  
        self.status_connect = False  
    def find_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # print(port.description)
            if Serial_Com.DEVICE in port.description:
                
                self.port = port.device
                # print(f"Đã tìm thấy cổng: {self.port}")
                return self.port
        # print("Không tìm thấy cổng cần tìm.")
        return None
    def open_port(self):
        self.find_port()
        if self.port and self.ser is None:
            try:
                print(f"Tiến hành mở cổng {self.port}")
                self.ser = serial.Serial(
                    port=self.port,
                    baudrate=Serial_Com.BAUDRATE,
                    bytesize=Serial_Com.BYTESIZE,
                    parity=Serial_Com.PARITY,
                    stopbits=Serial_Com.STOPBITS,
                    timeout=Serial_Com.TIMEOUT,
                )
                print("Cổng đã được mở thành công.")
            except:
                print("Mo cong bi loi")
        elif self.ser and self.port:
            print("Cổng Ser và Port đang mở không mở lại")
            return True 
        if self.port is None and self.ser is None: 
            print("Không tồn tại Port va Ser deu tat")   
        else:
            print("Cổng không tồn tại ")
    def send_data(self, data):
        if self.ser and self.ser.is_open:
            try:
                data_to_send = f"{data}\n".encode('utf-8')  
                self.ser.write(data_to_send)
                print(f"PC   :{data}")
                now = time.time()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
                ms = int((now - int(now)) * 1000)
                print("Thời gian gửi lệnh send trực tiếp",f"{timestamp}.{ms:03d}")
            except serial.SerialException as e:
                print("Lỗi khi gửi dữ liệu: {e}")
        else:
            print("Cổng không tồn tại 2")

    def receive_data(self):
        if self.ser and self.ser.is_open:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                print(f"ESP32:{data}")
                now = time.time()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
                ms = int((now - int(now)) * 1000)
                print("Thời gian nhận data receive trực tiếp ",f"{timestamp}.{ms:03d}")
                return data
            else:
                return None
        else:
            print("Cổng không tồn tại 3")
    def close_port(self):
        if self.ser and self.ser.is_open:
            try: 
                self.ser = None 
                self.port = None        
                self.ser.close()
                print(f"Cổng {self.port} đã được đóng.")
            except serial.SerialException as e:
                print(f"Lỗi khi đóng cổng: {e}")
        else:
            print("Cổng không tồn tại 4")
    def get_port_info(self):
        if self.ser and self.ser.is_open:
            info = {
                "port": self.ser.port,
                "baudrate": self.ser.baudrate,
                "bytesize": self.ser.bytesize,
                "parity": self.ser.parity,
                "stopbits": self.ser.stopbits,
                "timeout": self.ser.timeout
            }
            return info
        else:
            print("Chưa mở cổng hoặc cổng không tồn tại.")
            return None
    def show_port_info(self):
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("Không có cổng COM nào được kết nối.")
            return
        print("Danh sách các cổng COM đang kết nối:")
        for port in ports:
            print(f"➤ Tên cổng     : {port.device}")
            print(f"   Mô tả       : {port.description}")
            print(f"   VID:PID     : {port.vid}:{port.pid}")
            print(f"   Tên chip    : {port.name}")
            print(f"   Địa chỉ HW  : {port.hwid}")
            print("-" * 40)
    def try_connect(self):
        while self.find_port() is None:
             print("Đang đợi cổng cắm thiết bị...........")
             time.sleep(0.5)  
        if self.port is not  None:
                    self.open_port()             
                    print(self.get_port_info())
                    print("Ket noi thanh cong")
                
                

            
               
# serial_com = Serial_Com()
# serial_com.try_connect()
# try:
#     serial_com.find_port()
#     serial_com.open_port()
#     serial_com.send_data("200OK")
#     serial_com.receive_data()
#     serial_com.show_port_info()
#     serial_com.get_port_info()
#     serial_com.close_port()
# except Exception as e:
#     print(f"Lỗi: {e}")
# except KeyboardInterrupt as e:
#     print("thoat chuong trinh")
