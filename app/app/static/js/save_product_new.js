  const fileInput = document.getElementById("file_upload");
  const fileInfo = document.getElementById("fileInfo");
  const previewImg = document.getElementById("previewImg");
  const form = document.getElementById("productForm");

  let selectedFile = null;

  // --- Khi chọn ảnh thì preview offline trước ---
  fileInput.addEventListener("change", function() {
    let file = this.files[0];
    if (file) {
      selectedFile = file;
      fileInfo.textContent = "Đã chọn: " + file.name;

      if (file.type.startsWith("image/")) {
        let reader = new FileReader();
        reader.onload = function(e) {
          previewImg.src = e.target.result;
          previewImg.style.display = "block";
        }
        reader.readAsDataURL(file);
      } else {
        previewImg.style.display = "none";
      }
    } else {
      fileInfo.textContent = "Chưa chọn file nào";
      previewImg.style.display = "none";
      selectedFile = null;
    }
  });

  // --- Xử lý submit form ---
  form.addEventListener("submit", function(e) {
    
    e.preventDefault(); // chặn submit mặc định (reload trang)
    let formData = new FormData(form); // lấy toàn bộ dữ liệu form
    let product_id = formData.get("product_id");
    let product_name = formData.get("product_name");
    let limit_x = formData.get("limit_x");
    let limit_y = formData.get("limit_y");
    let limit_z = formData.get("limit_z");

    // Kiểm tra rỗng
    if (!product_id || !product_name || !limit_x || !limit_y || !limit_z ) {
        alert("Vui lòng nhập đầy đủ thông tin và chọn file!");
        return; // dừng lại, không gửi fetch
    }
    if (product_id < 0 || product_name < 0|| limit_x < 0 || limit_y < 0 || limit_z < 0 ) {
        alert("Vui lòng nhập giá trị lớn hơn 0");
        return; // dừng lại, không gửi fetch
    }

    console.log(formData);
    fetch(form.action, {
      method: "POST",
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success == true) {
        alert("Lưu thành công!");
      } else {
        alert("Lưu thất bại!");
      }
    })
    .catch(err => {
      console.error(err);
      alert("Lỗi kết nối server!");
    });
  });