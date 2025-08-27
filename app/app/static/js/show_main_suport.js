const run_btn = document.getElementById("api-run");
const add_product = document.getElementById("add-product");

run_btn.addEventListener('click',()=>{
      fetch('/api_run_application/run_application')
      .then(response => response.json())
      .then(data => {
        console.log("Dữ liệu nhận sau click Run"+ data);
        if(data.status  == "OK"){
          console.log("Gửi dữ liệu Run Thành công đến Server"+ data);
        }
      })
      .catch(err => {
        console.error('❌ Lỗi khi gửi Run GET:', err);
      });
});
const out_app =  document.getElementById("out-app");
out_app.addEventListener('click',()=>{
    
    window.close();

});
add_product.addEventListener("click",function(){
    window.location.href = "/api_new_product/add";
})

