async function runCode() {
    const code = document.getElementById("code").value;
    const language = document.getElementById("language").value;
    const input = document.getElementById("input").value;
    const user_id = localStorage.getItem("user_id");

    const res = await fetch("/run", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code, language, input, user_id })
    });

    const data = await res.json();

    let output = "";

    if (data.stdout) {
        output = data.stdout;
    } else if (data.stderr) {
        output = data.stderr;
    } else if (data.compile_output) {
        output = data.compile_output;
    } else {
        output = "No output";
    }

    document.getElementById("output").innerText = output;
}