
from pathlib import Path
class FolderCreator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)  # chỉ lưu lại đường dẫn, KHÔNG tạo ngay
        # print(f"📂 Base path set: {self.base_path}")

    def ensure_base(self):
        """Chỉ tạo thư mục gốc khi cần"""
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True, exist_ok=True)
            # print(f"📁 Đã tạo thư mục gốc: {self.base_path}")
        else:
            pass
            # print(f"📁 Thư mục gốc đã tồn tại: {self.base_path}")

    def create_subfolder(self, subfolder_name):
        self.ensure_base()
        subfolder_path = self.base_path / subfolder_name
        subfolder_path.mkdir(parents=True, exist_ok=True)
        # print(f"📂 Thư mục con: {subfolder_path}")
        return subfolder_path

    def create_nested_subfolder(self, parent_name, child_name):
        self.ensure_base()
        nested_path = self.base_path / parent_name / child_name
        nested_path.mkdir(parents=True, exist_ok=True)
        # print(f"📂 Thư mục cháu: {nested_path}")
        return nested_path

    def create_subfolder_support(self, subfolder_name: str):
        current_dir = Path(__file__).parent.resolve()
        static_dir = current_dir / "static"
        subfolder_path = static_dir / subfolder_name
        subfolder_path.mkdir(parents=True, exist_ok=True)
        # print(f"📁 Đã tạo thư mục: {subfolder_path}")
        return subfolder_path

 