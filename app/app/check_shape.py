import math
import json
import os
# --- Hỗ trợ hình học ---
def pointInPolygon(point, polygon):
    """Thuật toán ray-casting kiểm tra điểm trong polygon"""
    x, y = point["x"], point["y"]
    inside = False
    n = len(polygon)
    for i in range(n):
        j = (i - 1) % n
        xi, yi = polygon[i]["x"], polygon[i]["y"]
        xj, yj = polygon[j]["x"], polygon[j]["y"]
        intersect = ((yi > y) != (yj > y)) and \
                    (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi)
        if intersect:
            inside = not inside
    return inside

def rectCorners(rect):
    """Lấy danh sách 4 đỉnh của hình chữ nhật (nếu có corners thì trả luôn)"""
    if "corners" in rect and rect["corners"]:
        return rect["corners"]
    return [
        {"x": rect["x1"], "y": rect["y1"]},
        {"x": rect["x2"], "y": rect["y1"]},
        {"x": rect["x2"], "y": rect["y2"]},
        {"x": rect["x1"], "y": rect["y2"]},
    ]

def isRectInRect(inner, outer):
    """Kiểm tra rect trong rect (có xét góc xoay)"""
    outerCorners = rectCorners(outer)
    innerCorners = rectCorners(inner)
    # chỉ cần tất cả đỉnh inner nằm trong outer
    return all(pointInPolygon(c, outerCorners) for c in innerCorners)

def isCircleInCircle(inner, outer):
    """Kiểm tra circle trong circle"""
    dx = inner["cx"] - outer["cx"]
    dy = inner["cy"] - outer["cy"]
    dist = math.hypot(dx, dy)
    return dist + inner["r"] <= outer["r"]

def isRectInCircle(rect, circle):
    """Kiểm tra rect trong circle"""
    corners = rectCorners(rect)
    return all(math.hypot(p["x"]-circle["cx"], p["y"]-circle["cy"]) <= circle["r"] for p in corners)

def isCircleInRect(circle, rect):
    """Kiểm tra circle trong rect (có xét góc xoay)"""
    rectPoly = rectCorners(rect)
    testPoints = [
        {"x": circle["cx"] - circle["r"], "y": circle["cy"]},
        {"x": circle["cx"] + circle["r"], "y": circle["cy"]},
        {"x": circle["cx"], "y": circle["cy"] - circle["r"]},
        {"x": circle["cx"], "y": circle["cy"] + circle["r"]}
    ]
    return all(pointInPolygon(p, rectPoly) for p in testPoints)

# --- Kiểm tra list_min vs list_max ---
def validate_shapes(list_min, list_max):
    all_ok = True
    for i, min_shape in enumerate(list_min):
        inside_some_max = False
        for j, max_shape in enumerate(list_max):
            contained = False
            if min_shape["type"] == "rect" and max_shape["type"] == "rect":
                contained = isRectInRect(min_shape, max_shape)
            elif min_shape["type"] == "circle" and max_shape["type"] == "circle":
                contained = isCircleInCircle(min_shape, max_shape)
            elif min_shape["type"] == "rect" and max_shape["type"] == "circle":
                contained = isRectInCircle(min_shape, max_shape)
            elif min_shape["type"] == "circle" and max_shape["type"] == "rect":
                contained = isCircleInRect(min_shape, max_shape)

            if contained:
                inside_some_max = True
                print(f"✅ Min {min_shape['type']} #{i+1} nằm trong Max {max_shape['type']} #{j+1}")
                break
        if not inside_some_max:
            print(f"❌ Min {min_shape['type']} #{i+1} KHÔNG nằm trọn trong bất kỳ Max nào!")
            all_ok = False

    if not list_max:
        print("✅ OK không tìm thấy hình Max (không cần kiểm tra).")
        return True
    else:
        if all_ok:
            print("✅ OK không tìm thấy lỗi.")
            return True
        else:
            print("❌ Điểm dấu không được nằm ngoài phạm vi hình khối.")
            return False
# --- Tách list_min / list_max từ JSON ---
def extract_min_max(data):
    result = {}
    for frame_id, frame_data in data.items():
        list_min, list_max = [], []
        for shape in frame_data["shapes"]:
            if "ten_hinh_min" in shape:
                list_min.append(shape)
            if "ten_khung_max" in shape:
                list_max.append(shape)
        result[frame_id] = (list_min, list_max)
    return result

