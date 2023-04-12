let container = document.querySelector('.conteiner')
const dados = JSON.parse(localStorage.getItem('data'))

function load_passagens() {
    fetch('http://127.0.0.1:8000/voos/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'origem': dados.origem,
            'destino': dados.destino,
        })
        })
        .then(response => response.json())
        .then(data => readPagePassagens(data))
        .catch(error => {
            window.alert("algo deu errado /:")
            console.log(error)
        })
}


function readPagePassagens(dados) {
    for (valor of dados) {
        container.innerHTML +=
    `<div>
        <h3> viage de ${valor.origem} para ${valor.destino}</h3>
        <span><p></p></span>
        <p>preço ${valor.preco}</p>
    </div>`
    }
}

load_passagens()
