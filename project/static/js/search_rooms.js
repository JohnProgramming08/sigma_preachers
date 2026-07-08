const roomInput = document.getElementById("room-entry");
const submitButton = document.getElementById("submit");
const loadMoreButton = document.getElementById("load-more");
const table = document.getElementById("table");
let start = 0;
let lastSearch = -1;

loadMoreButton.classList.add("d-none");

function search() {
    const roomStart = roomInput.value;
    if (roomStart === lastSearch) {
        return 67;
    }
    lastSearch = roomStart;

    table.innerHTML = "";
    start = 0;
    let url = `/search_rooms_api/${roomStart}/${start}`;
    if (roomStart === "") {
        url = `search_all_rooms_api/${start}`;
    }

    fetch(url, {
        method: "POST",
    }).then((response) => response.json())
    .then(data => {
        displayUsers(data);
    });
}

function displayUsers(data) {
    for (const [key, value] of Object.entries(data)) {
        table.innerHTML += `
        <tr>
            <td class="m-0 p-0">
                <a href="/join_room/${value}" class="d-block p-2" style="text-decoration: none;">
                ${key}
                </a>
            </td>
        </tr>
        `;
        start += 1;
    }

    if (start % 10 === 0 && start != 0) {
        loadMoreButton.classList.remove("d-none");
    } else {
        loadMoreButton.classList.add("d-none");
    }
}


function loadMore() {
    let url = `/search_rooms_api/${lastSearch}/${start}`;
    if (lastSearch === "") {
        url = `search_all_rooms_api/${start}`;
    }

    fetch(url, {
        method: "POST",
    }).then((response) => response.json())
    .then(data => {
        displayUsers(data);
    });
}

search();