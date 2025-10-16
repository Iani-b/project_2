const signup_submit = document.getElementById("signup_submit");

signup_submit.addEventListener("click", async(event) => {
    event.preventDefault();

    document.getElementById("info").classList.remove("warning", "success");
    document.getElementById("info").textContent = "";

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
    
    setTimeout(() => {                                     /* Like time.sleep(), in ms, makes sure animation loads */
        if (result.type.includes("invalid_username")) {
         document.getElementById("info").textContent = result.message;
         document.getElementById("info").classList.add("warning");
        }    
        else if (result.type.includes("existing_username")) {
            document.getElementById("info").textContent = result.message;
            document.getElementById("info").classList.add("warning");
        }
        else if (result.type.includes("different_passwords")) {
            document.getElementById("info").textContent = result.message;
            document.getElementById("info").classList.add("warning");
        }
        else if (result.type.includes("invalid_password")) {
            document.getElementById("info").textContent = result.message;
            document.getElementById("info").classList.add("warning");
        }
        else if (result.type.includes("signup_success")) {
            document.getElementById("info").textContent = result.message;
            document.getElementById("info").classList.add("success");
        }
    }, 10)
})

const login_submit = document.getElementById("login_submit")
