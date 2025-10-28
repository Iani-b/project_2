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

buttonRedirect("leaderboard","/leaderboard");
buttonRedirect("view_accounts","/view_accounts");
buttonRedirect("create_account","/create_account");
buttonRedirect("bottom_play_button","/play");