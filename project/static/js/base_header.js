const homeLink = document.getElementById("home");
const profileLink = document.getElementById("profile");
const searchUsersLink = document.getElementById("search-users");
const searchRoomsLink = document.getElementById("search-rooms");
const contactUsLink = document.getElementById("contact-us");
const adminMessagesLink = document.getElementById("admin-messages");

const path = window.location.pathname;
let page = path.split("/");

while (["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"].indexOf(page.slice(-1)[0]) > -1) {
    page.pop();
}
page = page.pop();

const mapping = {
    "home": homeLink,
    "view_profile": profileLink,
    "edit_profile": profileLink,
    "ban_user": profileLink,
    "promote_user": profileLink,
    "search_users": searchUsersLink,
    "search_rooms": searchRoomsLink,
    "contact_us": contactUsLink,
    "admin_messages": adminMessagesLink
}

const pageLink = mapping[page];
pageLink.classList.add("active");
