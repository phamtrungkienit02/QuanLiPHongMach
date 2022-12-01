function addToListKham(hoTen,namSinh ,diaChi, gioiTinh, ngayKham,  avatar, sdt) {
    event.preventDefault()

    fetch('/api/listKham', {
        method: "post",
        body: JSON.stringify({
           "hoTen": hoTen,
            "diaChi": diaChi,
            "gioiTinh": gioiTinh,
            "namSinh": namSinh,
            "sdt": sdt,
            "ngayKham": ngayKham,
            "avatar": avatar,
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementsByClassName("totalBox")
        d.innerText = data.total_amount
    }) // promise
    .catch((err) => {
        console.error(err)
    })
}