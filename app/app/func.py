import time
import queue
from flask import Flask,request,jsonify
import json
import queue
import os
import numpy as np
import cv2 

SIZE_X_MAX =  110
SIZE_X_MIN = 0
SIZE_Y_MAX = 75
SIZE_Y_MIN = 0
SIZE_Z_MAX =  12
SIZE_Z_MIN = 0
SIZE_K_MAX = 100
SIZE_K_MIN = 0
SIZE_SHIFT_MAX = 10
SIZE_SHIFT_MIN = 0
TIME_OUT_WAIT_ARM_RESEND = 4
from  shared_queue import queue_accept_capture,queue_tx_web_main
def clear_queue(q):
    print(f"❌ Xoa queue {q}")
    while not q.empty():
        try:
            q.get_nowait()
            q.task_done()
        except queue.Empty:
            break
def send_with_ack_retry(obj_manager_serial, message:str, timeout:int=5):
        for attempt in range(2):
            print(f"🚀 Gửi lần {attempt + 1}: {message}")
            obj_manager_serial.send_data(message)
            start_time = time.time()

            while time.time() - start_time < timeout:
                data = obj_manager_serial.receive_data()
                if data:
                    print(f"📥 Nhận: {data}")
                    if data.strip() == message:
                        print("✅ Nhận phản hồi đúng. Gửi thành công.")
                        return True
                    else:
                        print("⚠️ Nhận sai nội dung.")
                time.sleep(0.1)  # Tránh busy-wait
            print("⏰ Timeout không nhận được dữ liệu đúng.")
        print("❌ Gửi không thành công sau 2 lần.")
        return False

def wait_for_specific_data(obj_manager_serial, expected_message_1, timeout=TIME_OUT_WAIT_ARM_RESEND):
    print(f"⏳ Đang chờ tín hiệu:{expected_message_1} trong {timeout} giây...")
    start_time = time.time()
    expected = data_format(expected_message_1)  # chỉ xử lý 1 lần
    while time.time() - start_time < timeout:
        data = obj_manager_serial.get_data_from_queue()
        if data:
            print(f"📥 PC Nhận được: {data}")
            print("📥 Sau chuyển đổi :", expected)

            if data.strip() == expected:
                now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(now_str,"✅ Nhận đúng tín hiệu mong đợi.")
                return True
            else:
                print("⚠️ Tín hiệu nhận sai nội dung.")
        time.sleep(0.001)  # 🔑 tránh CPU 100% + làm chương trình mượt hơn

    print(f"❌ Timeout: Không nhận được tín hiệu trong {timeout} giây.")
    return False
def is_all_int_strings(lst):
    try:
        return all(isinstance(int(item), int) for item in lst)
    except ValueError:
        return False
def data_format(arr_check):
    if not arr_check:
        print("❌ Dữ liệu bị lỗi hoặc trống, không có dữ liệu để so sánh.")
        return False
    if arr_check.startswith("cmd:"):
        raw_data = arr_check[4:].split(",")
        raw_data = [x.strip() for x in raw_data if x.strip() != ""]

        if not raw_data:
            print("❌ Không có dữ liệu tọa độ sau 'cmd:'")
            return False

        arr_covert_text = ["cmd:"]
        for i in raw_data:
            try:
                padded = f"{int(i):03}"
            except ValueError:
                print(f"⚠️ Không thể chuyển '{i}' thành số nguyên.")
                return False
            arr_covert_text.append(padded)

        arr_covert_text.append("ok")
        s = ",".join(arr_covert_text[1:])
        s = "cmd:"+s
        return s
    else:
        print("❌ Không phải dữ liệu tọa độ (không bắt đầu bằng 'cmd:')")
        return False
