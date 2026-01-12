const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

/**
 * Thêm tin nhắn vào khung chat
 * @param {string} text - Nội dung tin nhắn
 * @param {string} sender - 'user' hoặc 'bot'
 * @param {boolean} isBot - Xác định icon hiển thị
 */
function appendMessage(text, sender, isBot = false) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `msg ${sender}`;

    const iconClass = isBot ? "fas fa-robot" : "fas fa-user";

    msgDiv.innerHTML = `
        <div class="icon"><i class="${iconClass}"></i></div>
        <div class="bubble">${text}</div>
    `;

    chatBox.appendChild(msgDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    input.value = "";

    const typingDiv = appendMessage(
        "Đang chuẩn bị thực đơn cho bạn...",
        "bot",
        true
    );

    try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        });

        if (!res.ok) throw new Error("Lỗi kết nối server");

        const data = await res.json();

        typingDiv.remove();
        appendMessage(data.message, "bot", true);
    } catch (err) {
        typingDiv.remove();
        appendMessage(
            "Rất tiếc, tôi không thể kết nối với nhà bếp lúc này. Vui lòng thử lại sau!",
            "bot",
            true
        );
        console.error("Chat Error:", err);
    }
}

function quickOrder(type) {
    let prompt = "";
    switch (type) {
        case "Thực đơn":
            prompt = "Cho tôi xem thực đơn hôm nay";
            break;
        case "Gợi ý":
            prompt = "Gợi ý cho tôi vài món ngon nhé";
            break;
        case "Đơn hàng":
            prompt = "Kiểm tra trạng thái đơn hàng của tôi";
            break;
        default:
            prompt = type;
    }
    input.value = prompt;
    sendMessage();
}

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});
