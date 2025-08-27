from flask import Flask
from flask import Flask,request,jsonify
from flask import Blueprint,render_template
from flask_socketio import SocketIO
from connect_camera import BaslerCamera
from flask import redirect, url_for
from producttypemanager import ProductTypeManager
import check_shape
import threading
import time
import func
import json

#static varialble--------------
NAME_FILE_CHOOSE_MASTER = "choose_master"

#Class -------------------------
main_html = Blueprint("main",__name__)
api = Blueprint("api",__name__)
api_new_model = Blueprint("api_new_model",__name__)
api_choose_master = Blueprint("api_choose_master",__name__)
api_take_master = Blueprint("api_take_master",__name__)
api_run_application = Blueprint("api_run_application",__name__)
api_new_product = Blueprint("api_new_product",__name__)
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
manage_product = ProductTypeManager()
cam_basler = None

#-------open thread--------
OPEN_THREAD_LOG =  True
OPEN_THREAD_STREAM =  True
OPEN_THREAD_IMG = True
#soket io
@socketio.on('connect', namespace='/video')
def handle_video_connect():
    print("📡 Client connected to /video")
@socketio.on('connect', namespace='/log') 
def handle_log_connect():
    print("📡 Client connected to /log")
def stream_frames():
    cam_basler.acc_run = True
    global OPEN_THREAD_STREAM
    OPEN_THREAD_STREAM = True
    while OPEN_THREAD_STREAM:
         cam_basler.run_cam_html()
    cam_basler.release()
    print("Thoát luồng gửi video thành công")
 
#queue_tx_web_main
def stream_img():
    global OPEN_THREAD_IMG
    while OPEN_THREAD_IMG:
        if queue_tx_web_main.qsize() > 0:
            data = queue_tx_web_main.get(block=False)
            socketio.emit("photo_taken", data, namespace="/video")
        time.sleep(0.1)

    
def stream_logs():
    while OPEN_THREAD_LOG:
        with main_pc.manage_product_type_lock:
            socketio.emit("log_message_product", {"manage_product_type": main_pc.manage_product_type.return_data_dict_all()}, namespace='/log')
        # queue_tx_web_log.put("🔔 Thông báo từ server")   #cab gui gi thi gui vao log nay
        if not queue_tx_web_log.empty():
            socketio.emit("log_message", {"log_training": f"{queue_tx_web_log.get()}"}, namespace='/log')
        time.sleep(1)

# Blueprint main---------------------------------------------------------------------------------
@main_html.route("/")
def show_main():
    """Là hàm hiển thị giao diện chính trên Html"""
    func.create_choose_master(NAME_FILE_CHOOSE_MASTER) #tạo file choose_master nếu tạo rồi thì thôi
    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)#đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    #------------------------------------------------ Thay the bang file kia nha
    # choose_master_index =  choose_master_index.strip()
    # test = manage_product.find_by_id(choose_master_index)
    # print("test",test)
    # if(test == -1):
    #     print("Tim khong thanh cong")
    # else:
    #     print("Tim thanh cong")
    # check_shape.check_shapes()
    #------------------------------------------------------------
    arr_type_id = manage_product.get_list_id_product()
    # print("arr_type_id :",arr_type_id)
    # print("choose_master_index :",choose_master_index)
    main_pc.click_page_html = 1  # thong bao dang o trang web chinh
    data_strip = choose_master_index.strip() 
    if data_strip in  arr_type_id:
        print(f"gui data master co ten {choose_master_index}")
        path_arr_img = manage_product.get_list_path_master_product_img_name(data_strip)
        # print(path_arr_img)
        return render_template("show_main.html",path_arr_img = path_arr_img)
    return render_template("show_main.html",path_arr_img = None)
@main_html.route('/out_app', methods=['GET'])
def out_app():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Server không hỗ trợ shutdown trực tiếp")
    func()
   
    OPEN_THREAD_LOG =  False
    
    print("Người dùng thoát tab")
    return jsonify({"status":"OK"})

#chua dinh nghia
@api.route("/master-setting")
def master_setting():
    # func.clear_queue(queue_rx_web_api)   #rst bufff nhan
    main_pc.click_page_html = 3           # che do config master
    return render_template("master_setting.html")
