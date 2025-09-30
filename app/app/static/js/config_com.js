
const btn_open_com_config = document.getElementById("btn-open-com-config");
const overlay_config_com = document.getElementById("overlay_config_com");
const com_close = document.getElementById("com-close");



btn_open_com_config.addEventListener('click',()=>{
    console.log("Xuất hiện khung hình config camera");
    overlay_config_com.style.display = "flex";
    let data_return = fetch_get("/api_config_com/get_list_com");
    console.log(data_return);

});


com_close.addEventListener("click",()=>{
     fetch('/api_config_com/exit')
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


async function fetch_get(domanin_str) {
  // domanin_str = "/hello"
  try {
    const response = await fetch(domanin_str, {
      method: "GET",
      headers: { "Accept": "application/json" }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return data;                          // Trả về dữ liệu cho nơi gọi
  } catch (err) {
    console.error("Fetch thất bại:", err);
    return { error: err.message };         // Trả về thông báo lỗi
  }
}