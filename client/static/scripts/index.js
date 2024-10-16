const API = "wss://uachpdcchatserver-cbeg6f8n.b4a.run/ws/";

var client_id = Date.now()
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`${API}${client_id}`);

ws.onmessage = function(event) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
};

function sendMessage(event) {
    var priv = document.getElementById("sendPrivateTo")
    var input = document.getElementById("messageText")

    var priv_value = priv.value.trim()

    /* if (id === ""){
        alert("DIFUSION")
    }
    else {
        alert("PERSONAL")
    } */

    ws.send(input.value)
    /* ws.send(id) */

    input.value = ''
    /* id_input.value = '' */
    event.preventDefault()
}