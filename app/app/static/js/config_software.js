const btn_open_software_config = document.getElementById("btn-open-software-config");
const overlay_config_software  = document.getElementById("overlay_config_software");
const close_settings_software  = document.getElementById("close-settings");
btn_open_software_config.addEventListener("click",()=>{
      overlay_config_software.style.display = "flex";
});

close_settings_software.addEventListener("click",()=>{
     fetch('/api_config_software/exit')
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
