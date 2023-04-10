const inputUser = document.querySelector('.nameUser')
const buttonConf = document.querySelector('.confLogin')
const inputEmail = document.querySelector('.emailUser')
const inputPassword = document.querySelector('.passwordUser')
const inputPassword_2 = document.querySelector('.passwordUser_2')


// Faz uma solicitação de POST na api
buttonConf.addEventListener('click', () =>{
    if (validaDados()){

    if (inputPassword_2.value === inputPassword.value){
        fetch('http://127.0.0.1:8000/client/singup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'nome':inputUser.value,
            'email':inputEmail.value,
            'key_pw':inputPassword.value
        })
        })
        .then(response => response.json())
        .then(data => loadData(data))
        .catch(error => console.log(error))
    }else{
        alert('Senhas não confere')
    }
}
})

function loadData(data){
    console.log('foi')
    if (data.detail == 'DuplicateError') {
        window.alert('Usuario já existe!')
    }else {
        
        window.location.href = '../pages/login.html'
    }  

}
function validaDados(){
    if ((inputUser.value == '') || (inputEmail.value == '') ||
    (inputPassword.value == '') || (inputPassword_2.value == '')) {
        window.alert('Todos os valores são obrigatorios!')
        return false
    }else{
        return true
    }
}