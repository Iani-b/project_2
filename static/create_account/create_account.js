function buttonRedirect(id, url) {
    const button = document.getElementById(id)

    button.addEventListener("click", async(eventObject) => {
        eventObject.preventDefault();

        button.disabled = true;
        await new Promise(timer => setTimeout(timer, 10));
        button.disabled = false;
        window.location.href = url;
    }); 
};

function displayResult(givenResult) {
    if (givenResult.type.includes("warning")) {
        document.getElementById("info").textContent = givenResult.message;
        document.getElementById("info").classList.add("warning");
    }
    else if (givenResult.type.includes("success")) {
        document.getElementById("info").textContent = givenResult.message;
        document.getElementById("info").classList.add("success");
        setTimeout(() => {window.location.href = "/"}, 1000);
    }
};

const form = document.getElementById("create_account_form");

form.addEventListener("submit", async(eventObject) => {
    eventObject.preventDefault();

    document.getElementById("info").classList.remove("warning", "success");
    document.getElementById("info").textContent = "";

    const response = await fetch("/create_account/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            "username": document.getElementById("createAcc_username").value,
            "password1": document.getElementById("createAcc_password1").value,
            "password2": document.getElementById("createAcc_password2").value,
            "date_of_birth": document.getElementById("createAcc_dob").value,
        }),
    });

    const result = await response.json();
    await new Promise(timer => setTimeout(timer, 10));

    displayResult(result);
})

buttonRedirect("dashboard","/")