const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

function appendMessage(text, sender, typing = false) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    if (typing) div.classList.add("typing");
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    input.value = "";

    const typingDiv = appendMessage("Agent đang nhập...", "agent", true);

    try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        const data = await res.json();
        typingDiv.remove();
        appendMessage(data.reply, "agent");
    } catch (err) {
        typingDiv.remove();
        appendMessage("Lỗi kết nối server", "agent");
    }
}

input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});
