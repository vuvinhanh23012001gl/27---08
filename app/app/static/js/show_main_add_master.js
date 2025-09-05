import {
    postData,headerMasterAdd,current_panner,setCurrentPanner,
    index_img_current,scroll_content,set_Z_index_canvas_show,canvas_show,ctx_show,ctx
} from "./show_main_status.js";

const logSocket = io("/log");
const erase_master = document.getElementById("erase-master");
const btn_add_master = document.getElementById("btn-add-master");
const log_master =  document.getElementById("log_add_master");

let Max_X = 0;
let Max_Y = 0;
let Max_Z = 0;
let Max_K= 0;






btn_add_master.addEventListener("click",function(){
    console.log("Đã nhấn vào nút thêm master");
    const div_create = document.createElement("div");
    div_create.className = "div-index-img-mater";

    const h_create = document.createElement("p");
    h_create.innerText = `Ảnh master`;
    h_create.className = "p-index-img-master";

    const img = document.createElement("img");
    img.src = "./static/img/plus (2).png";
    img.alt = "Click vào đây để chụp ảnh";
    img.style.padding = "35px";
    img.style.width = "200px";
    div_create.appendChild(img);
    div_create.appendChild(h_create);
    scroll_content.appendChild(div_create); 
    div_create.addEventListener("click",function(){
      console.log("Đã nhấn vào ảnh master mới để thêm master");
      const index = Array.from(scroll_content.children).indexOf(this);
      console.log("Ảnh master đang chỉ tới là",index);
      //Tao ra cac nut nhan
      









    });  
});






//Xóa chưa Oke Cần Viết sau
erase_master.addEventListener("click",function(){
  console.log("Max_X",Max_X,Max_Y,Max_Z)
  console.log("Đã nhấn vào nút xóa master");
  console.log("Ảnh đang chỉ tới là",index_img_current);
  postData("api_add_master/erase_master", { "status": "200OK" }).then(data => {
  console.log("Server response: " + data);
  });
  
});

// sự kiện nhấn chuyển tab
headerMasterAdd.addEventListener("click",function(){
    set_Z_index_canvas_show(2);
    console.log("current_panner",current_panner);
    console.log("Chuyển sang trang thêm mẫu");
    scroll_content.innerHTML = ""; 
    postData("api_add_master", { "status": "on" }).then(data => {
            const imgList = data?.path_arr_img;
            const list_point  = data?.arr_point;
            create_table_product(data)
            // if (!imgList || imgList.length === 0) {log_master.innerHTML = "Hệ thống chưa có ảnh master nào";console.log("Hệ thống chưa có ảnh master nào");return}
            console.log("Danh sách điểm:", list_point);
            console.log("Danh sách ảnh:", imgList);
            imgList.forEach((imgPath, index) => {
                const div_create = document.createElement("div");
                div_create.className = "div-index-img-mater";
                const h_create = document.createElement("p");
                h_create.innerText = `Ảnh master ${index}`;
                h_create.className = "p-index-img-master";

                const img = document.createElement("img");
                img.src = imgPath;
                img.alt = "Ảnh sản phẩm";
                img.style.width = "200px";
                img.style.margin = "10px";

                div_create.appendChild(img);
                div_create.appendChild(h_create);
                scroll_content.appendChild(div_create);

                div_create.addEventListener("click", () => {
                    ctx.clearRect(0, 0, 1328, 830);
                              const show_img = new Image();
                              canvas_show.width = 1328;
                              canvas_show.height = 830;
                              show_img.src = imgPath;
                                        show_img.onload = () => {
                                          ctx_show.drawImage(show_img, 0, 0, 1328, 830);
                                        };
                });


          });
    });
    const add_master = document.getElementById("panel-add-master");
    if (current_panner === add_master) return;
    current_panner.classList.remove("active");
    current_panner.style.zIndex = 1;
    add_master.classList.add("active");
    add_master.style.zIndex = 2;
    setCurrentPanner(add_master);
});



