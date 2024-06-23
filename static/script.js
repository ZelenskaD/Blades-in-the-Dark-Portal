// // Spinner JS
//
// document.addEventListener('DOMContentLoaded', () => {
//     const spinner = document.getElementById('spinner');
//     const spinButton = document.getElementById('spinButton');
//
//     spinButton.addEventListener('click', () => {
//         fetch('/spin')
//             .then(response => response.json())
//             .then(data => {
//                 const randomNumber = data.number;
//                 spinner.style.transform = 'rotate(0deg)';
//                 setTimeout(() => {
//                     spinner.textContent = randomNumber;
//                     spinner.style.transform = 'rotate(360deg)';
//                 }, 100);
//             });
//     });
// });