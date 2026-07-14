const titleDisplay = document.getElementById("message-title");
const usernameDisplay = document.getElementById("message-username");
const typeDisplay = document.getElementById("message-type");
const contentDisplay = document.getElementById("message-content");
const dismissButton = document.getElementById("dismiss-btn");
const filterInput = document.getElementById("filter-input");
const messages = Array.from(document.getElementsByClassName("admin-message"));

function getMessageData(messageID) {
    fetch(`/admin_messages_api/retrieve/${messageID}`, {
        method: "GET",
    }).then((response) => response.json())
    .then(data => {
        displayMessage(data);
    });
}

function displayMessage(data) {
    titleDisplay.innerHTML = data.title;
    usernameDisplay.innerHTML = `USERNAME: ${data.username}`;
    typeDisplay.innerHTML = data.message_type;
    contentDisplay.innerHTML = data.content;
    dismissButton.classList.remove("d-none");
    dismissButton.href = `/admin_messages/dismiss/${data.id}`;
}

function filter() {
    const valueMap = ["All", "Report", "Feature Request", "Chatroom Request", "Bug", "Other"];
    const value = valueMap[filterInput.value];

    if (value === "All") {
        for (const message of messages) {
            message.classList.remove("d-none");
        }
    } else {
        for (const message of messages) {
            if (message.classList.contains(value)) {
                message.classList.remove("d-none");
            } else {
                message.classList.add("d-none");
            }
        }
    }
}