function create_table_product(data) {
       const tbody = document.querySelector(".product-table tbody");
       if (!tbody){
        console.log("Bảng không tồn tại");
        return;
       }
       tbody.innerHTML = "";
       let log = data?.inf_product;
        console.log("Dữ liệu nhận được là ",log);
       let id =  log?.list_id[0];
       let name   = log?.list_name[0];
       let x = log?.xyz[0][0];
       Max_X = x;
       let y = log?.xyz[0][1];
       Max_Y = y;
       let z = log?.xyz[0][2];
       Max_Z = z;
       let k = 100;
       Max_K = k;

      //  console.log(name)
      //  console.log(id)
      //  console.log(x)
      //  console.log(y)
      //  console.log(z)
      const row = document.createElement("tr");
      row.innerHTML =  
      `<td>${name}</td>
       <td>${x}</td>
       <td>${y}</td>
       <td>${z}</td>
       <td>${k}</td>
      `;
      tbody.appendChild(row);
};



































//Log sản phẩm
// logSocket.on("log_message", function (data) {
//        const tbody = document.querySelector(".product-table tbody");
//        if (!tbody){
//         console.log("Bảng không tồn tại");
//         return;
//        }
//        tbody.innerHTML = "";
//        let log = data.log_add_master;
//           console.log("Dữ liệu nhận được là ",log);
//        let id =  log?.list_id[0];
//        let name   = log?.list_name[0];
//        let x = log?.xyz[0][0];
//        let y = log?.xyz[0][1];
//        let z = log?.xyz[0][2];
//        let k = 100;
//       //  console.log(name)
//       //  console.log(id)
//       //  console.log(x)
//       //  console.log(y)
//       //  console.log(z)
//       const row = document.createElement("tr");
//       row.innerHTML =  
//       `<td>${name}</td>
//        <td>${x}</td>
//        <td>${y}</td>
//        <td>${z}</td>
//        <td>${k}</td>
//       `;
//       tbody.appendChild(row);

// });

// Log dữ liệu
// logSocket.on("log_data", function (data) {
//    console.log(data.log);
   
//    if (data.log){
//         log_master.innerText += data.log;
//    }
// });
  
 

 

  



function validatePoint(x, y, z, brightness, Limit_x, Limit_y, Limit_z, Limit_k) {
  if (isNaN(x) || isNaN(y) || isNaN(z) || isNaN(brightness)) {
    return `❌ Các giá trị X, Y, Z, K phải là số hợp lệ và không được để trống`;
  }
  if (x < 0 || y < 0 || z < 0 || brightness < 0) {
    return `❌ Giá trị X, Y, Z, K phải lớn hơn hoặc bằng 0`;
  }
  if (x > Limit_x) {
    return `❌ Giá trị X phải nhỏ hơn hoặc bằng ${Limit_x}`;
  }
  if (y > Limit_y) {
    return `❌ Giá trị Y phải nhỏ hơn hoặc bằng ${Limit_y}`;
  }
  if (z > Limit_z) {
    return `❌Giá trị Z phải nhỏ hơn hoặc bằng ${Limit_z}`;
  }
  if (brightness > Limit_k) {
    return `❌Giá trị ánh sáng (K) phải nhỏ hơn hoặc bằng ${Limit_k}`;
  }
  return null; // không lỗi
}


function handleStart(index,inputs) {
  // Lấy giá trị từ các input
  const x = parseFloat(inputs.X.value);
  const y = parseFloat(inputs.Y.value);
  const z = parseFloat(inputs.Z.value);
  const brightness = parseFloat(inputs.K.value); // K là độ sáng

  // const errorMsg = validatePoint(index, x, y, z, brightness);  thay doi
  // if (errorMsg) {
  //   alert(errorMsg);
  //   return;
  // }

  // ✅ Gửi dữ liệu tới server
  fetch('/api_new_model/run_point', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      x: x,
      y: y,
      z: z,
      brightness: brightness
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Trạng thái:",data.message)
      console.log(`✅ Đã gửi điểm ${index} đến thiết bị. Phản hồi: ${data.message}`);
    })
    .catch(error => {
      console.error('Lỗi khi gửi điểm:', error);
      alert('❌ Gửi dữ liệu thất bại.');
    });
}
