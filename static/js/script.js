//login.html
async function login() {
    const password = document.getElementById("password").value;

    const res = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password })
    });

    if (res.ok) {
        window.location.href = "/dashboard";
    } else {
        document.getElementById("error").innerText = "Wrong password";
    }
}

function handleKeyDown(event) {
    if (event.key === "Enter") {
        login();
    }
}

const asciiArt = document.getElementById("ascii-art");
const threshold = 30;

const wrappedText = asciiArt.textContent
    .split("")
    .map(char => `<span class="char">${char === " " ? "&nbsp;" : char}</span>`)
    .join("");
  asciiArt.innerHTML = wrappedText;

  document.addEventListener("mousemove", (e) => {
    const mouseX = e.clientX;
    const mouseY = e.clientY;

    const chars = document.querySelectorAll(".char");

    chars.forEach(char => {
      const charRect = char.getBoundingClientRect();
      const charX = charRect.left + charRect.width / 2;
      const charY = charRect.top + charRect.height / 2;

      const distance = Math.sqrt(
        Math.pow(mouseX - charX, 2) + Math.pow(mouseY - charY, 2)
      );

      if (distance < threshold) {
        char.style.color = "#e4b558";
        char.style.fontWeight = "bold";
      } else {
        char.style.color = "";
        char.style.fontWeight = "";
      }
    });
  });


//dashboard.html
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