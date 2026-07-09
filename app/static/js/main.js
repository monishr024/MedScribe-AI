document.querySelectorAll(".selection-group").forEach(group => {

    const cards = group.querySelectorAll(".selection-card");

    cards.forEach(card => {

        card.addEventListener("click", () => {

            cards.forEach(c => c.classList.remove("selected"));

            card.classList.add("selected");

        });

    });

});

/* ==========================================
   Smooth Sidebar Navigation
========================================== */

const steps = document.querySelectorAll(".step-item");

steps.forEach(step => {

    step.addEventListener("click", () => {

        const section = document.getElementById(
            step.dataset.target
        );

        if(section){

            section.scrollIntoView({

                behavior:"smooth",

                block:"start"

            });

        }

    });

});

/* ==========================================
   Active Sidebar
========================================== */

const sections = document.querySelectorAll(".medical-card");

window.addEventListener("scroll",()=>{

    let current="";

    sections.forEach(section=>{

        const top=section.offsetTop-180;

        if(scrollY>=top){

            current=section.id;

        }

    });

    steps.forEach(step=>{

        step.classList.remove("active");

        if(step.dataset.target===current){

            step.classList.add("active");

        }

    });

});

/* ==========================================
   Progress Bar
========================================== */

const progress=document.getElementById("formProgress");

const requiredInputs=document.querySelectorAll(

"input[required], textarea[required]"

);

function updateProgress(){

    let completed=0;

    requiredInputs.forEach(input=>{

        if(input.value.trim()!==""){

            completed++;

        }

    });

    const percentage=Math.round(

        completed/

        requiredInputs.length*100

    );

    progress.style.width=percentage+"%";

    progress.innerHTML=percentage+"%";

}

requiredInputs.forEach(input=>{

    input.addEventListener("input",updateProgress);

});

/* ==========================================================
                AI LOADING SCREEN
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    const overlay = document.getElementById("loadingOverlay");

    const progressBar = document.getElementById("progressBar");

    const message = document.getElementById("loadingMessage");

    if (!form || !overlay) return;

    const messages = [

        "Analyzing Patient Information...",

        "Reviewing Vital Signs...",

        "Evaluating Clinical Findings...",

        "Generating Differential Diagnosis...",

        "Recommending Laboratory Tests...",

        "Preparing Treatment Plan...",

        "Finalizing Clinical Report..."

    ];

    form.addEventListener("submit", function () {

        overlay.style.display = "flex";

        const btn = document.getElementById("generateBtn");

        if (btn) {

            btn.disabled = true;

            btn.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin me-2"></i> Generating...';

        }

        let progress = 0;

        let step = 0;

        progressBar.style.width = "0%";

        message.innerText = messages[0];

        const interval = setInterval(() => {

            progress += 2;

            progressBar.style.width = progress + "%";

            if (progress >= 100) {

                clearInterval(interval);

            }

        }, 120);

        const textInterval = setInterval(() => {

            step++;

            if (step < messages.length) {

                message.innerText = messages[step];

            } else {

                clearInterval(textInterval);

            }

        }, 1500);

    });

});