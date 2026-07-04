async function loadBookmarks() {
    const res = await fetch("/api/bookmarks");
    const bookmarks = await res.json();

    const list = document.getElementById("bookmarkList");
    list.innerHTML = "";

    bookmarks.forEach((b, index) => {
        list.innerHTML += `
        <div class="bookmark">
            <h3>${b.title}</h3>
            <a href="${b.url}" target="_blank">${b.url}</a>
            <p>${b.description || ""}</p>
            <button onclick="deleteBookmark(${index})">Delete</button>
        </div>
        `;
    });
}

async function addBookmark() {
    const title = document.getElementById("title").value;
    const url = document.getElementById("url").value;
    const description = document.getElementById("description").value;

    if (!title || !url) return;

    await fetch("/api/bookmarks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, url, description })
    });

    document.getElementById("title").value = "";
    document.getElementById("url").value = "";
    document.getElementById("description").value = "";

    loadBookmarks();
}

async function deleteBookmark(index) {
    await fetch(`/api/bookmarks/${index}`, {
        method: "DELETE"
    });

    loadBookmarks();
}

loadBookmarks();