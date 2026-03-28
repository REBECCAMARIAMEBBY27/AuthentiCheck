let currentTab = "text";

// Switch tabs
function switchTab(type, element) {
    currentTab = type;

    document.querySelectorAll(".tab").forEach(btn => btn.classList.remove("active"));
    element.classList.add("active");

    const textInput = document.getElementById("textInput");
    const preview = document.getElementById("previewImage");

    if (type === "text") {
        textInput.style.display = "block";
        preview.style.display = "none";
    } else {
        textInput.style.display = "none";
    }
}

// File handling
document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    const preview = document.getElementById("previewImage");

    if (!file) return;

    if (currentTab === "image") {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    } else {
        preview.style.display = "none";
    }
});

// Analyze
function analyze() {

    console.log("TAB:", currentTab);

    const textInput = document.getElementById("textInput");
    const fileInput = document.getElementById("fileInput");

    let formData = new FormData();

    if (currentTab === "text") {
        if (!textInput.value.trim()) {
            alert("Enter text!");
            return;
        }
        formData.append("text", textInput.value);
    }

    else if (currentTab === "image") {
        if (!fileInput.files[0]) {
            alert("Upload image!");
            return;
        }
        formData.append("image", fileInput.files[0]);
    }

    else if (currentTab === "audio") {
        if (!fileInput.files[0]) {
            alert("Upload audio!");
            return;
        }
        formData.append("audio", fileInput.files[0]);
    }

    fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData
    })
    .then(async res => {
        if (!res.ok) {
            const text = await res.text();
            throw new Error("Server error: " + text);
        }
        return res.json();
    })
    .then(data => {

        console.log("BACKEND RESPONSE:", data);

        let prediction = data.prediction;
        let confidence;

        // Case 1: confidence is 0–1
        if (data.confidence <= 1) {
            const ai = data.confidence * 100;
            const human = 100 - ai;

            if (prediction === "AI Generated") {
                confidence = ai;
            } else {
                confidence = human;
            }
        }

        // Case 2: confidence already 0–100
        else {
            confidence = data.confidence;
        }

        confidence = Math.round(confidence);

        const resultDiv = document.getElementById("result");

        const color = prediction === "AI Generated" ? "#ef4444" : "#22c55e";

        resultDiv.innerHTML = `
            <h2 style="color:${color}">${prediction}</h2>
            <p>Confidence: ${confidence}%</p>
        `;
    })
    .catch(err => {
        console.error("ERROR:", err);
        alert(err.message);
    });
}