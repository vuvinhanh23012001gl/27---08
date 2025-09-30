
import time 
import serial.tools.list_ports
from folder_create import Create
from common_value import NAME_FOLDER_CONFIG
class Serial_Com:
    folder = Create()
    NAME_FILE_CONFIG = "config_com.json"
    path_config = folder.get_or_create_json(NAME_FILE_CONFIG,NAME_FOLDER_CONFIG)
    def __init__(self):
        self.baud_rate = None
        self.parity = None
        self.stop_bits = None
        self.byte_size = None
        self.timeout = None
        self.reconnect_interval = None
        self.serial_com   = None

        self.ser = None 
        self.port = None  
      

        self.init()
    def init(self):
        data = Serial_Com.folder.read_json_from_file(Serial_Com.path_config)
        if data:
            self.serial_com = data.get("device_name",None)
            self.baud_rate = data.get("baudrate", 115200)
            self.parity = data.get("parity", "N")
            self.stop_bits = data.get("stopbits", 1)
            self.byte_size = data.get("bytesize", 8)
            self.timeout = data.get("timeout", 1.0)
            self.reconnect_interval = data.get("reconnect_interval", 1.0)
            print("🔧 Cấu hình Serial:")
            print("  device_name       :", self.serial_com)
            print("  baudrate          :", self.baud_rate)
            print("  parity            :", self.parity)
            print("  stopbits          :", self.stop_bits)
            print("  bytesize          :", self.byte_size)
            print("  timeout           :", self.timeout)
            print("  reconnect_interval:", self.reconnect_interval)
        else:
            print("Dữ liệu rỗng hoặc không thể đọc từ file.")
            print("Yêu cầu chọn cấu hình từ file ")

        # config = self.read_file_config(self.path_config)
        # if config:
        #     self.baud_rate = config.get("baudrate", 115200)
        #     self.parity = config.get("parity", "N")
        #     self.stop_bits = config.get("stopbits", 1)
        #     self.byte_size = config.get("bytesize", 8)
        #     self.timeout = config.get("timeout", 1.0)
        # else:
        #     print("Không thể đọc cấu hình từ file.")
    def find_port_by_description(self, description):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # print(port.description)
            if description in port.description:
                self.port = port.device
                # print(f"Đã tìm thấy cổng: {self.port}")
                return self.port
        return None
    def open_port_external(self, port: str,
                baudrate: int = 115200,
                bytesize: int = 8,
                parity: str = "N",
                stopbits: int = 1,
                timeout: float = 1.0) -> bool:
        """
        Mở cổng serial với các tham số truyền từ bên ngoài.
        Trả về True nếu mở thành công, False nếu thất bại.
        """
        if port and self.ser is None:
            try:
                print(f"🔌 Tiến hành mở cổng {port}")
                self.ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    bytesize=bytesize,
                    parity=parity,
                    stopbits=stopbits,
                    timeout=timeout
                )
                print("✅ Cổng đã được mở thành công.")
                return True
            except serial.SerialException as e:
                print(f"❌ Lỗi khi mở cổng: {e}")
                return False

        elif self.ser and port:
            print("⚠️ Cổng đã được mở trước đó, không mở lại.")
            return True

        else:
            self.status_connect = False
            print("❌ Không tồn tại port hợp lệ.")
            return False

    def connect_com(self):
        if self.serial_com:
            status_open  = self.open_port_external(self.serial_com,
                baudrate=self.baud_rate,
                bytesize=self.byte_size,
                parity=self.parity,
                stopbits=self.stop_bits,
                timeout=self.timeout)
            return status_open
        return False


  
        # else:







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
    def get_list_port(self):
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
                self.status_connect = True   # ✅ ĐÃ KẾT NỐI THÀNH CÔNG
                print("Cổng đã được mở thành công.")
            except:
                self.status_connect = False  # ❌ MỞ CỔNG LỖI
                print("Mở cổng bị lỗi")
        elif self.ser and self.port:
            self.status_connect = True 
            print("Cổng Ser và Port đang mở không mở lại")
            return True 
        if self.port is None and self.ser is None: 
            self.status_connect = False      # ❌ KHÔNG TỒN TẠI CỔNG
            print("Không tồn tại Port và Ser đều tắt")   
        else:
            self.status_connect = False
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
            return False
    def close_port(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
                self.status_connect = False   # ✅ ĐÓNG CỔNG → MẤT KẾT NỐI
                self.ser = None 
                self.port = None        
                print(f"Cổng đã được đóng.")
            except serial.SerialException as e:
                self.status_connect = False
                print(f"Lỗi khi đóng cổng: {e}")
        else:
            self.status_connect = False       # ❌ KHÔNG TỒN TẠI → CHẮC CHẮN MẤT KẾT NỐI
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
        if not self.status_connect:
            self.open_port()
        if self.status_connect:           # ✅ KIỂM TRA TRẠNG THÁI
                print(self.get_port_info())
                print("Kết nối thành công")
        else:
                print("Kết nối thất bại")
serial_com = Serial_Com()
# folder = Create()
# path= folder.create_file_in_folder_two("config.json","CONFIG")
# data = {
#   "device_name": "Serial Device",    
#   "baudrate": 115200,               
#   "bytesize": 8,                       
#   "parity": "N",                        
#   "stopbits": 1,                      
#   "timeout": 1.0,                     
#   "reconnect_interval": 1.0            
# }
# folder.write_json_to_file(path,data)
# # serial_com.try_connect()
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
