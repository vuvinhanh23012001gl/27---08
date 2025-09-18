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

    def __init__(self,master_shape:Proces_Shape_Master):
        self.master_shape = master_shape
  
    def judget(self,ID:str,atitude_z,index_picture,img:np.ndarray):
            """Khi cho 1 bức ảnh vào thì nó sẽ phán định ok hay ng"""
            print(f"Phán định ID{ID} tại Index:{index_picture}")
            data_id = self.master_shape.get_data_is_id(ID)
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
                arr_object_shape = self.load_object(ID,index_picture)
                if not arr_object_shape:
                    print("Không có dữ liệu master trong ảnh thứ:{index_picture} của ID:{ID}")
                for shape_master in arr_object_shape:
                     img  = shape_master.draw(img)
                     name = shape_master.get_name()
                     data_area = shape_master.area(img)
                     print(f"------------------------Kiểm tra vùng  Master:{name}-------------------------------")
                     is_inside = False         
                     index_detect_point = 0
                     count_oil_in_point = 0
                     for poly in polygons:   
                        object_point = object_one_point_detect.get_object_index_area_while(index_detect_point) #Trả về đối tượng từng điểm ảnh phát hiện đc
                        index_detect_point += 1
                        if shape_master.contains_polygon(poly, img):
                            width_reality = max(object_point.estimate_area_with_calib(atitude_z,object_one_point_detect.calib_Z,object_one_point_detect.calib_scale))
                            print(f"Hình {name} đường kính thực tế max điểm dầu thực tế là :{width_reality} mm")
                            print(f"Hình {name} là hình {data_area["shape"]}  có diện tích khung là:{data_area["area"]}")
                            print(f"Kích thước điểm dầu MIN :{shape_master.size_min} MAX: {shape_master.size_max}")
                            print(f"Hình {name} có diện tích vùng phát hiện là:{object_point.count_mask_white_pixels()}")
                            print(f"Tỷ lệ chiếm {self.calc_area_percentage(object_point.count_mask_white_pixels(),data_area["area"])}")
                            print(f"Hình {name} có Polygon nằm trong")
                            count_oil_in_point +=1
                            is_inside =  True
                     print(f"Số điểm dầu hợp lệ nằm trong khung quy định của điểm {name}là: {count_oil_in_point}")
                     print(f"Số điểm dầu hợp lệ mater quy định {name}là: {shape_master.number_point}")
                     if not is_inside:
                        print(f"Hình {name} có không có Polygon nằm trong")
                     print("------------------------END master-------------------------------")
                cv2.imshow("Processing IMG",img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
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

    def load_object(self,ID,index_picture):
        data_one_point_master = self.master_shape.get_data_shape_of_location_point(ID,index_picture)
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
        return arr_object_shape
             
                


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

       
    

    
PATH_MODEL = r"C:\Users\anhuv\Desktop\26_08\25-08\app\app\static\Master_Photo\Master_SP01\img_0.png"  

img = cv2.imread(PATH_MODEL)  
class_regulation = Proces_Shape_Master()


judget1 = Judget_Product(class_regulation)
judget1.judget("SP01",2,0,img)



# judget1 = Judget_Product(class_regulation)
# list_id = judget1.get_list_id()
# print(list_id)





