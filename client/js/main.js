const token = localStorage.getItem('token')
if (token == null){
    window.location.href = '../pages/login.html'
}

window.onload = function(){
let request = new XMLHttpRequest();
request.onload = function(){
    let my_obj = this.responseText;
    let response = JSON.parse(my_obj);
    console.log(response)
    loadResponse(response)

}
request.open("GET",`http://127.0.0.1:8000/client/singin/permission?token=${token}`);
request.send()
}
function loadResponse(response){
if (response.error == 'token_not_exist'){
window.location.href = '../pages/login.html'
} 
}

function sair(){
    localStorage.removeItem('token')
    window.location.href = '../pages/index.html' 
}