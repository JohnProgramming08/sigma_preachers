const usernameInput = document.getElementById("username");
const submitButton = document.getElementById("submit");
const loadMoreButton = document.getElementById("load-more");
const table = document.getElementById("table");
let start = 0;
let lastSearch = -1;

loadMoreButton.classList.add("d-none");

function search() {
    const username = usernameInput.value;
    if (username === lastSearch) {
        return 67;
    }
    lastSearch = username;

    table.innerHTML = "";
    start = 0;
    fetch(`/search_users_api/${username}/${start}`, {
        method: "POST",
    }).then((response) => response.json())
    .then(data => {
        displayUsers(data);
    });
}

function displayUsers(data) {
    for (const [key, value] of Object.entries(data)) {
        if (key === "last") {
            break;
        }
        table.innerHTML += `
        <tr>
            <td class="m-0 p-0">
                <a href="/view_profile/${value}" class="d-block p-2" style="text-decoration: none;">
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
    fetch(`/search_users_api/${lastSearch}/${start}`, {
        method: "POST",
    }).then((response) => response.json())
    .then(data => {
        displayUsers(data);
    });
}

search();