let currentTab = "text";

function switchTab(type, element) {
    currentTab = type;

    document.querySelectorAll(".tab").forEach(btn => {
        btn.classList.remove("active");
    });

    element.classList.add("active");

    const textInput = document.getElementById("textInput");
    const fileInput = document.getElementById("fileInput");
    const preview = document.getElementById("previewImage");

    if (type === "text") {
        textInput.style.display = "block";
        preview.style.display = "none";
    } else {
        textInput.style.display = "none";
        fileInput.click();
    }

    fileInput.onchange = function () {
        if (type === "image") {
            const file = fileInput.files[0];
            preview.src = URL.createObjectURL(file);
            preview.style.display = "block";
        }
    };
}

function animateCounter(element, target) {
    let count = 0;
    let interval = setInterval(() => {
        if (count >= target) {
            clearInterval(interval);
        } else {
            count++;
            element.innerText = count + "%";
        }
    }, 15);
}

function analyze() {

    const btnText = document.getElementById("btnText");
    btnText.innerText = "Analyzing...";

    setTimeout(() => {

        let human = Math.floor(Math.random() * 100);
        let ai = 100 - human;

        animateCounter(document.getElementById("humanPercent"), human);
        animateCounter(document.getElementById("aiPercent"), ai);

        document.getElementById("humanBar").style.width = human + "%";
        document.getElementById("aiBar").style.width = ai + "%";

        btnText.innerText = "ANALYZE NOW";

    }, 1500);
}

/* Particle Background */

const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

for (let i = 0; i < 120; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 2,
        dx: (Math.random() - 0.5),
        dy: (Math.random() - 0.5)
    });
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#00f7ff";

    particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();

        p.x += p.dx;
        p.y += p.dy;

        if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
    });

    requestAnimationFrame(animateParticles);
}

animateParticles();