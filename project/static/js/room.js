const username = window.username;
const roomName = window.room_name;
const messages = document.getElementById("messages");

let socket = io();

socket.emit("join", {"username": username, "room_name": roomName});

// Messages sent by server
socket.on("message", function(data) {
    const contents = data["message"];
    const sender = data["sender"];
    let colour = "text-primary";
    if (sender == "SERVER") {
        colour = "text-danger";
    }

    messages.innerHTML += `
    <div class="mb-3 d-flex flex-column p-3 bg-light rounded rounded=2" style="max-width: 67%; width: fit-content;">
    <p class="${colour} text-break mb-1" style="width: fit-content3">${sender}</p>
    <p class="text-break mb-0" style="width: fit-content;">${contents}</p>
    <div>
    `;
});

// Messages sent to server
function sendMessage() {
    let msgInput = document.getElementById("msg");
    let message = msgInput.value;
    if (message.length == 0) {
        return 67;
    }
    
    const data = {
        "message": message,
        "username": username,
        "room_name": roomName
    };
    socket.send(data);

    msgInput.value = "";
}

