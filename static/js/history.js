async function getHistory() {
    const user_id = localStorage.getItem("user_id");

    const res = await fetch(`/history/${user_id}`);
    const data = await res.json();

    document.getElementById("history").innerText =
        JSON.stringify(data, null, 2);
}