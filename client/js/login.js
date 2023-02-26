
let buttonConf = document.querySelector('.confLogin')
let inputEmail = document.querySelector('.emailUser')
let inputPassword = document.querySelector('.passwordUser')

let forgotPw = document.querySelector('.forgotPw')
let conteiner = document.querySelector('.boxRecuperacaoPw')
let mainLogin = document.querySelector('.main_login')

// Faz uma solicitação de GET na api
buttonConf.addEventListener('click', () =>{
  let request = new XMLHttpRequest();
  request.onload = function(){
    let my_obj = this.responseText;
    let response = JSON.parse(my_obj);
      loadResponse(response)
        
  }
request.open("GET",`http://127.0.0.1:8000/client/singin?email=${inputEmail.value}&password=${inputPassword.value}`);
request.send()

})

// Faz uma validação na resposta da api
export function loadResponse(response){
  if (response.error == 'email_not_exist'){
    window.alert('O usuario não existe!')

  }else if (response.error == 'password_error'){
    window.alert('Senha inválida!') 

  }else{
    let token = Math.random().toString(16).slice(-13) + Math.random().toString(16).slice(-13)
    localStorage.setItem('token', token)
    window.location.href = '../pages/main.html'
    
  }
}

forgotPw.addEventListener('click', function(){
  mainLogin.classList.add('noneDisplay')
  conteiner.classList.remove('noneDisplay')
})