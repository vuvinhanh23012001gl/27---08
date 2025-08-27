from typing import Dict,Any
import json
import os
class Create:
    def __init__(self):
        pass
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