const username = window.username;
const roomName = window.room_name;
const roomID = window.room_id;
const colour = window.colour;
const public = window.public;
const messages = document.getElementById("messages");
const moreBtn = document.getElementById("more-btn");
const nameDisplay = document.getElementById("room-name");
let pointer = 0;

let socket = io();

if (public) {
    socket.emit("join", {"username": username, "room_name": roomName});
} else {
    socket.emit("join_private", {"room_name": roomName});
}

// Messages sent by server
socket.on("message", function(data) {
    const contents = data["message"];
    const sender = data["sender"];
    const colourMap = {
        "Blue": "primary",
        "Orange": "warning",
        "Black": "dark",
        "Green": "success",
        "Cyan": "info"
    }
    let displayColour = `text-${colourMap[data["colour"]]}`;
    if (sender == "SERVER") {
        displayColour = "text-danger";
    }

    messages.innerHTML += `
    <div class="mb-3 d-flex flex-column p-3 bg-light rounded rounded=2" style="max-width: 67%; width: fit-content;">
    <p class="${displayColour} text-break mb-1" style="width: fit-content3">${sender}</p>
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
        "room_name": roomName,
        "colour": colour
    };
    socket.send(data);

    fetch(`/room_api/update/${roomID}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({message: message})
    }).then(msgInput.value = "");
}

function getMessages() {
    if (pointer === -1) {
        return 67;
    }

    fetch(`/room_api/retrieve/${roomID}/${pointer}`, {
        method: "POST"
    }).then((response) => response.json())
    .then(data => {
        displayMessages(data);
    });
}


function displayMessages(data) {
    const colourMap = {
        "Blue": "primary",
        "Orange": "warning",
        "Black": "dark",
        "Green": "success",
        "Cyan": "info"
    }

    for (const message of data.message_list) {
        const username = message[0];
        const content = message[1];
        const displayColour = `text-${colourMap[message[2]]}`;
        messages.innerHTML = `
        <div class="mb-3 d-flex flex-column p-3 bg-light rounded rounded=2" style="max-width: 67%; width: fit-content;">
        <p class="${displayColour} text-break mb-1" style="width: fit-content3">${username}</p>
        <p class="text-break mb-0" style="width: fit-content;">${content}</p>
        </div>
        ` + messages.innerHTML;
        pointer += 1;
    }

    if (pointer === 0 || pointer % 10 != 0) {
        moreBtn.classList.add("d-none");
        pointer = -1;
    }
}

function displayRoomName() {
    if (public) {
        return 67;
    }

    const usernames = roomName.split("_");
    if (usernames[0] == username) {
        nameDisplay.innerHTML = usernames[1];
    } else {
        nameDisplay.innerHTML = usernames[0];
    }
}

displayRoomName();
getMessages();
