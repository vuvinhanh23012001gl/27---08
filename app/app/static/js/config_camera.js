console.log("Đã vào camera config");
const close_config_camera = document.getElementById("close-config-camera");
const btn_open_camera_config = document.getElementById("btn-open-camera-config");    
const overlay_config_camera = document.querySelector(".overlay_config_camera");


btn_open_camera_config.addEventListener('click',()=>{
    console.log("Xuất hiện khung hình config camera");
    overlay_config_camera.style.display = "flex";
});

close_config_camera.addEventListener("click",()=>{
     fetch('/api_config_camera/exit')
      .then(response => {
          if (response.redirected) {
              window.location.href = response.url;
          } else {
              response.json().then(data => {
                  window.location.href = data.redirect_url;
              });
          }
      });
});

