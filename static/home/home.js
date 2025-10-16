const signup_submit = document.getElementById("signup_submit");

signup_submit.addEventListener("click", async(event) => {
    event.preventDefault();

    const signup_username = document.getElementById("signupUsername").value.trim();
    const signup_password1 = document.getElementById("signupPassword1").value;
    const signup_password2 = document.getElementById("signupPassword2").value;

    const response = await fetch("/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            "username": signup_username,
            "password1": signup_password1,
            "password2": signup_password2,
        })
    })

    const result = await response.json()

    if (result.message.includes("Username cannot be blank")) {
         document.getElementById("warning1").textContent = result.message;
         document.getElementById("warning1").classList.add("show_warning");
    }    
    else if (result.message.includes("Username already exists")) {
        document.getElementById("warning1").textContent = result.message;
        document.getElementById("warning1").classList.add("show_warning");
    }
    else if (result.message.includes("Passwords do not match")) {
        document.getElementById("warning1").textContent = result.message;
        document.getElementById("warning1").classList.add("show_warning");
    }
    else if (result.message.includes("Password must be at least 6 characters long")) {
        document.getElementById("warning1").textContent = result.message;
        document.getElementById("warning1").classList.add("show_warning");
    }
    else if (result.message.includes("Signup successful")) {
        document.getElementById("warning1").classList.remove("show_warning");
        window.location.href = "/game";
        }
})

const login_submit = document.getElementById("login_submit")
