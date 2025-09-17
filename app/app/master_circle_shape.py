import cv2
import func
class Master_Circle_Shape():
    def __init__(self,shape):
        self.shape =  shape
        self.name = None
        self.x = None
        self.y = None
        self.r = None
        self.init()
    def init(self):
         self.name = self.shape.get("ten_hinh_min",-1)
         self.x = self.shape.get("cx",-1)
         self.y = self.shape.get("cy",-1)
         self.r = self.shape.get("r",-1)
         if( self.name  == -1 or self.x ==-1 or self.y == -1 or self.r == -1):
            print("Lỗi init dũ liệu hình tròn không đúng")
    def draw(self, img, color=(0, 255, 0)):
        """
        Vẽ hình tròn trực tiếp từ chính object này chỉ vẽ thôi không làm thay đổi dữ liệu
        """
        # Vẽ hình tròn
        h, w = img.shape[:2]
        cx, cy, rx = int(self.x * w), int(self.y * h),(int(self.r * w))
        cv2.circle(img,(cx,cy),rx, color, 2)
        if self.name:
            cv2.putText(img,func.remove_vietnamese_tone(self.name),
                        (cx, cy - rx - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, color, 1)
        return img
    
    
    