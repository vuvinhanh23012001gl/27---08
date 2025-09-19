from process_master import  Proces_Shape_Master
from point_oil_detected_manage import Manage_Point_Oil_Detect
from ultralytics import YOLO
from folder_create import Create
from master_circle_shape import  Master_Circle_Shape
from master_rect_shape import  Master_Rect_Shape
import cv2
import numpy as np
class Judget_Product:

    """Lớp này chỉ phán định sản phẩm có 
    lớp này chỉ khởi tạo 1 lần
    OK hay NG"""

    folder =  Create()
    file_path = folder.create_file_in_folder_two("best.pt","model")
    model = YOLO(file_path)

    def __init__(self):
        pass
    def judget(self,ID:str,atitude_z,index_picture,img:np.ndarray,master_shape:Proces_Shape_Master):
            """Khi cho 1 bức ảnh vào thì nó sẽ phán định ok hay ng"""
            print(f"Phán định ID{ID} tại Index:{index_picture}")
            data_id = master_shape.get_data_is_id(ID)
            if data_id:
                data_regulation = Judget_Product.model(img)                                                  # Dữ liệu đi ra từ mô hình 
                object_one_point_detect = Manage_Point_Oil_Detect(data_regulation,atitude_z)                 # Đưa vào đối tượng điểm của mô hình
                polygons = object_one_point_detect.get_contourn_polygon_standardization()                    # Lấy các điểm bao 
                if not polygons:
                    print(f"Không có điểm dầu hoặc không phát hiện điểm dầu trong ảnh thứ:{index_picture} của ID:{ID}")
                    #Phan nay cần phải thêm Logic xem điểm dầu hợp lệ hay không
                # object_one_point_detect.draw_all()                                                         # Vẽ các điểm dầu
                # print(data_one_point_master)
                img = self.draw_polylines_on_image(img,polygons)   
                data_one_point_master = master_shape.get_data_shape_of_location_point(ID,index_picture)
                arr_object_shape = [] 
                if not data_one_point_master:
                    print("Dữ liệu không đúng")
                    return False                 
                for shape in data_one_point_master:
                    if shape["type"] == "circle":
                        shape_object = Master_Circle_Shape(shape)
                                #  img  = shape_object.draw(img)
                        arr_object_shape.append(shape_object)
                    elif shape["type"] == "rect":
                        shape_object = Master_Rect_Shape(shape)
                                #  img  = shape_object.draw(img)
                        arr_object_shape.append(shape_object)
                if not arr_object_shape:
                    print("Không có dữ liệu master trong ảnh thứ:{index_picture} của ID:{ID}")
                is_frame_ok = True
                for shape_master in arr_object_shape:
                     arr_specified_size_data = []
                     img  = shape_master.draw(img)
                     name = shape_master.get_name()
                     data_area = shape_master.area(img)
                     print(f"------------------------Kiểm tra vùng  Master:{name}-------------------------------")
                     is_inside = True         
                     index_detect_point = 0
                     count_oil_in_point = 0
                     for poly in polygons:   
                        object_point = object_one_point_detect.get_object_index_area_while(index_detect_point) #Trả về đối tượng từng điểm ảnh phát hiện đc
                        index_detect_point += 1
                        dict_data_detect = shape_master.contains_polygon(poly, img)
                        status = dict_data_detect.get("status",-1)
                        inside_percent = dict_data_detect.get("inside_percent",-1)
                        if inside_percent == -1 or status == -1:
                            print("Lỗi dữ liệu output")
                        if status == "inside":
                            print(f"--Thuộc tính điểm thứ {count_oil_in_point + 1} phát hiện ra--")
                            width_reality = max(object_point.estimate_area_with_calib(atitude_z,object_one_point_detect.calib_Z,object_one_point_detect.calib_scale))
                            print("--Vật thể")
                            print(f"Khung {name} có điểm {count_oil_in_point + 1} max đường kính thực tế của vật thể :{width_reality} mm")
                            print(f"Khung {name} có điểm {count_oil_in_point + 1} số px trắng phát hiện là :{object_point.count_mask_white_pixels()} px")
                            print("--Master quy định")
                            print(f"Kích thước điểm dầu MIN :{shape_master.size_min} MAX: {shape_master.size_max}")
                            if(width_reality >shape_master.size_max or width_reality < shape_master.size_min):
                                specified_size_data = {"name_master":name,"name_point":count_oil_in_point + 1}
                                arr_specified_size_data.append(specified_size_data)
                            print(f"Khung {name} có điểm {count_oil_in_point + 1} master quy định nằm trong hình:{data_area["shape"]} có diện tích khung là:{data_area["area"]} px")
                            print("Phán định")
                            print(f"Tỷ lệ chiếm của điểm {count_oil_in_point + 1} với khung master :{self.calc_area_percentage(object_point.count_mask_white_pixels(),data_area["area"])} %")
                            print(f"{inside_percent} % nằm trọn trong khung")
                            print(f"==> Điểm {count_oil_in_point + 1} nằm trong khung {name}")
                            count_oil_in_point +=1
                            is_inside =  True
                        if status == "partial":
                             print(f"Khung {name} phát hiện {inside_percent} % nằm một phần trong khung")
                     if not is_inside:
                        print(f"Hình {name} có không có Polygon nằm trong")
                     print(f"Khung {name} số lượng điểm phát hiện nằm trong là :{count_oil_in_point} và master đặt là:{shape_master.number_point}")
                     if count_oil_in_point != shape_master.number_point:
                         print(f"=>Số lượng điểm phát hiện khác với quy định")
                         is_frame_ok =  False
                     else:
                          print(f"=>Số lượng điểm phát hiện giống với quy định")
                          if len(arr_specified_size_data) > 0:
                              print("Tìm được những điểm dầu sau không đúng với kích thước quy định",arr_specified_size_data)
                              is_frame_ok =  False
                     print("------------------------END master-------------------------------")
                if is_frame_ok:
                     print("=======================> Bức Hình OK")
                else:
                     print("=======================> Bức Hình NG")
                # cv2.imshow("Processing IMG",img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            else:
                print("Không tìm thấy ID")


    def calc_area_percentage(self,area_shape, area_frame):
        """
        Tính tỷ lệ % diện tích của hình so với diện tích khung
        - area_shape: diện tích của hình
        - area_frame: diện tích khung (lớn hơn 0)
        """
        if area_frame <= 0:
            raise ValueError("Diện tích khung phải lớn hơn 0")

        percent = (area_shape / area_frame) * 100
        return percent

    def draw_polylines_on_image(self, image, polygons=None):
        """
        image: numpy array (H, W, 3) ảnh RGB
        shapes: list chứa dict (rect hoặc circle)
        polygons: list các contour (numpy array Nx2) giá trị normalized [0-1]
        """
        h, w = image.shape[:2]
        print("height", h)
        print("width", w)
        result = image.copy()
        # Vẽ polygons nếu có
        if polygons is not None:
            for poly in polygons:
                pts = np.array([[int(x * w), int(y * h)] for x, y in poly], dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(result, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            return result

       
    

    
# PATH_MODEL = r"C:\Users\anhuv\Desktop\26_08\25-08\app\app\static\Master_Photo\Master_SP01\img_6.png"  
# img = cv2.imread(PATH_MODEL)  
# class_regulation = Proces_Shape_Master()

# judget1 = Judget_Product()
# judget1.judget("SP01",0,6,img,class_regulation)



# judget1 = Judget_Product(class_regulation)
# list_id = judget1.get_list_id()
# print(list_id)





