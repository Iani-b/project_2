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

const find_user_form = document.getElementById("find_user_form");

find_user_form.addEventListener("submit", async(eventObject) => {
    eventObject.preventDefault();

    document.getElementById("info").classList.remove("warning");
    document.getElementById("info").textContent = "";

    const response = await fetch("/view_accounts/find", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"username": document.getElementById("viewAcc_username").value})
    });

    const result = await response.json();
    await new Promise(timer => setTimeout(timer, 10));

    if (result.type.includes("success")) {
        document.getElementById("date_of_birth").textContent = result.date_of_birth;
        document.getElementById("last_game_result").textContent = result.last_game;
        document.getElementById("wins").textContent = result.wins;
        document.getElementById("losses").textContent = result.losses;
    }
    else if (result.type.includes("warning")) {
        document.getElementById("info").classList.add("warning");
        document.getElementById("info").textContent = result.message;
    };
});

buttonRedirect("dashboard", "/")

