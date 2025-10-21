const logout_btn = document.getElementById("logout_btn")

logout_btn.addEventListener("click", async(event) => {
    event.preventDefault();

    document.getElementById("info").classList.remove("warning", "success");
    document.getElementById("info").textContent = "";

    const response = await fetch("/dashboard/logout", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            "log_out": true
        })
    })

    const result = await response.json()

    setTimeout(() => {                                     /* Like time.sleep(), in ms, makes sure animation loads */
        if (result.type.includes("success")) {
         document.getElementById("info").textContent = result.message;
         document.getElementById("info").classList.add("success");
         setTimeout(() => {
            window.location.href = "/";
         }, 1000)
        }    
        else if (result.type.includes("error")) {
            document.getElementById("info").textContent = result.message;
            document.getElementById("info").classList.add("warning");
            alert("Something Went Wrong")
        }
    }, 10)
})