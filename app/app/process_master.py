import json
from folder_create import Create
 
class Proces_Shape_Master():
    NAME_FOLDER_SAVE_DATA_MASTER = "Master_Regulations"
    NAME_FILE_SAVE_MASTER_REGULATIONS = "data_regulations.json"
    NAME_FOLDER_STATIC = "static"

    def __init__(self):
        self.object_folder = Create()
        self.path_save = self.init_file()
        self.list_regulations = self.get_file_data_json()    #Những cái nào thay đổi file trong data thì phải load lại dữ liệu cho   self.list_regulations 
    def init_file(self):
        return self.object_folder.get_path_grandaugter(
            Proces_Shape_Master.NAME_FILE_SAVE_MASTER_REGULATIONS,
            Proces_Shape_Master.NAME_FOLDER_SAVE_DATA_MASTER,
            Proces_Shape_Master.NAME_FOLDER_STATIC
        )

    def get_file_data_json(self):
        data = self.object_folder.get_data_in_path(self.path_save)
        return data if data else {}

    def save_shapes_to_json(self, type_id: str, data_master):
        if not self.path_save:
            print("Lưu thất bại: đường dẫn tới file không tồn tại")
            return False
        self.list_regulations = self.get_file_data_json() or {}
        self.list_regulations[type_id] = data_master
        with open(self.path_save, 'w', encoding='utf-8') as f:
            json.dump(self.list_regulations, f, ensure_ascii=False, indent=4)
        return True
    def update_data(self) -> bool:
        """
        Ghi lại toàn bộ dữ liệu self.list_regulations xuống file JSON.
        Trả về True nếu thành công, False nếu thất bại.
        """
        if not self.path_save:
            print("❌ Lưu thất bại: đường dẫn tới file không tồn tại")
            return False

        try:
            # Đảm bảo luôn cập nhật dữ liệu mới nhất trong RAM
            with open(self.path_save, "w", encoding="utf-8") as f:
                json.dump(self.list_regulations, f, ensure_ascii=False, indent=4)

            # Đọc lại file để đảm bảo dữ liệu đã lưu thành công
            self.list_regulations = self.get_file_data_json() or {}

            print("✅ Cập nhật dữ liệu thành công")
            return True

        except Exception as e:
            print(f"❌ Lỗi update_data: {e}")
            return False
    def load_file(self):
       self.list_regulations = self.get_file_data_json() 

    def check_all_rules(self, data_sp: dict) -> bool:
            """
            Kiểm tra toàn bộ dữ liệu của 1 sản phẩm (vd: data["SP01"]).
            Rule:
            1. Mỗi shape phải có tên (ten_hinh_min) và không rỗng.
            2. Trong 1 frame, các tên không được trùng nhau.
            """
            all_ok = True

            for frame_id, frame_data in data_sp.items():
                print(f"\n🔍 Kiểm tra Frame {frame_id}:")
                shapes = frame_data.get("shapes", [])

                # lấy tất cả tên min
                names = []
                for idx, shape in enumerate(shapes):
                    name = str(shape.get("ten_hinh_min", "")).strip()
                    if not name:
                        print(f"❌ Frame {frame_id}: Shape #{idx+1} thiếu hoặc rỗng 'ten_hinh_min'")
                        all_ok = False
                    names.append(name)

                # kiểm tra trùng lặp
                duplicates = [n for n in set(names) if names.count(n) > 1 and n]
                if duplicates:
                    print(f"❌ Frame {frame_id}: Tên Min bị trùng -> {duplicates}")
                    all_ok = False
                else:
                    print(f"✅ Frame {frame_id}: Không có tên Min trùng.")

            print("\n📌 Tổng kết:", "✅ Tất cả hợp lệ" if all_ok else "❌ Có lỗi trong dữ liệu")
            return all_ok
    def get_list_id_master(self):
        """Trả về None nếu trong file không có dữ liệu nào trả về danh sách dữ liệu có trong file"""
        if self.list_regulations:
            return [i for i in self.list_regulations]
    def get_data_is_id(self,ID:str):
        """Trả về data master regulation có ID là id trả về None nếu không tìm thấy ID """
        list_ID =  self.get_list_id_master()
        if not list_ID:
            print("Không có ID nào tồn tại có thể File rỗng") 
            return None
        if ID in list_ID :
            print(self.list_regulations[ID])
            return self.list_regulations[ID]  
        else:
            print("ID sản phẩm không tồn tại trong dữ liệu regulation")
            return None
    def erase_product_master(self,ID:str):
        """Hàm này thực hiện xóa master có ID là"""
        ID = ID.strip()
        if self.list_regulations:
            list_key = self.get_list_id_master()
            if ID in list_key:
                print("Tìm thấy ID thực hiện xóa")
                status_erase = self.list_regulations.pop(ID,None)
                status_save  = self.update_data()
                if status_erase is not None  and status_save != False:
                    print("Xóa thành công sản phẩm có ID:",status_erase)
                    return True
                else:
                    print("Xóa không thành công sản phẩm có ID=",ID)
                    return False
            else:
                print("Không tìm thấy ID đó trong sản phẩm")
                return False
    def erase_master_index(self, ID: str, index:int):
        """Hàm này thực hiện xóa index thứ bao nhiêu trong 1 ID"""
        print("Xóa master thứ index:", index)
        self.list_regulations = self.get_file_data_json() or {}
        print("self.list_regulations",self.list_regulations)
        if self.list_regulations:
            list_key = self.get_list_id_master()
            print("Danh sách ID Master hiện có :",list_key)
            if  ID in list_key:
                print("Tìm thấy master quy định có ID",ID)
                arr_key = [i for i in self.list_regulations[ID]]
                print("Index ảnh đã có:", arr_key)
                if arr_key:
                    if str(index) in arr_key:
                        self.list_regulations[ID].pop(str(index), None)
                        arr_key_new = list(self.list_regulations[ID].keys())
                        print("Sau khi xóa danh sách ảnh là:",arr_key_new)
                        if arr_key_new:
                            name_key_arr_new = [str(i) for i in range(len(arr_key)-1)]
                            print("Danh sách ảnh sau khi cần đổi tên",name_key_arr_new)
                            for value1, value2 in zip(arr_key_new, name_key_arr_new):
                                self.list_regulations[ID][value2] = self.list_regulations[ID].pop(value1)
                            print("Update sau khi xoa")
                            self.update_data()
                            print("Danh sách index còn lại sau khi xóa", list(self.list_regulations[ID].keys()))
                            print("Xóa thành công")
                            return True
                        else:
                          self.update_data()
                          print("Danh sách đã rỗng")
                          return False
                    else:
                       print("Index không nằm trong data đang có")
                       return False
                else:
                    print("Loại sản phẩm này chưa có dữ liệu Master regulation")
                    return False
            else:
                print("ID này chưa tạo master regulation")
                return False
          

# shape = Proces_Shape_Master()
# shape.erase_master_index("SP01",0)


# shape = Proces_Shape_Master()
# print(shape.get_list_id_master())

# shape = Proces_Shape_Master()
# shape.get_data_is_id("SP01")

# shape = Proces_Shape_Master()
# shape.erase_product_master("SP02")

# data =shape.get_file_data_json()
# ok = shape.check_all_rules(data["SP01"])
# print("KẾT LUẬN CHUNG:", ok)