#--------------------------------------------------------Api_run_application---------------------------------------------
@api_run_application.route('/run_application',methods = ['GET'])
def run_application():
    """Hàm này đê chạy run khi người dùng nhấn "chạy" trên giao diện chính"""
    main_pc.is_run = 1      #bat bien Run len bat dau qua trinh chay
    print("Đã nhấn nút Run application")
    return jsonify({"status":"OK"})
#--------------------------------------------------------Api_master_take---------------------------------------------

@api_take_master.route("/master_take",methods=["POST"])
def master_take():
    data = request.get_json()
    print(data)   
    return jsonify({'status':"OKE"})
@api_take_master.route("/config_master",methods=["POST"])
def config_master():
    data = request.get_json()
    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER) # đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    print(data)   
    # status = check_shape.check_shapes(data)
    check_shape.save_shapes_to_json(data,"shapes.json")
    print("--------------------------------Luu Thanh cong-------------------")
    # if(status):
    #     print("--------------------------------dU LIEU CHUA CHUAN-------------------")
    # else :
    #     print("--------------------------------dU LIEU DA  CHUAN---------------------")
    
    return jsonify({'status':"OKE"})
#--------------------------------------------------------Api_new_product ---------------------------------------------
import os
@api_new_product.route("/add")
def add():
     return render_template("save_product_new.html")
# @api_new_product.route("/upload", methods=["POST"])
# def upload():
#     try:
#         product_id = request.form.get("product_id",-1)
#         product_name = request.form.get("product_name",-1)
#         limit_x = request.form.get("limit_x",-1)
#         limit_y = request.form.get("limit_y",-1)
#         limit_z = request.form.get("limit_z",-1)
#         print(product_id,product_name,limit_x,limit_y,limit_z)
#         if product_id  == -1 or product_name  == -1 or limit_x == -1 or limit_y == -1 or limit_z == -1:
#               print("1 trong ca cacs gias tri server gui Khong co")
#         return jsonify({"success": True, "msg": "Đã chọn ảnh "})
#     except:
#         return jsonify({"success": False, "msg": "Chưa chọn ảnh"})

@api_new_product.route("/upload", methods=["POST"])
def upload_product():
    # ---- Lấy dữ liệu text từ form ----
    product_id = request.form.get("product_id")
    product_name = request.form.get("product_name")
    limit_x = request.form.get("limit_x")
    limit_y = request.form.get("limit_y")
    limit_z = request.form.get("limit_z")
    # ---- Lấy file từ form ----
    file = request.files.get("file_upload")   # "file_upload" = name trong <input type="file">
    #can viet ham kiem tra tren day 
    if not file:
        return jsonify({"success": False, "error": "Không có file được gửi"}), 400
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    try:
        product_id = int(product_id)
        limit_x = int(limit_x.strip())
        limit_y = int(limit_y.strip())
        limit_z = int(limit_z.strip())
    except:
        print("Dữ liệu gưi về lỗi")
    manage_product.add_product_type(product_id,product_name,[limit_x,limit_y,limit_z])
    # ---- Lưu file ----
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # ---- Trả kết quả về client ----
    return jsonify({
        "success": True,
        "product_id": product_id,
        "product_name": product_name,
        "limit_x": limit_x,
        "limit_y": limit_y,
        "limit_z": limit_z,
        "filename": file.filename,
        "filepath": filepath
    })

#--------------------------------------------------------Api_choose_master---------------------------------------------
@api_choose_master.route("/get_show_main",methods = ["POST"])
def get_content():
    json_data = request.get_json()
    choose_master = json_data.get('data')
    print(f"Master được chọn là : {choose_master}")
    func.clear_file_content(NAME_FILE_CHOOSE_MASTER)
    func.write_data_to_file(NAME_FILE_CHOOSE_MASTER,choose_master)
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)
@api_choose_master.route("/chose_product")
def chose_product():
    data =  manage_product.get_file_data()
    print("DUONG Dan anh gui len laaaaaaaa",data)
    print(data)
    return render_template("chose_product.html",data = data)
#--------------------------------------------------------Api_new_model----------------------------------------------

