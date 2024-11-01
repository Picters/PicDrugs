// Находим кнопки
const yesButton = document.getElementById('yesButton');
const noButton = document.getElementById('noButton');

// Обработчик нажатия на кнопку "Да"
yesButton.addEventListener('click', () => {
    // Переход на следующий вопрос
    window.location.href = '../question2/index.html';
});

// Обработчик нажатия на кнопку "Нет"
noButton.addEventListener('click', () => {
    // Переход на следующий вопрос
    window.location.href = '../question2/index.html';
});
