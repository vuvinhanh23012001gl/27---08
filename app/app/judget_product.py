from process_master import  Proces_Shape_Master
from point_oil_detected_manage import Manage_Point_Oil_Detect
from ultralytics import YOLO
from folder_create import Create
from master_circle_shape import Master_Circle_Shape
from master_rect_shape import Master_Rect_Shape
import cv2
import numpy as np
class Judget_Product:
    """Lớp này chỉ phán định sản phẩm có 
    lớp này chỉ khởi tạo 1 lần
    OK hay NG"""
    folder =  Create()
    file_path = folder.create_file_in_folder_two("best.pt","model")
    model = YOLO(file_path)
  
    def __init__(self,master_shape:Proces_Shape_Master):
        self.master_shape = master_shape
        self.arr_object_shape = []
        self.Init()
    def judget(self,ID:str,index_picture,img:np.ndarray):
            data_id = self.master_shape.get_data_is_id(ID)
            if data_id:
                data_one_point_master = self.master_shape.get_data_shape_of_location_point(ID,index_picture) # Dữ liệu master 
                for shape in data_one_point_master:
                    # if shape["type"] == "circle":
                    #      shape_object = Master_Circle_Shape(shape)
                    #      self.arr_object_shape.append(shape_object)
                    # elif shape["type"] == "rect":
                    #      shape_object = Master_Rect_Shape(shape)
                    #      self.arr_object_shape.append(shape_object)
                        pass
    def Init(self,ID:str,index_picture):
        data_id = self.master_shape.get_data_is_id(ID)
        if data_id:
                data_one_point_master = self.master_shape.get_data_shape_of_location_point(ID,index_picture) # Dữ liệu master 
                for shape in data_one_point_master:
                    if shape["type"] == "circle":
                         shape_object = Master_Circle_Shape(shape)
                         self.arr_object_shape.append(shape_object)
                    elif shape["type"] == "rect":
                         shape_object = Master_Rect_Shape(shape)
                         self.arr_object_shape.append(shape_object)
                        
             




                # data_regulation = Judget_Product.model(img)                                                  # Dữ liệu đi ra từ mô hình 
                # object_one_point_detect = Manage_Point_Oil_Detect(data_regulation,10)                        # Đưa vào đối tượng điểm của mô hình
                # polygons = object_one_point_detect.get_contourn_polygon_standardization()                    # Lấy các điểm bao 
                # # object_one_point_detect.draw_all()                                                         # Vẽ điểm dầu
                # self.draw_shapes_on_image(img,data_one_point_master,polygons)                                # Vẽ các điểm bao
                # print(data_one_point_master)
                    


    def draw_shapes_on_image(self, image, shapes, polygons=None):
        """
        image: numpy array (H, W, 3) ảnh RGB
        shapes: list chứa dict (rect hoặc circle)
        polygons: list các contour (numpy array Nx2) giá trị normalized [0-1]
        """
        h, w = image.shape[:2]
        print("height", h)
        print("width", w)
        result = image.copy()
        # Vẽ rect & circle
        for shape in shapes:
            color = (0, 0, 255)  # mặc định vẽ đỏ
            if shape.get("color") == "blue":
                color = (255, 0, 0)

            if shape["type"] == "rect":
                x1, y1 = int(shape["x1"] * w), int(shape["y1"] * h)
                x2, y2 = int(shape["x2"] * w), int(shape["y2"] * h)
                cv2.rectangle(result, (x1, y1), (x2, y2), color, 2)
                cv2.putText(result,self.remove_vietnamese_tone(shape["ten_hinh_min"]), (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            elif shape["type"] == "circle":
                cx, cy = int(shape["cx"] * w), int(shape["cy"] * h)
                r = int(shape["r"] * w)   # scale bán kính theo width
                cv2.circle(result, (cx, cy), r, color, 2)
                cv2.putText(result,self.remove_vietnamese_tone(shape["ten_hinh_min"]), (cx, cy - r - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        # Vẽ polygons nếu có
        if polygons is not None:
            for poly in polygons:
                pts = np.array([[int(x * w), int(y * h)] for x, y in poly], dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(result, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.imshow("Processing IMG",result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
       
    

    
PATH_MODEL = r"C:\Users\anhuv\Desktop\26_08\25-08\app\app\static\Master_Photo\Master_SP01\img_2.png"  
img = cv2.imread(PATH_MODEL)  

class_regulation = Proces_Shape_Master()


judget1 = Judget_Product(class_regulation)
judget1.judget("SP01",2,img)



# judget1 = Judget_Product(class_regulation)
# list_id = judget1.get_list_id()
# print(list_id)





