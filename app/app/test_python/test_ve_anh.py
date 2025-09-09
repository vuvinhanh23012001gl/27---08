import cv2

# Đọc ảnh gốc
image = cv2.imread(r"C:\Users\anhuv\Desktop\26_08\25-08\app\app\test_python\img_0.png")

# Kích thước canvas hiển thị
canvas_w, canvas_h = 1328, 830

# Kích thước ảnh thật
real_w, real_h = 1920, 1200

# Hệ số scale
scale_x = real_w / canvas_w
scale_y = real_h / canvas_h

# Data rect trên canvas
shape = {
    "x1": 567,
    "y1": 73,
    "x2": 712,
    "y2": 166,
    "ten_hinh_min": "Diem1"
}

# Chuyển sang tọa độ thật
x1 = int(shape["x1"] * scale_x)
y1 = int(shape["y1"] * scale_y)
x2 = int(shape["x2"] * scale_x)
y2 = int(shape["y2"] * scale_y)

# Vẽ
color = (255, 0, 0)
cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
cv2.putText(image, shape["ten_hinh_min"], (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

cv2.imshow("Shapes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
