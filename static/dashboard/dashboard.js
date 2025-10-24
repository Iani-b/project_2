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
buttonRedirect("account_details","/account_details");
buttonRedirect("create_account","/create_account");
buttonRedirect("bottom_play_button","/play");