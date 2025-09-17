import cv2
import func
import numpy as np
class Master_Rect_Shape:
    def __init__(self,shape):
        """
        Đại diện 1 hình chữ nhật
        - (x1, y1): góc trên trái
        - (x2, y2): góc dưới phải
        """
        self.shape = shape
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.corners = None
        self.name = None
        self.rotation =  None
        self.size_max = None
        self.size_min = None
        self.compatible_max = None
        self.compatible_min = None
        self.Init()
    def draw(self, img, color=(255, 0, 0)):
        h, w = img.shape[:2]
        print("self.corners", self.corners)

        if self.corners and self.corners != -1:
            # Lấy 4 điểm corners (chuẩn hóa -> pixel)
            pts = np.array([[int(c["x"] * w), int(c["y"] * h)] for c in self.corners], dtype=np.int32)

            # Vẽ polygon từ corners
            cv2.polylines(img, [pts], isClosed=True, color=color, thickness=2)
           

            # Tính tâm polygon
            cx, cy = np.mean(pts, axis=0).astype(int)
            # Vẽ tên tại đỉnh đầu tiên
            cv2.putText(img, func.remove_vietnamese_tone(self.name), (cx-10, cy-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        else:
            # Vẽ bounding box nếu không có corners
            x1, y1 = int(self.x1 * w), int(self.y1 * h)
            x2, y2 = int(self.x2 * w), int(self.y2 * h)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, func.remove_vietnamese_tone(self.name), (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    def Init(self):
        self.name = self.shape.get("ten_hinh_min",-1)
        self.x1 = self.shape.get("x1",-1)
        self.y1 = self.shape.get("y1",-1)
        self.x2 = self.shape.get("x2",-1)
        self.y2 = self.shape.get("y2",-1)
        self.corners = self.shape.get("corners",-1)
        
        self.rotation = self.shape.get("rotation",None)

        self.size_max = self.shape.get("kich_thuoc_max",-1)
        self.size_min = self.shape.get("kich_thuoc_min",-1)

        self.compatible_max = self.shape.get("tuong_thich_max",-1)
        self.compatible_min = self.shape.get("tuong_thich_min",-1)
        
        if(self.corners == -1):
            print(f"Hình {self.name} không xoay")
        if( self.name  == -1 or self.x1 ==-1 or self.y1 == -1 or self.x2  == -1 or self.y2   == -1 or self.size_max  == -1 or self.size_min  == -1 or  self.compatible_max  == -1 or  self.compatible_min  == -1 ):
            print("Lỗi init dũ liệu hình vuông không đúng")
        else:
            print(f"Init thành công điểm {self.name}")