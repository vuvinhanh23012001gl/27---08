
import threading
import time
from manager_serial import ManagerSerial
import func
import queue    
from shared_queue import queue_rx_web_api,queue_tx_web_main,queue_rx_web_main,queue_tx_web_log
from producttypemanager import ProductTypeManager
from connect_camera import  BaslerCamera
#---lock doi tuong-----
manage_product_type = ProductTypeManager()
manage_product_type_lock = threading.Lock()
Object_BaslerCamera = None
click_page_html = threading.Lock()     #1 la dang o file chinh  2 la o fine traing_model 3 la file cau hinh cam hay lmj do
click_page_html = 0
flask_training_erase_queue = 1
is_data_train = 0
is_run = 0
#-------------------------------------------------
STATUS_CHECK_CONNECT = 2         #trang thai cho ket noi
SIZE_SEND_THE_FIRST_CONNECT = 2
# SIZE_SEND_THE_FIRST_CONNECT_WEB_API_INF_MODEL = 1
TIME_RETURN_TO_ORIGIN = 10
SIZE_QUEUE_RX_ARM = 50
SIZE_QUEUE_TX_ARM = 50
NAME_FILE_CHOOSE_MASTER = "choose_master"   #Tránh import nhiều lần nên đặt biến luôn . khi thay đổi đường dẫn nhớ thay đổi cả file run và file main_pc giống nhau


queue_tx_arm = queue.Queue(maxsize = SIZE_QUEUE_TX_ARM)
print("queue_tx_arm:", queue_tx_arm)
queue_rx_arm = queue.Queue(maxsize = SIZE_QUEUE_RX_ARM)
print("queue_rx_arm:", queue_rx_arm)
#-------------------------------------------------
def fuc_main_process():
    global STATUS_CHECK_CONNECT
    global is_data_train 
    global click_page_html
    global is_run
    obj_manager_serial = ManagerSerial(queue_rx_arm=queue_rx_arm,queue_tx_arm=queue_tx_arm) # Mở hàm này thì mới vào đc phân mềm chính không thì chương trình bị giữ ở đây
    the_first_connect = True
    flag_the_firts_connect = True
    while True:
        if obj_manager_serial.find_port() is not None:
            while (the_first_connect == True):
                # print("----------------- Bắt đầu kết nối với ARM -------------------")
                if(queue_tx_arm.qsize() < SIZE_SEND_THE_FIRST_CONNECT):
                    obj_manager_serial.send_data("200OK:")
                    STATUS_CHECK_CONNECT = 0
                    time.sleep(1)   
                if obj_manager_serial.get_rx_queue_size() > 0:
                        data = obj_manager_serial.get_data_from_queue()
                        print("Data nhận được từ Queue ARM:", data)
                        if("200OK," in data ):
                            if(len(data) <= 6):
                                print("❌Độ dài dữ liệu gửi về ngắn....PC Gửi lại 200OK") 
                                continue
                            cut_data = data[6:].split(",")
                            print("Mảng ",cut_data)
                            if cut_data == data[6:]:
                                print("❌Dữ liệu không có dấu phẩy....PC Gửi lại 200OK")
                                continue
                            if (func.is_all_int_strings(cut_data) == False or len(cut_data) != 4):
                                print("Dữ liệu tọa độ ban đầu không hợp lệ. Vui lòng kiểm tra lại.")
                                continue
                            if "200OK,000,000,000" in data:
                                  print("........Nhan dung tin hieu dieu khien .....")
                                  the_first_connect = False
                                  obj_manager_serial.clear_rx_queue()  
                                  obj_manager_serial.clear_tx_queue()
                                  break
                            else:
                                 obj_manager_serial.send_data("cmd:0,0,0,0")
                                 time.sleep(1)   
            # print("----------------- Bắt đầu điều khiển với ARM -------------------")
            #click_page_html  ==  2 vao che do trainning san pham
            #click_page_html  ==  1 Vào Chế độ main  show
            STATUS_CHECK_CONNECT = 1
            if click_page_html  == 2:
                if not queue_rx_web_api.empty():
                    data_web_rx = queue_rx_web_api.get()
                    if("cmd:" in data_web_rx):
                        obj_manager_serial.clear_tx_queue()
                        obj_manager_serial.send_data(data_web_rx)
                        result_send = func.wait_for_specific_data(obj_manager_serial,data_web_rx)                   
                        if result_send:
                            queue_tx_web_log.put(f"Send : {data_web_rx} Thanh cong ")
                        else :
                            queue_tx_web_log.put(f"Send : {data_web_rx} That bai")
                if is_data_train == 1:
                              is_data_train = 0
                              print("Co san pham dang can train")
                              func.read_file_training('name_product_train.json',queue_tx_arm,obj_manager_serial,data_web_rx) # Thuc hien doc tin hieu tra ve va thuc hien
                              time.sleep(0.5)
                              
            elif(click_page_html == 1):
                import run 
                
                print("Đang Xử Lý Trang Main")
                if flag_the_firts_connect :
                     flag_the_firts_connect = False
                
                # else:
                #     #  print("Cam đã kết nối")
                if(is_run == 1): 
                       run.cam_basler.initialize_camera()
                       is_run = 0  #tat de khong vao lai
                       obj_manager_serial.clear_rx_queue()
                       obj_manager_serial.clear_tx_queue()
                       print("Bắt đầu chạy các điểm")
                       func.create_choose_master(NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
                       choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER) # đọc lại file choose master cũ xem lần trước  người dùng chọn gì
                       print("Chạy với ID là :",choose_master_index)
                       arr_point = manage_product_type.get_list_point_find_id(choose_master_index.strip())
                       name_product       = manage_product_type.get_product_name_find_id(choose_master_index.strip())
                    #    print("arr Point",arr_point)
                    #    print("name product",name_product)
                       
                       if arr_point is not None and name_product is not None :
                              print("Quá trình chạy các điểm")
                              func.run_and_capture(name_product,arr_point,obj_manager_serial,run.cam_basler)
                       else:
                            print("Không tìm thấy ID danh sách điểm để chạy")
                            
                              
                  
                              
                       
                              


               

                time.sleep(2)         
            # time.sleep(2)
                         
        else:
            the_first_connect = True
            func.clear_queue(queue_rx_web_main)
            print("❌ Không tìm thấy cổng Serial. Vui lòng kiểm tra kết nối.")
            print("Xin chao")
            time.sleep(1)
       
main_process = threading.Thread(target=fuc_main_process)
main_process.start()     
    