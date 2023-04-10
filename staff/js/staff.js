let estados_br = 
[['AC', 'Acre'],
['AL', 'Alagoas'],
['AP', 'Amapá'],
['AM', 'Amazonas'],
['BA', 'Bahia'],
['CE', 'Ceará'],
['DF', 'Distrito Federal'],
['ES', 'Espírito Santo'],
['GO', 'Goiás'],
['MA', 'Maranhão'],
['MT', 'Mato Grosso'],
['MS', 'Mato Grosso do Sul'],
['MG', 'Minas Gerais'],
['PA', 'Pará'],
['PB', 'Paraíba'],
['PR', 'Paraná'],
['PE', 'Pernambuco'],
['PI', 'Piauí'],
['RJ', 'Rio de Janeiro'],
['RN', 'Rio Grande do Norte'],
['RS', 'Rio Grande do Sul'],
['RO', 'Rondônia'],
['RR', 'Roraima'],
['SC', 'Santa Catarina'],
['SP', 'São Paulo'],
['SE', 'Sergipe'],
['TO', 'Tocantins']
]
let origem = document.querySelector('.select_origem')
let destino = document.querySelector('.select_destino')
let dt_partida = document.querySelector('.data_partida')
let dt_chegada = document.querySelector('.data_chegada')
let lu_disponiveis = document.querySelector('.lu_disponiveis')
let preco = document.querySelector('.preco')
let num_voo = document.querySelector('.num_voo')

for (let i = 0; i < 27; i++){

let option = document.createElement('option')
option.value = estados_br[i][0]
option.textContent = estados_br[i][1]
destino.appendChild(option)

let option2 = document.createElement('option')
option2.value = estados_br[i][0]
option2.textContent = estados_br[i][1]
origem.appendChild(option2)
}
document.querySelector('section').addEventListener('click', (event) =>{
origin = event.target
// console.log(origin.value)
})

function getForm(){

  fetch('http://127.0.0.1:8000/staff/voos', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        'origem':origem.value,
        'destino':destino.value,
        'data_partida':dt_partida.value,
        'data_chegada':dt_chegada.value,
        'lugares_disponiveis':lu_disponiveis.value,
        'preco':preco.value,
        'numero_voo':num_voo.value,
    })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log(error))

}


