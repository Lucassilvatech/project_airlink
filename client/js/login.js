let buttonConf = document.querySelector('.confLogin')
let inputEmail = document.querySelector('.emailUser')
let inputPassword = document.querySelector('.passwordUser')

let forgotPw = document.querySelector('.forgotPw')
let conteiner = document.querySelector('.boxRecuperacaoPw')
let mainLogin = document.querySelector('.main_login')

buttonConf.addEventListener('click', requestAPI)


// Faz uma solicitação de GET na api
function requestAPI(){

  if (inputEmail.value == '' || inputPassword.value == ''){
      alert('O campo email e senha são obrigatorios')
      return
    }
    
    fetch('http://127.0.0.1:8000/client/singin', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          'email':inputEmail.value,
          'key_pw':inputPassword.value
      })
      })
      .then(response => response.json())
      .then(data => loadResponse(data))
      .catch(error => {
        window.alert("algo deu errado /:")
        console.log(error)
    })
  }


// Faz uma validação na resposta da api
function loadResponse(response){
  if (response.detail == 'email_not_exist'){
    window.alert('O usuario não existe!')

  }else if (response.detail == 'password_error'){
    window.alert('Senha inválida!') 

  }else{
    let token = response.key_login
    localStorage.setItem('token', token)
    localStorage.setItem('user_id', response.id_user)
    localStorage.setItem('nome', response.nome)
    window.location.href = '../pages/main.html'
  }
}


forgotPw.addEventListener('click', function(){
  mainLogin.classList.add('noneDisplay')
  conteiner.classList.remove('noneDisplay')
})

