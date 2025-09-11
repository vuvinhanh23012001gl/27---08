from typing import Dict,Any
import json
import os
import shutil
from pathlib import Path
class Create:
    def __init__(self,base_path: str = None):
        self.base_path = base_path
    def get_data_grandaugter(self,file_name:str,parent:str,grandparent:str)->Dict[str, Any]:
        """Trả về data sản phẩm hiện tại ở trong neu chua khoi tao thi se khoi tao duong dan
           Trả về rỗng nếu không có dữ liệu trong file
        """
        try: 
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dir_static = os.path.join(current_dir,grandparent)
            dir_static_name_product = os.path.join(dir_static,parent)
            os.makedirs(dir_static_name_product, exist_ok=True)
            file_json = os.path.join(dir_static_name_product, file_name)
            print(f"📂 Đường dẫn JSON đầy đủ: {file_json}")
            self.path_product_list = file_json   
            if not os.path.exists(file_json):
                with open(file_json, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                    print(f"📄 Tạo file JSON mới: {file_json}")
                    return None 
            with open(file_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.data = data
                print("✅ Đọc JSON thành công")
                return data
        except Exception as e:
            print("⚠️ File JSON rỗng hoặc sai định dạng → trả về dict rỗng")
            return {}
    def get_data_in_path(self,path:str):
         """đọc File json theo đường dẫn nếu không có trả về False nếu không có  file hoặc 
         có đường dẫn nhưng không phải file json . nếu thỏa mãn hết tất cả trả về data của đường dẫn
         """
         if path.lower().endswith(".json"):
            print("Là file Json")
         else:
             return False
         if not os.path.exists(path):
               print("Thư mục này không tồn tại")
               return False
         else :
            with open(path, 'r', encoding='utf-8') as f:
                print("Đọc File thành cônng")
                return json.load(f)

    def get_path_grandaugter(self,file_name:str,parent:str,grandparent:str)->Dict[str, Any]:
            """Giống với hàm trên nhưng trả về đường dẫn tới thu mục con
            """
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dir_static = os.path.join(current_dir,grandparent)
            dir_static_name_product = os.path.join(dir_static,parent)
            os.makedirs(dir_static_name_product, exist_ok=True)
            file_json = os.path.join(dir_static_name_product, file_name)
            print(f"📂 Đường dẫn JSON đầy đủ: {file_json}")
            self.path_product_list = file_json   
            if not os.path.exists(file_json):
                with open(file_json, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                    print(f"📄 Tạo file JSON mới: {file_json}")
            return file_json 
    def delete_folder(self,file_path):
        """
        Xóa file hoặc thư mục nếu tồn tại.
        Trả về True nếu xóa thành công, False nếu không xóa được.
        """
        if not os.path.exists(file_path):
            print(f"File/Thư mục không tồn tại: {file_path}")
            return False

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File đã xóa: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Thư mục đã xóa: {file_path}")
            else:
                print(f"Không phải file hay thư mục: {file_path}")
                return False
            return True
        except PermissionError:
            print(f"Lỗi quyền truy cập: Không thể xóa '{file_path}'")
            return False
        except Exception as e:
            print(f"Lỗi khi xóa '{file_path}': {e}")
            return False
    def delete_file(self,file_path):
        """
        Xóa file nếu tồn tại.
        Trả về True nếu xóa thành công, False nếu thất bại.
        """
        if not os.path.exists(file_path):
            print(f"File không tồn tại: {file_path}")
            return False

        if not os.path.isfile(file_path):
            print(f"'{file_path}' không phải là file")
            return False

        try:
            os.remove(file_path)
            print(f"Đã xóa file: {file_path}")
            return True
        except PermissionError:
            print(f"Lỗi quyền truy cập: Không thể xóa '{file_path}'")
            return False
        except Exception as e:
            print(f"Lỗi khi xóa file '{file_path}': {e}")
            return False
    def find_file_in_folder(self,folder_path, filename):
        """
        Tìm file trong thư mục.
        folder_path: đường dẫn thư mục
        filename: tên file muốn tìm (exact match)
        Trả về đường dẫn đầy đủ nếu tìm thấy, None nếu không tìm thấy
        """
        if not os.path.exists(folder_path):
            print(f"Thư mục không tồn tại: {folder_path}")
            return None

        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path) and f == filename:
                return full_path

        print(f"Không tìm thấy file '{filename}' trong '{folder_path}'")
        return None
    def create_file_in_folder(self, folder_path: str, file_name: str) -> Path | bool:
        """
        Tạo một file mới trong folder_path với tên file_name.
        - Nếu file chưa tồn tại: tạo file, trả về Path.
        - Nếu file đã tồn tại: trả về False.
        - Nếu không tạo được file: trả về false.
        """
        try:
            folder = Path(folder_path)
            folder.mkdir(parents=True, exist_ok=True)  # đảm bảo folder tồn tại

            file_path = folder / file_name
            if not file_path.exists():
                file_path.touch()  # tạo file rỗng
                print(f"Đã tạo file: {file_path}")     
                return {"return":True,"path":file_path}
            else:
                print(f"File đã tồn tại: {file_path}")
                return {"return":False,"path":file_path}
            
        except Exception as e:
            print(f"❌ Không thể tạo file: {e}")
            return False
    def create_file_in_folder_two(self,name_file: str, name_folder: str):
            """Tạo ra 1 foder nếu có rồi thì vào đó tạo ra 1 file
             trả về đường dẫn đến file nằm trong folder
            """
            current_dir = os.path.dirname(os.path.abspath(__file__))
            target_dir = os.path.join(current_dir, name_folder)
            os.makedirs(target_dir, exist_ok=True)

            file_path = os.path.join(target_dir, name_file)

            if not os.path.exists(file_path):
                print("📄 File không tồn tại, tạo mới.")
                with open(file_path, "wb") as f:   # tạo file nhị phân rỗng
                    print("File rỗng")
                    f.write(b"")                   # ghi 0 byte
            # else:
            #     print("📄 File đã tồn tại.")
            #     # Kiểm tra phần mở rộng
            #     ext = os.path.splitext(name_file)[1].lower()
            #     if ext in [".txt", ".json", ".md"]:   # file text
            #         with open(file_path, "r", encoding="utf-8") as f:
            #             print(f.read())
            #     else:  # file nhị phân (.pt, .png, .jpg, ...)
            #         with open(file_path, "rb") as f:
            #             data = f.read()
            #             print(data)
            #             print("📦 Đây là file nhị phân, kích thước:", len(data), "bytes")
            return file_path
    def create_folder(self,folder_path: str):
        """
        Tạo 1 folder theo đường dẫn.
        Nếu đã tồn tại thì không báo lỗi.
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"✅ Đã tạo (hoặc đã tồn tại): {folder_path}")
            return folder_path
        except Exception as e:
            print(f"❌ Lỗi khi tạo folder: {e}")
            return None