def save_shapes_to_json(shapes, filename="shapes_data.json"):
    """Lưu dữ liệu shapes vào file JSON"""
    try:
        # Nếu file chưa tồn tại thì tạo file rỗng
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                json.dump([], f)

        # Đọc dữ liệu cũ
        with open(filename, "r", encoding="utf-8") as f:
            data_old = json.load(f)

        # Thêm dữ liệu mới
        data_old.append(shapes)

        # Ghi lại file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_old, f, ensure_ascii=False, indent=2)

        print(f"✅ Đã lưu dữ liệu vào {filename}")
    except Exception as e:
        print(f"❌ Lỗi khi lưu JSON: {e}")
def read_file_json(patd:str):
    try:
        with open(patd,"r",encoding="utf-8") as f:
            data = json.load(f)
            return data
    except UnicodeDecodeError:
        print("Loi UTF-8 khong doc dc")
    except FileNotFoundError:
        print("Khong tim thay file")
    finally:
        print("Ket thuc")
        
        
def check_quantity(request_quantity:int,data:list):
    """Hàm này kiểm tra số lượng shapes gửi về có bằng request quantity không"""
    if data :
        get_key = list(data[0].keys())
        return True if len(get_key) == request_quantity else False
    else:
        print("Dữ liệu rỗng")
        return False
def check_unique(arr):
    return len(arr) == len(set(arr))
def check_name_in_shape_empyty(data_dict:dict):
    """Hàm này kiểm tra có dữ liệu nào bị rỗng  và dữ liệu tên min có bị trùng không tên hay không"""
    try:
        if data_dict:
            arr_shape = data_dict.get("shapes",-1)
            if arr_shape != -1:
                arr_check_duplicate  = []
                for shape in arr_shape:
                    exist_name_min = shape.get("ten_hinh_min",-1) 
                    exist_name_max = shape.get("ten_khung_max",-1) 
                    if(exist_name_min == -1 and exist_name_max == -1):
                        print("Một hình không có tên trong shape")
                        return False   
                    if (exist_name_min == -1 and exist_name_max == ""):
                        print("Có hình tên Rỗng trong shape")
                        return False
                    if (exist_name_max == -1 and exist_name_min == ""):
                        print("Có hình tên Rỗng trong shape")
                        return False
                    #   print("\nexist_name_min",exist_name_min)
                    #   print("\nexist_name_max",exist_name_max)
                    if exist_name_min != "" and exist_name_max == -1:
                        arr_check_duplicate.append(exist_name_min)    
                print("---Có Tên----")
                status = check_unique(arr_check_duplicate)
                if status:
                    print("---Không trùng---")
                else:
                    print("---Bị Trùng---")
                return status
    
            else:
                print("Không có thuộc tính Shapes")
                return False
        else:
            print("Dũ liệu Shape không tồn tại")
            return False
    except:
        print("Có lỗi trong quá trình kiểm tra tên trùng")
        return False
        
def check_shape_data_config_master(length_shapes,data):
     """Hàm này để check xem dữ liệu có khung max nằm trong min không, giá trị tên có trống, giá trị tên min có trùng nhau không hợp lệ hay không nếu hợp về thì trả về giá trị Oke TRả về TRUE"""
     print("Kiểu dữ liệu :",type(data))
     length_oke = check_quantity(length_shapes,data)
     if not length_oke:
            print("Lỗi Chiều Dài Dữ liệu")
            return False
     value = list(data[0].values())
     for shape in value:
        status_oke = check_name_in_shape_empyty(shape) #kIEM TRA ten co rong va co trung lap nhau khong
        if not status_oke:
            return False
     frames = extract_min_max(data[0])
     for frame_id, (list_min, list_max) in frames.items():
        print(f"\n--- Frame {frame_id} ---")
        status_check = validate_shapes(list_min, list_max)
        if not status_check:
            print("Lỗi Chiều Logic dữ liệu")
            return False
     print("Dữ Liệu Hợp Lệ")
     return True

# if __name__ == "__main__":
#     data = read_file_json("shapes.json")
    # print("Dữ liệu JSON",data)
    # print("check du lieu co phai so nguyen k")
    # print("Kiểu dữ liệu :",type(data))
    # frames = extract_min_max(data[0])
    # for frame_id, (list_min, list_max) in frames.items():
    #     print(f"\n--- Frame {frame_id} ---")
    #     validate_shapes(list_min, list_max)
    # length_oke = check_quantity(21,data) # Kiem Tra do dai du lieu co du
    # check_shape_data_config_master(5,data)
   

        

    
    
    
    
