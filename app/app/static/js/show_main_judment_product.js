import {logSocket,canvas_img_show_oke,ctx_oke} from "./show_main_status.js";
console.log("đã vào Hàm phán định")


const io_img_and_data = io("/img_and_data");
io_img_and_data.on("connect", () => {
            console.log("Đã kết nối server namespace /video");
});
io_img_and_data.on("photo_taken", (data) => {
    // Lấy chỉ số điểm và tổng số điểm
    console.log("Index:", data.index);
    console.log("Total length:", data.length);

    // Nếu muốn hiện lên giao diện
    // document.getElementById("index_label").innerText = `Điểm: ${data.index}/${data.length}`;  //thay label

    // Phần xử lý ảnh giữ nguyên như trước
    let arrayBuffer;
    if (data.img instanceof ArrayBuffer) {
        arrayBuffer = data.img;
    } else if (data.img && data.img.data) {
        arrayBuffer = new Uint8Array(data.img.data).buffer;
    } else {
        console.error("Không nhận được dữ liệu ảnh hợp lệ:", data);
        return;
    }

    const blob = new Blob([arrayBuffer], { type: 'image/jpeg' });
    const imgUrl = URL.createObjectURL(blob);


      const img = new Image();
    img.onload = () => {
    canvas_img_show_oke.width = 1328;
    canvas_img_show_oke.height = 830;
    ctx_oke.drawImage(img, 0, 0, 1328, 830);
    if (prevUrl) URL.revokeObjectURL(prevUrl);
    prevUrl = imgUrl;
  };
  img.src = imgUrl;
});
