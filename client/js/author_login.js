
window.onload = function(){
const token = localStorage.getItem('token')
let request = new XMLHttpRequest();
request.onload = function(){
    let my_obj = this.responseText;
    let response = JSON.parse(my_obj);
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