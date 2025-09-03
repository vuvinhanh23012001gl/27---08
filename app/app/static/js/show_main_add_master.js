import {
    postData,headerMasterAdd,current_panner,setCurrentPanner,
} from "./show_main_status.js";




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

  
 

  