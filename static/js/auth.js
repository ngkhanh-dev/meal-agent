function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie =
        name + "=" + (value || "") + expires + "; path=/; SameSite=Lax";
}

async function handleLogin(event) {
    event.preventDefault();
    const user = document.getElementById("login-username").value;
    const pass = document.getElementById("login-password").value;
    const messageTag = document.getElementById("message");

    try {
        console.log("Đang đăng nhập cho:", user);

        const fakeToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";

        setCookie("access_token", fakeToken, 7);

        messageTag.style.color = "#2ecc71";
        messageTag.innerText = "Đăng nhập thành công! Đang chuyển hướng...";

        setTimeout(() => {
            window.location.href = "/gateway";
        }, 1000);
    } catch (error) {
        messageTag.style.color = "red";
        messageTag.innerText = "Lỗi đăng nhập! Vui lòng kiểm tra lại.";
    }
}