@api_new_model.route('/stop-video', methods=['POST'])
def stop_video():
    main_pc.click_page_html = 1
    global OPEN_THREAD_STREAM
    OPEN_THREAD_STREAM = False
    cam_basler.acc_run = False
    print("Người dùng đã thoát khỏi trang Training Model")
    return "ok"
@api_new_model.route('/replay', methods=['GET'])
def handle_replay():
    main_pc.is_data_train = 1
    print("🔁 Người dùng đã nhấn nút replay!")
    return jsonify({
        "message": "Đã nhận tín hiệu từ nút Replay",
        "status": "ok"
    })
@api_new_model.route("/run_point",methods=['POST'])
def run_point():                       
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    brightness = data.get('brightness')
    data_send = f"cmd:{x},{y},{z},{brightness}"
    print(f'x ={x}, y = {y}, z = {z} brightness ={brightness}')
    queue_rx_web_api.put(data_send)
    return jsonify({"message": "Ok"})

@api_new_model.route("/run_all_points", methods=["POST"])
def run_all_points():
    data = request.get_json()
    points = data.get("points", [])
    print(f"📥 Nhận {len(points)} điểm dầu:")
    for i, p in enumerate(points):
        print(f"  • Điểm {i+1}: x={p['x']}, y={p['y']}, z={p['z']}, k={p['k']}")
        data_send = f"cmd:{p['x']},{p['y']},{p['z']},{p['k']}"
        queue_rx_web_api.put(data_send)
        time.sleep(2)
    return jsonify({"message": f"Đã nhận {len(points)} điểm dầu"})
@api_new_model.route("/exit-training")
def exit_training():
    main_pc.click_page_html = 1
    global OPEN_THREAD_STREAM
    OPEN_THREAD_STREAM = False
    cam_basler.acc_run = False
    print("Người dùng đã thoát khỏi trang Training Model")
    return redirect(url_for("main.show_main"))
# @api_new_model.route("/get_status")
# def get_status():
#     param = request.args.get("param1")
#     print(f"Client hỏi trạng thái với param1 = {param}")
#     if param == "status_connect":
#         print("Trạng thái connect hiện tại ",main_pc.STATUS_CHECK_CONNECT)
#         if(main_pc.STATUS_CHECK_CONNECT==0 ):   #trang thai ket noi
#             return "0"
#         elif(main_pc.STATUS_CHECK_CONNECT==1):
#             return "1"                        
#         else:
#             return "2" 
@api_new_model.route('/submit', methods=['POST']) 
def submit():
    """Training khong the anh huong truc tiep den file chay hayg lam tap trung vao master lay master."""
    form_data = request.form 
    status_check_submit = func.Check_form_data(form_data)  #status_check_submit co thể la typeid
    print(status_check_submit)
    if status_check_submit:
        queue_tx_web_log.put("🔔Dữ liệu hợp lệ")
        queue_tx_web_log.put("🔔Tiến hành Traing Data")
        #Gui Tin hieu vao file main
        main_pc.is_data_train = 1
    else:
        queue_tx_web_log.put("🔔Dữ liệu không hợp lệ") 
        return "X Dữ liệu không hợp lệ"
    return "✅ Đã nhận dữ liệu"
@api_new_model.route("/training-model")
def take_photo_trainning_model():
    threading.Thread(target = stream_frames,daemon=True).start()
    func.clear_queue(queue_rx_web_api)   #rst bufff nhan
    main_pc.click_page_html = 2
    return render_template("take_photo.html")
#--------------------------------------------------------end Api----------------------------------------------
app.register_blueprint(main_html)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(api_new_model, url_prefix="/api_new_model")
app.register_blueprint(api_choose_master, url_prefix="/api_choose_master") 
app.register_blueprint(api_take_master, url_prefix="/api_take_master")  
app.register_blueprint(api_run_application, url_prefix="/api_run_application") 
app.register_blueprint(api_new_product, url_prefix="/api_new_product") 
from shared_queue import queue_accept_capture
cam_basler = BaslerCamera(queue_accept_capture, socketio, config_file="Camera_25129678.pfs")
if __name__ == "__main__":
    import main_pc
    from shared_queue import queue_rx_web_api,queue_tx_web_log,queue_tx_web_main
    import threading
    threading.Thread(target=stream_logs).start()
    threading.Thread(target=stream_img).start()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)



       