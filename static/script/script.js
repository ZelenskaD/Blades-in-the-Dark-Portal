$(function () {
    $('[data-toggle="tooltip"]').tooltip({ delay: { "show": 0, "hide": 0 } });
});


document.addEventListener('DOMContentLoaded', function() {
    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function generateKeyframes(birdId, animationName) {
        const startLeft = getRandomInt(0, 100);
        const startTop = getRandomInt(0, 100);
        const endLeft = getRandomInt(0, 100);
        const endTop = getRandomInt(0, 100);

        const keyframes = `
            @keyframes ${animationName} {
                0% {
                    left: ${startLeft}%;
                    top: ${startTop}%;
                    transform: translate(-50%, -50%) scaleX(1);
                }
                50% {
                    left: ${endLeft}%;
                    top: ${endTop}%;
                    transform: translate(-50%, -50%) scaleX(1);
                }
                50.01% {
                    transform: translate(-50%, -50%) scaleX(-1);
                }
                100% {
                    left: ${startLeft}%;
                    top: ${startTop}%;
                    transform: translate(-50%, -50%) scaleX(-1);
                }
            }
        `;

        const styleSheet = document.createElement("style");
        styleSheet.type = "text/css";
        styleSheet.innerText = keyframes;
        document.head.appendChild(styleSheet);

        const bird = document.getElementById(birdId);
        bird.style.animation = `${animationName} ${getRandomInt(20, 40)}s linear infinite`;
    }

    function showBirds() {
        generateKeyframes('bird1', 'fly1');
        generateKeyframes('bird2', 'fly2');
        generateKeyframes('bird3', 'fly3');
        generateKeyframes('bird4', 'fly4');
        generateKeyframes('bird5', 'fly5');
        generateKeyframes('bird6', 'fly6');
    }

    // Initial call to show the birds with random trajectories
    showBirds();
});

