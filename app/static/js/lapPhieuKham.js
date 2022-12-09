
function hiddenText(){
    event.preventDefault()
    d = document.getElementsByClassName('txt-checked')[0]
    d.style.display =  'block'
}


//function autoCheckedMaBN(obj) {
//    fetch(`/api/autoCheckedMaBN/${obj.value}`).then(res => res.json()).then(data => {
//        method: 'put',
//        body: JSON.stringify({
//            "id": obj.value,
//        }),
//        headers: {
//            "Content-Type": "application/json"
//        }
//
//    })
//}