// Находим кнопки
const yesButton = document.getElementById('yesButton');
const noButton = document.getElementById('noButton');

// Обработчик нажатия на кнопку "Да"
yesButton.addEventListener('click', () => {
    // Переход на следующую страницу вопроса
    window.location.href = '../question3/index.html';
});

// Обработчик нажатия на кнопку "Нет"
noButton.addEventListener('click', () => {
    // Переход на следующую страницу вопроса
    window.location.href = '../question3/index.html';
});
