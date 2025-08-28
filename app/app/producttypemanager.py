from producttype import ProductType
from typing import Dict,Any,List
from folder_create import Create
import json
import os
import func
class ProductTypeManager:

    NAME_FILE_STATIC  = "static"
    NAME_FOLDER_PRODUCT_LIST = "Product_list"
    NAME_DATA_PRODUCT_LIST = "data.json"

    def __init__(self):
        self.product_types = {}
        self.path_product_list = self.get_patd_datajson()    # Trả về đường dẫn của dẫn tới nơi lưu dữ liệu data.json
        self.data = self.get_file_data()                     # Lấy dữ liệu từ File đấy ra
        self.load_from_file()                                # Load File đấy ra 


    def get_patd_datajson(self):
        """"Hàm này trả về đường dẫn,dẫn tới data.json"""
        object_folder = Create()
        return object_folder.get_path_grandaugter(ProductTypeManager.NAME_DATA_PRODUCT_LIST,ProductTypeManager.NAME_FOLDER_PRODUCT_LIST,ProductTypeManager.NAME_FILE_STATIC)
    
    def load_from_file(self):
        """Load File vào trong đối tượng Point dầu"""
        print("📥 Đang tải dữ liệu từ file JSON...")
        if self.data:
            for key in self.data.keys():
                type_id = self.data[key].get("type_id",-1)
                type_name = self.data[key].get("type_name",-1)    
                xyz  = self.data[key].get("xyz",-1) 
                if type_id == -1 or type_name == -1 or xyz == -1:
                    print("❌Không Tìm Thấy 1 Số Dữ liệu Khi Load Trả về False")
                    return
                product = ProductType(type_id,type_name,xyz)
                product.Init_path() #Tao File luon cho no 
                for point in self.data[key]["point_check"]:
                    product.add_list_point(point["x"], point["y"], point["z"], point["brightness"])
                self.product_types[key] = product   #Thêm vào Sản phẩm
                # self.show_all()
        else:
            print("❌Data rỗng chưa có dữ liệu")
    def save_json_data(self, data_file_path:str):
        "Luu dữ liệu điểm vào đường link data data.json"
        try:
            dir_name = os.path.dirname(data_file_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(data_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.return_data_dict_all(), f, ensure_ascii=False, indent=4)
            print(f"✅ Đã lưu dữ liệu JSON vào: {data_file_path}")
        except Exception as e:
            print(f"❌ Lỗi khi lưu dữ liệu JSON: {e}")
    def add_product_type(self,id,name:str,xyz:list,description:str="")->bool:
        """Thêm đối tượng ProductType vào danh 1 loại sản phẩm mới vào danh sách các ProductType để quản lý
        Kiểm tra type nếu trùng rồi thì trả về  False
        Trả về True nếu thêm thành công và print lỗi
        Trả về False nếu thêm không thành công và print lỗi
        """
        product = ProductType(id,name,xyz)
        if description:
            product.description_product(description)
        status  = self.check_id_in_data(id)
        if status == 1: # Du lieu da co
            print("Dữ liệu đã có bị trùng ID Không lưu")
            return False
        elif status == 0:
            if(product.check_xyz()):
                print("🔔Kiểm tra trước khi thêm OKE")
                product.Init_path()
                self.product_types[product.type_id] = product
                try:
                 
                    self.save_json_data(self.path_product_list)
                    self.data = self.get_file_data()
                    self.load_from_file()
                    return True  
                except Exception as e:
                    print(f"❌ Lỗi khi lưu JSON sau khi thêm: {e}")
                    return False   
            else:
                print("❌Lỗi Data Không Hợp Lệ")
                False
        else:
            print("File Trống Cứ Thế Lưu")
            product.Init_path()
            self.product_types[product.type_id] = product
            self.save_json_data(self.path_product_list)
            self.data = self.get_file_data()
            self.load_from_file()
            return True

    def get_file_data(self)->Dict[str, Any]:
        """Trả về data sản phẩm hiện tại ở trong tao File co ten neu khong co file do
           Trả về rỗng nếu không có dữ liệu trong file
        """
        object_folder = Create()
        return object_folder.get_data_grandaugter(ProductTypeManager.NAME_DATA_PRODUCT_LIST,ProductTypeManager.NAME_FOLDER_PRODUCT_LIST,ProductTypeManager.NAME_FILE_STATIC)

    def check_id_in_data(self, id: str) -> bool:
            """Trả về -1 nếu File trắng trả về 1 nếu có , trả về 0 nếu k có"""
            list_id = self.get_list_id_product()
            if list_id:
                if id in list_id:
                    return 1
                else:
                    return 0
            return -1
        
    def get_list_id_product(self)->List[any]:
        """Trả về list danh sách các ID,Nếu không có trả về mảng rỗng"""
        return [pt.type_id for pt in self.product_types.values()]
    
    def get_list_path_master(self)->List[any]:
        "Trả về danh sách đường dẫn đầy đủ của các lis path master c:\\Users\\anhuv\\Desktop\\26_08\\25-08\\app\\app\\static\\Master_Photo\\Master_Vinhanh', 'c:\\Users\\anhuv\\Desktop\\26_08\\25-08\\app\\app\\static\\Master_Photo\\Master_Vinhan132' "
        return [pt.path_img_master for pt in self.product_types.values()]
    
    def get_list_path_master_product_img_name(self,idtype:str)->List[Any]:
        """Trả về danh sách các path ảnh Master của loại ID đó"""
        if idtype is not None and  self.product_types is not None:
            for pt in self.product_types.values():
                if pt.type_id == idtype.strip():
                    return func.get_image_paths_from_folder(pt.get_path_name_folder_master_img())
        else:
            print("Tên ID hoặc dữ liệu chưa có")

    def find_by_id(self, type_id:str)->object:
        """Trả về đối tượng có id trùng với id nhập  nếu không có trả về -1"""
        return self.product_types.get(type_id,-1 )
    
    def get_list_point_find_id(self,type_id_product:str)->dict:
        """Trả về None nếu không tìm thấy, Trả về mảng danh sách điểm có ID trùng"""
        result =  self.find_by_id(type_id_product)
        if result == -1:
            return  None
        else :
            return result.get_list_point()
        
    def get_product_name_find_id(self,type_id_product:str)->dict:
        """Trả về tên sản phẩm nếu trùng ID nếu không trả về None"""
        result =  self.find_by_id(type_id_product)
        if result == -1:
            return None
        else :
            return result.get_type_name()
        
    def get_path_product_img_name(self,idtype:str):
        """Trả về None nêu không tìm thấy sp có typeid còn không trả về link ảnh của sản phẩm"""
        if idtype is not None and  self.product_types is not None:
            for pt in self.product_types.values():
                if pt.type_id == idtype.strip():
                     return pt.get_path_name_folder_product_img()
        else:
            print("Tên ID hoặc dữ liệu chưa có")

    def absolute_path(self,idtype:str):
        """object :Trả về None nêu không tìm thấy sp có typeid còn không trả về link đường dẫn tuyệt đối của sản phẩm"""
        if idtype is not None and  self.product_types is not None:
            for pt in self.product_types.values():
                if pt.type_id == idtype.strip():
                    return pt.Path_Product
        else:
            print("Tên ID hoặc dữ liệu chưa có")

    def show_all(self):
        """object : show toàn bộ thông tin có trong đối tượng"""
        if not self.product_types:
            print("❌ Chưa có loại sản phẩm nào.")
            return
        print("📦 Danh sách loại sản phẩm:")
        for pt in self.product_types.values():
            pt.show_product_type()
            print("-" * 40)

    def get_all_ids_and_names(self):
        """Trả về dict ID và Name của các sản phẩm hiện có"""
        self.load_from_file()
        return {
            "list_id": [pt.type_id for pt in self.product_types.values()],
            "list_name": [pt.type_name for pt in self.product_types.values()],
            "xyz":    [pt.xyz for pt in self.product_types.values()]
        }
    
    def return_data_dict_all(self):
        """object: Trả về danh sách dữ data dict có trong đối tượng"""
        result = {}
        for i in self.product_types.values():
            result[i.type_id] = i.protype_to_dict()
        # print(result)
        return result
    
    def get_all_id(self):
        """Trả về danh sách các ID"""
        return list(self.product_types.keys())
    
    def count(self):
        """Đếm số lượng sản phảm hiện có"""
        return len(self.product_types)
    
    def return_data_dict(self,type_id):
        """Trả về dict của ID nhập"""
        if(self.find_by_id(type_id)  is not None):
             return self.find_by_id(type_id).protype_to_dict()

    def remove_product_in_file_data(self,id:str):
        if id in self.get_all_id():
            status_pop = self.product_types.pop(id,None)
            if status_pop is None:
                print(f"Xóa File có ID:{id} không thành công")
                return False
            else:
                print(self.return_data_dict_all())
                self.save_json_data(self.path_product_list)
                self.data = self.get_file_data()
                self.load_from_file()
                print(f"Xóa ID:{id} thành công trong file data.json")
                return True
        else:
            print("Không tìm thấy ID trong danh sách")

        
        
#-------------------------------------------------------------------------
    def remove_product_type(self, type_id:str)->bool:
        print("Tiến Hành Xóa ID")
        isObject = self.find_by_id(type_id)
        if isObject!= -1:
            path_master = isObject.get_path_img_master()
            path_retraining = isObject.get_path_img_retraning()
            if path_master is not None and path_retraining is not None:
                print("File Tồn tại")
                object_folder = Create()
                print(path_master,"\n",path_retraining)
                status_img_master = object_folder.delete_folder(path_master)
                status_img_retraining = object_folder.delete_folder(path_retraining)
                if not status_img_master:
                    print("Xóa Path Img master Không Thành công")
                    return False
                if not status_img_retraining:
                    print("Xóa Path IMG retraining không thành công")
                    return False
                if status_img_master:
                    print("Xóa Folder matster thành công")
                if status_img_retraining:
                    print("Xóa Folder retraining thành công")
                path_product = isObject.get_Path_Product()
                if path_product:
                     path_img = object_folder.find_file_in_folder(path_product,f"Img_{isObject.type_id.strip()}.png")
                     if(path_img):
                        print("Xóa File ảnh thành công",path_img)  
                        status_img_product = object_folder.delete_file(path_img)
                        if not status_img_product:
                            print("Xóa File ảnh sản phẩm không thành công")
                        else:
                            print("Xóa File ảnh sản phẩm thành công")
                     else :
                        print("Không tìm thấy File ảnh lưu sản phẩm xóa ảnh chưa đc")
                else:
                    print("Đường dẫn tới Product_Photo không tồn tại")
                status = self.remove_product_in_file_data(type_id)
                if status:
                    print("Xóa thành công 3 File")
                    return True
                else:
                    print("Xóa bị False")
                    return False
            else:
                print("File không tồn tại")
                return False
        else:
            print("Không tìm thấy ID")
            return False
    


            
# #----------------------------------------------------------------------------------------------------------------------------
# quanly = ProductTypeManager()
# print(quanly.get_list_path_master())

# quanly = ProductTypeManager()
# quanly.remove_product_in_file_data('SP1')

# quanly = ProductTypeManager()
# print(quanly.get_list_path_master_product_img_name("SP001"))

# quanly = ProductTypeManager()
# quanly.remove_product_type("0")

# quanly = ProductTypeManager()
# print(quanly.return_data_dict("SP1"))

# quanly = ProductTypeManager()
# print(quanly.get_all_ids())

# quanly = ProductTypeManager()
# print(quanly.count())

# quanly = ProductTypeManager()
# print(quanly.find_by_id("SP1"))


# quanly = ProductTypeManager()
# print(quanly.get_list_point_find_id("SP1"))

# quanly = ProductTypeManager()
# print(quanly.get_product_name_find_id("SP12"))

# quanly = ProductTypeManager()
# quanly.show_all()

# quanly = ProductTypeManager()
# print(quanly.get_all_ids_and_names())

# quanly = ProductTypeManager()
# print(quanly.get_file_data())

# # # # # quanly.load_from_file()

# # # # # quanly = ProductTypeManager()
# # # # # print(quanly.get_list_id_product())

# # # # # quanly = ProductTypeManager()
# # # # # print(quanly.get_list_path_master())
# # print(quanly.get_list_path_master_product_img_name("typeid1"))

# quanly.add_product_type("typeid1","xinchoa",[1,2,3])
# quanly.add_product_type("typeid2","xinchoa2",[1,2,3])

# quanly = ProductTypeManager()
# print(quanly.return_data_dict_all())


# print(quanly.find_by_id("idtype1"))
# print(quanly.get_list_point_find_id("idtype1"))
# # path = quanly.get_list_path_master()

# # # print(path)
# # path  = quanly.get_list_path_master_product_img_name("idtype1")
# # print(path)

# # # # # print(quanly.find_by_id("typeid2"))
# # # quanly.get_path_product_img_name(232)
# # print(quanly.absolute_path("1"))

# # print(quanly.get_file_data())
# # # # # # Tạo các loại sản phẩm
# pt1 = ProductType("idtype4", "Loại A")
# pt2 = ProductType("idtype5", "Loại B")

# # # # # # # # # Thêm các điểm
# pt1.add_list_point(1, 2, 3, 10)
# pt1.add_list_point(4, 5, 6, 20)

# pt2.add_list_point(7, 8, 9, 30)
# pt2.add_list_point(10, 11, 12, 40)
# # # # # # # # # Thêm vào danh sách quản lý


# quanly.return_data_dict_all()
# pt3 = ProductType("idtype3", "Loại C")
# pt3.add_list_point(7, 8, 9, 30)
# pt3.add_list_point(10, 11, 12, 40)





# quanly.return_data_dict_all()
# # # # Hiển thị toàn bộ

# # quanly.show_all()
# quanly.load_from_file()
# quanly.remove_product_type("idtype1")
# print(quanly.return_data_dict("idtype2"))
# print(quanly.return_data_dict_all())
# print(quanly.get_file_data())
# print(quanly.return_data_dict_all())
# Hiển thị sau khi xóa



