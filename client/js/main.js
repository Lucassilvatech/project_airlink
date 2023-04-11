let passagens = document.querySelector('.passagens')
let origem = document.querySelector('.origem')
let destino = document.querySelector('.destino')
let carrinho = document.querySelector('span')
let viewCarrinho = document.querySelector('.carrinho')


function sair() {
    localStorage.removeItem('token')
    window.location.href = '../pages/index.html'
}


fetch('http://127.0.0.1:8000/voos', {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json'
    },
    })
    .then(response => response.json())
    .then(data => loadPassagensAuto(data))
    .catch(error => console.log(error))


function loadPassagensAuto(data) {
    let client = localStorage.getItem('nome')
    document.querySelector('header').innerHTML = 'Olá, '+ client  
    for (valor of data) {
        passagens.innerHTML +=
    `<div id="sub_box">
        <h3> viage de ${valor.origem} para ${valor.destino}</h3>
        <span><p></p></span>
        <p>preço ${valor.preco}</p>
        <p>Numero do voo:${valor.numero_voo}</p>
        <div class="product" id="${valor.numero_voo}">Add Carrinho</div>
    </div>`
    }
}


function passagensSearch() {
    let data = JSON.stringify({
        'origem': origem.value,
        'destino': destino.value,
    })
    
    localStorage.setItem('data', data)
    window.location.href = '../pages/view_passagens.html'
}


passagens.addEventListener('click', function(evt){
    try{
        let origin_value = evt.target.closest('.product').id
        if (evt.target.id == 'sub_box'){
            return;
        }
    let user = localStorage.getItem('user_id')
    console.log(user)
    fetch(`http://127.0.0.1:8000/client/carrinho/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'numero_voo': origin_value,
            'user': user
        })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error))
    }catch (error){
        return
    }
})


let cont = 1

carrinho.addEventListener('click', () =>{

    let user = localStorage.getItem('user_id')
    fetch(`http://127.0.0.1:8000/search/carrinho/${user}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        })
        .then(response => response.json())
        .then(data => addCarrinho(data))
        .catch(error => console.log(error))

    viewCarrinho.classList.remove('noneDisplay')
})


viewCarrinho.addEventListener('click', (evt) =>{
    if (evt.target.id == 'i'){
        viewCarrinho.classList.add('noneDisplay')
        viewCarrinho.innerHTML = '<i id="i">x</i>'
    } 
})


function addCarrinho(data){
    // carrinho.innerHTML = `Carrinho ${cont++}`
    let cont = 0
    for (valor of data) {
        cont++
        viewCarrinho.innerHTML +=
    `<div class="car_box" id="ex${cont}">
        <i id="excluir" class="ex${cont}">X</i>
        <h3> viage de ${valor[0].origem} para ${valor[0].destino}</h3>
        <span></span>
        <p id="${valor[0].numero_voo}">preço ${valor[0].preco}</p>
        <p>Numero do voo:${valor[0].numero_voo}</p>
    </div>`
    }
}


viewCarrinho.addEventListener('click', (evt) =>{
    
    if (evt.target.id == 'excluir'){
       let classe = evt.target.getAttribute('class')
       let parent = document.querySelector(`#${classe}`)
       let filho = parent.querySelector('p')
       parent.remove()

       fetch(`http://127.0.0.1:8000/search/carrinho/remove/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'num_voo': filho.id,
            'user': localStorage.getItem('user_id')
        })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error))
       
    }
})