def is_integer(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False
def Check_form_data(data_form):
    """Hàm này trả về ID của sản phẩm nến dữ liêu vượt qua bài kiểm tra dữ liệu vào, 
    nếu id sai thì sẽ trả lại  -1
    tiếp theo dũ liệu có bị trùng với dữ liệu đã có hay không"""
    print(data_form)
    try:
        device_id = data_form.get("deviceId")
        device_name = data_form.get("deviceName")
        number_of_trainings = data_form.get("number_trainings")
        shif_x = data_form.get("shif_x",-1)
        shif_y = data_form.get("shif_y",-1)
        shif_z = data_form.get("shif_z",-1)
        limit_x = data_form.get("limit_x",-1)
        limit_y = data_form.get("limit_y",-1)
        limit_z = data_form.get("limit_z",-1)
        limit_k = data_form.get("limit_k",-1)
        limit_x = int(limit_x)
        limit_y = int(limit_y)
        limit_z = int(limit_z)
        limit_k = int(limit_k)
        shif_X = int(shif_x)
        shif_Y = int(shif_y)
        shif_Z = int(shif_z)
        print("limit_x,limit_x,limit_x",limit_x,limit_y,limit_z,limit_k)
        if limit_x < 0 or limit_y < 0 or limit_z < 0 or limit_k < 0:
            print("Python nhận giới hạn âm sai")
            return -1 
        if not (SIZE_SHIFT_MIN <= shif_X <= SIZE_SHIFT_MAX):
            print("Du lieu shif_X khong hop le")
            return -1     
        if not (SIZE_SHIFT_MIN <= shif_Y <= SIZE_SHIFT_MAX):
            print("Du lieu shif_Y khong hop le")
            return -1
        if not (SIZE_SHIFT_MIN <= shif_Z <= SIZE_SHIFT_MAX):
            print("Du lieu shif_Z khong hop le")
            return -1
        try:
            int(device_id)
            int(number_of_trainings)
        except:
            print("❌ device_id không phải số nguyên")
            return -1
        print(f"📟 Thiết bị: ID={device_id}, Name={device_name},Number Of Training ={number_of_trainings}, shift=({shif_x}, {shif_y}, {shif_z})")
        point_x = data_form.getlist("point_x[]")
        point_y = data_form.getlist("point_y[]")
        point_z = data_form.getlist("point_z[]")
        point_k = data_form.getlist("point_k[]")
        for i in range(len(point_x)):
            try:
                x = int(point_x[i])
                if not (SIZE_X_MIN <= x <= SIZE_X_MAX):
                    print("Du lieu x khong hop le")
                    return -1
                y = int(point_y[i])
                if not (SIZE_Y_MIN <= y <= SIZE_Y_MAX):
                    print("Du lieu y khong hop le")
                    return -1
                z = int(point_z[i])
                if not (SIZE_Z_MIN <= z <= SIZE_Z_MAX):
                    print("Du lieu z khong hop le")
                    return -1
                k = int(point_k[i])
                if not (SIZE_K_MIN <= k <= SIZE_K_MAX):
                    print("Du lieu k (brightness) khong hop le")
                    return -1
            except Exception as e:
                print(f"⚠️ Lỗi tại điểm dầu {i+1}: {e}")
                return -1
        return True
    except Exception as e:
        print(f"❌ Lỗi tổng quát khi xử lý form: {e}")
        return -1

def return_point_change(point_current: int, shift_point: int, Min_type: int, Max_type: int):
    if point_current - shift_point < Min_type:
        print("❌ Dữ liệu bị lệch min")
        return False
    if point_current + shift_point > Max_type:
        print("❌ Dữ liệu bị lệch max")
        return False
    arr_return = [
        point_current + shift_point,
        point_current - shift_point
    ]
    return arr_return
def prcess_check_run_train(name_protype:str,shiftx:int, shifty:int, shiftz:int, arr_xyz, len_arr_xyz:int,queue_send_arm:queue,obj_manager_serial,data_web_rx, max_x = SIZE_X_MAX, min_x = SIZE_X_MIN, max_y = SIZE_Y_MAX, min_y = SIZE_Y_MIN, max_z = SIZE_Z_MAX, min_z = SIZE_Z_MIN):
    for i in range(len_arr_xyz):
        print(f"\n🔹 Chạy điểm dầu chính: x={arr_xyz[i]['x']}, y={arr_xyz[i]['y']}, z={arr_xyz[i]['z']} k ={arr_xyz[i]['k']}")
        from_data_send_run = f"cmd:{arr_xyz[i]['x']},{arr_xyz[i]['y']},{arr_xyz[i]['z']},{arr_xyz[i]['k']}"
        print(from_data_send_run)
        obj_manager_serial.send_data(from_data_send_run)
        status_send_arm = wait_for_specific_data(obj_manager_serial,from_data_send_run)
        data = {'productname':name_protype,'index':i,'lengt_index':len_arr_xyz,'training':1}
        queue_accept_capture.put(data)
        print("✅ Chạy chính thành công") if status_send_arm else print("❌ Chạy chính không thành công")
        for key, value in arr_xyz[i].items():
            if key == "x":
                arr_return = return_point_change(value, shiftx, min_x, max_x)
            elif key == "y":
                arr_return = return_point_change(value, shifty, min_y, max_y)
            elif key == "z":
                arr_return = return_point_change(value, shiftz, min_z, max_z)
            else:
                continue
            if arr_return is False:
                for retry in range(2):
                    print(f"❌ Lỗi tại {key.upper()} lần {retry + 1}: x={arr_xyz[i]['x']}, y={arr_xyz[i]['y']}, z={arr_xyz[i]['z']} k = {arr_xyz[i]['k']}")
                    from_data_send_run = f"cmd:{arr_xyz[i]['x']},{arr_xyz[i]['y']},{arr_xyz[i]['z']},{arr_xyz[i]['k']}"
                    print(from_data_send_run)
                    obj_manager_serial.send_data(from_data_send_run)
                    status_send_arm = wait_for_specific_data(obj_manager_serial,from_data_send_run)
                    print("✅ Chạy chính điểm phụ thành công") if status_send_arm else print("❌ Chạy phụ không thành công điểm chính ")
                    data = {'productname':name_protype,'index':i,'lengt_index':len_arr_xyz,'training':1}
                    queue_accept_capture.put(data)
            else:
                # Nếu OK thì chạy từng điểm thay đổi
                for k in range(2):
                    new_point = {
                        "x": arr_xyz[i]['x'],
                        "y": arr_xyz[i]['y'],
                        "z": arr_xyz[i]['z']
                    }
                    new_point[key] = arr_return[k]
                    print(f"✅ OK {key.upper()} lần {k}: x={new_point['x']}, y={new_point['y']}, z={new_point['z']} k = {arr_xyz[i]['k']} ")
                    from_data_send_run = f"cmd:{new_point['x']},{new_point['y']},{new_point['z']},{arr_xyz[i]['k']}"
                    obj_manager_serial.send_data(from_data_send_run)
                    status_send_arm = wait_for_specific_data(obj_manager_serial,from_data_send_run)
                    print("✅ Chạy lại điểm phụ thành công") if status_send_arm else print("❌ Chạy lại điểm  phụ không thành công điểm chính ")
                    data = {'productname':name_protype,'index':i,'lengt_index':len_arr_xyz,'training':1}
                    queue_accept_capture.put(data)
def run_and_capture(name_product,List_point,obj_manager_serial,cam_basler):
    """Trả về False nếu đã cố gắng chạy nhưng không thành công trả về true nếu chạy thành công"""
    print("name_product",name_product)
    print("List_point",List_point)
    length_list_point =  len(List_point)
    obj_manager_serial.clear_rx_queue()
    obj_manager_serial.clear_tx_queue()
    for i in range(length_list_point):
        from_data_send_run = f"cmd:{List_point[i].x},{List_point[i].y},{List_point[i].z},{List_point[i].brightness}"
        print(f"-------------------------------------Chạy lần thứ {i + 1 }-----------------------------")
        obj_manager_serial.send_data(from_data_send_run)
        status_send_arm = wait_for_specific_data(obj_manager_serial,from_data_send_run)
        if status_send_arm :
            print("✅Điểm Thành Công")
            img = cam_basler.capture_one_frame()
            cv2.imshow("anh1",img)
            cv2.waitKey(1)
            try:
                convert_jpg = frame_to_jpeg_bytes(img)
                if convert_jpg:
                    data_point = {
                        'index':i,
                        'length':length_list_point,
                        'img':convert_jpg
                    }
                    try:
                        queue_tx_web_main.put(data_point, timeout=0.1)
                        print("✅ Đưa ảnh vào queue thành công")
                    except queue.Full:
                        print("⚠️ Queue đầy, bỏ qua frame này")
                    print("ConVert gửi trong queue Thành công!")
            except:
                print("Có lỗi gì ở bước chuyển ảnh")
        else :
            print("❌ Chạy lại điểm  phụ không thành công điểm chính ")
           
       

def frame_to_jpeg_bytes(frame, quality=90) -> bytes:
    """
    Chuyển từ numpy array (frame BGR) sang JPEG bytes.
    """
    ok, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return buffer.tobytes() if ok else None


    
def get_path_from_static(full_path):
        parts = full_path.split("static", 1)
        if len(parts) > 1:
            return "static" + parts[1]
        else:
            return None
def read_file_training(name_file:str,queue_send_arm:queue,obj_manager_serial,data_web_rx):
    try:
        with open(name_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        print("✅ Đọc file thành công")
        data = content['data']
        device_id = data['device_id']
        device_name = data['device_name']
        shif_x = int(data['shif_x'])
        shif_y = int(data['shif_y'])
        shif_z = int(data['shif_z'])
        points = data['points']
        print(f"📟 Thiết bị: ID={device_id}, Name={device_name}, shift=({shif_x}, {shif_y}, {shif_z})")
        print(points)
        prcess_check_run_train(device_name,shif_x,shif_y,shif_z,points,len(points),queue_send_arm,obj_manager_serial = obj_manager_serial,data_web_rx = data_web_rx)
        return content
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {name_file}'")
        return False
    except Exception as e:
        print("❌ Lỗi khác:", e)
        return False
def create_folder_in_static(subfolder_name: str) -> str:

    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, "static")
    subfolder_path = os.path.join(static_dir, subfolder_name)

    # Tạo folder cha (static) và folder con
    os.makedirs(subfolder_path, exist_ok=True)

    print(f"📁 Đã tạo thư mục: {subfolder_path}")
    return subfolder_path
def create_choose_master(name_location_save_in_static: str):
    """Hàm này sẽ luôn tạo 1 file nằm trong static/name_location_save_in_static nếu không có thì nó sẽ tạo vào khởi giá trị
    ban đầu là 0 nếu có rồi thì nó sẽ không làm gì cả
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, "static")
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, name_location_save_in_static)
    if not os.path.exists(file_path):
        print("File không tồn tại, tạo mới.")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("0")
    else:
        print("File đã tồn tại, sẽ đọc nội dung.")
def write_data_to_file(filename: str, content: str, append: bool = False) -> None:
    """
    Ghi dữ liệu vào file trong thư mục static.
    - append = False: ghi đè nội dung file
    - append = True: ghi thêm vào cuối file
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(current_dir, "static")
        os.makedirs(static_dir, exist_ok=True)
        file_path = os.path.join(static_dir, filename)
        mode = "a" if append else "w"
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(content + "\n")
        action = "Thêm vào" if append else "Ghi đè"
        print(f"✅ {action} file '{filename}' thành công.")
    except:
        print(f"X {action} file '{filename}' lỗi thành công.")

def clear_file_content(filename: str) -> None:
    """
    Làm rỗng nội dung file (giữ lại file nhưng xóa toàn bộ dữ liệu bên trong).
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, "static")
    file_path = os.path.join(static_dir, filename)

    if os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.truncate(0)  # Xóa toàn bộ nội dung
        print(f"🧹 Đã xóa toàn bộ nội dung trong file '{filename}'.")
    else:
        print(f"❌ File '{filename}' không tồn tại để xóa nội dung.")
def read_data_from_file(filename: str) -> str:
    """
    Đọc toàn bộ nội dung từ file trong thư mục static có tên là filename
    Trả về chuỗi nội dung, hoặc chuỗi rỗng nếu file không tồn tại.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, "static")
    file_path = os.path.join(static_dir, filename)
    if not os.path.exists(file_path):
        print(f"❌ File '{filename}' không tồn tại.")
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"📄 Đọc nội dung từ file '{filename}' thành công.")
        return content
def get_image_paths_from_folder(folder_path: str) -> list:
    """
    Trả về danh sách đường dẫn các file nằm trong folder_path.
    Đường dẫn đầu ra có định dạng chuẩn cho Flask (dùng dấu /).
    Args:
        folder_path (str): Đường dẫn thư mục (ví dụ: 'static/Master_Photo/Master_Loại A')
    Returns:
        list: Danh sách các đường dẫn file (ví dụ: ['static/Master_Photo/Master_Loại A/image1.jpg', ...])
    """
    image_paths = []

    # Đường dẫn tuyệt đối trên hệ thống
    abs_folder_path = os.path.join(os.path.dirname(__file__), folder_path)

    if os.path.exists(abs_folder_path) and os.path.isdir(abs_folder_path):
        for file in os.listdir(abs_folder_path):
            file_path = os.path.join(abs_folder_path, file)
            if os.path.isfile(file_path):
                # Chuẩn hóa dấu `/` để Flask hiểu đúng
                normalized_path = os.path.join(folder_path, file).replace("\\", "/")
                image_paths.append(normalized_path)
    return image_paths
