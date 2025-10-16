const signup_submit = document.getElementById("signup_submit")
const login_submit = document.getElementById("login_submit")

signup_submit.addEventListener("click", async() => {

    const signup_username = document.getElementById("signupUsername").value
    const signup_password1 = document.getElementById("signupPassword1").value
    const signup_password2 = document.getElementById("signupPassword2").value

    const response = await fetch("/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "username": signup_username,
            "password1": signup_password1,
            "password2": signup_password2,
        }),
    })

    const data = await response.text()

        if (data.includes("Username already exists")) {
            alert("Username already exists")
        }
        else if (data.includes("Passwords do not match")) {
            alert("Passwords do not match")
        }
        else if (data.includes("Password must be at least 6 characters long")) {
            alert("Password must be at least 6 characters long")
        }
        else if (data.includes("Signup successful")) {
            alert("Account created successfully")               /* make it more aesthetic with the .warning class */
        }
})
