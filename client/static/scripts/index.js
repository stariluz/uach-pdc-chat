async function loadEnv() {
    const response = await fetch('/env'); // Cambia '/env' por el endpoint que estés usando
    
    const env = await response.json();
    console.log(env);
    
    return env.SERVER;
}
loadEnv().then((SERVER) => {

    const API = `${SERVER}/ws/`;
    console.log((API))

    var client_id = Date.now()
    document.querySelector("#ws-id").textContent = client_id;
    var ws = new WebSocket(`${API}${client_id}`);

    ws.onmessage = function (event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };

    function sendMessage(event) {
        var id_input = document.getElementById("targetID")
        var input = document.getElementById("messageText")
        /* var id = id_input.value.trim()
    
        ws.send(input.value)
        input.value = ''

        event.preventDefault()
    }
}).catch((error)=>{
    console.log("No se pudo obtener las variables de entorno", error);
})