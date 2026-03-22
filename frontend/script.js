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

// Animate %
function animateCounter(el, target) {
    let count = 0;
    let interval = setInterval(() => {
        if (count >= target) clearInterval(interval);
        else {
            count++;
            el.innerText = count + "%";
        }
    }, 10);
}

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
    .then(res => res.json())
    .then(data => {
        const ai = Math.round(data.confidence);
        const human = 100 - ai;

        animateCounter(document.getElementById("aiPercent"), ai);
        animateCounter(document.getElementById("humanPercent"), human);

        document.getElementById("aiBar").style.width = ai + "%";
        document.getElementById("humanBar").style.width = human + "%";
    })
    .catch(() => alert("Backend error"));
}