import {
    postData,headerMasterAdd,current_panner,setCurrentPanner,index_img_current,scroll_content
} from "./show_main_status.js";

const logSocket = io("/log");
const erase_master = document.getElementById("erase-master");
const btn_add_master = document.getElementById("btn-add-master");







// btn_add_master.addEventListener("click",function(){
//    console.log("Đã nhấn vào nút thêm master");
//     const div_create = document.createElement("div");
//     div_create.className = "div-index-img-mater";

//     const h_create = document.createElement("p");
//     h_create.innerText = `Ảnh master`;
//     h_create.className = "p-index-img-master";

//     const img = document.createElement("img");
//     img.src = "./static/img/plus (2).png";
//     img.alt = "Click vào đây để chụp ảnh";
//     img.style.padding = "35px";
//     img.style.width = "200px";
//     div_create.appendChild(img);
//     div_create.appendChild(h_create);
//     scroll_content.appendChild(div_create); 
//     div_create.addEventListener("click",function(){
//       console.log("Đã nhấn vào ảnh master mới để thêm master");
//       const index = Array.from(scroll_content.children).indexOf(this);
//       console.log("Ảnh master đang chỉ tới là",index);
//       //Tao ra cac nut nhan
//       let html = ""












//     });  
// });






//Xóa chưa Oke Cần Viết sau
erase_master.addEventListener("click",function(){
  console.log("Đã nhấn vào nút xóa master");
  console.log("Ảnh đang chỉ tới là",index_img_current);
  postData("api_add_master/erase_master", { "status": "200OK" }).then(data => {
  console.log("Server response: " + data);
  });
  
});


// sự kiện nhấn chuyển tab
headerMasterAdd.addEventListener("click",function(){
      console.log("current_panner",current_panner);
    console.log("Chuyển sang trang thêm mẫu");
    postData("api_add_master", { "status": "on" }).then(data => {
    console.log("Master Take :" + data);
  });
    const add_master = document.getElementById("panel-add-master");
    if (current_panner === add_master) return;
    current_panner.classList.remove("active");
    current_panner.style.zIndex = 1;
    add_master.classList.add("active");
    add_master.style.zIndex = 2;
    setCurrentPanner(add_master);
});




//Log sản phẩm
logSocket.on("log_message", function (data) {
       const tbody = document.querySelector(".product-table tbody");
       if (!tbody){
        console.log("Bảng không tồn tại");
        return;
       }
       tbody.innerHTML = "";
       let log = data.log_add_master;
          console.log("Dữ liệu nhận được là ",log);
       let id =  log?.list_id[0];
       let name   = log?.list_name[0];
       let x = log?.xyz[0][0];
       let y = log?.xyz[0][1];
       let z = log?.xyz[0][2];
       let k = 100;
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

});

// Log dữ liệu
logSocket.on("log_data", function (data) {
   console.log(data.log);
   const log_master =  document.getElementById("log_add_master");
   if (data.log){
        log_master.innerText += data.log;
   }
});
  
 

 

  