function addToListKham(id, hoTen, gioiTinh, namSinh, diaChi, sdt,ngayKham, avatar) {

    fetch('/api/listKham', {

        method: 'post',
        body: JSON.stringify({
            "id": id,
            "hoTen": hoTen,
            "gioiTinh": gioiTinh,
            "namSinh": namSinh,
            "diaChi": diaChi,
            "sdt": sdt,
            "ngayKham": ngayKham,
            "avatar": avatar
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then((data) => {

        console.log(data)
        let d = document.getElementsByClassName("totalBox")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_amount + "/40"
    }).catch(err => console.error())
 }