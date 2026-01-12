const displayArea = document.getElementById("display-area");
const mainInput = document.getElementById("main-input");
const sendBtn = document.getElementById("send-btn");

function addMessage(text, type) {
    const html = `
        <div class="msg ${type}">
            <div class="icon"><i class="fas fa-${
                type === "user" ? "user" : "robot"
            }"></i></div>
            <div class="bubble">${text}</div>
        </div>
    `;
    displayArea.insertAdjacentHTML("beforeend", html);
    displayArea.scrollTop = displayArea.scrollHeight;
}

function quickAction(cmd) {
    addMessage(`Tôi muốn đăng ký ${cmd}`, "user");

    setTimeout(() => {
        let response = "";
        const time = new Date().toLocaleTimeString();
        if (cmd === "vào")
            response = `Đã xác nhận **Vào** lúc ${time}. Chúc bạn làm việc hiệu quả!`;
        else if (cmd === "ra")
            response = `Đã xác nhận **Ra** lúc ${time}. Hẹn gặp lại bạn!`;
        else response = "Hiện tại trạng thái của bạn là: Đang có mặt.";

        addMessage(response, "bot");
    }, 600);
}

sendBtn.onclick = () => {
    if (!mainInput.value.trim()) return;
    addMessage(mainInput.value, "user");
    mainInput.value = "";
};

mainInput.onkeypress = (e) => {
    if (e.key === "Enter") sendBtn.click();
};
