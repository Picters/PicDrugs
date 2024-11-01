// Находим элементы
const scareText = document.getElementById('scareText');
const questionContainer = document.getElementById('questionContainer');
const yesButton = document.getElementById('yesButton');
const noButton = document.getElementById('noButton');

// Показать вопрос после 1 секунды
setTimeout(() => {
    scareText.style.display = 'none';
    questionContainer.style.display = 'block';
}, 1000); // Текст "Обернись" будет показан только 1 секунду

// Обработчик нажатия на кнопку "Да"
yesButton.addEventListener('click', () => {
    // Переход на следующую страницу вопроса
    window.location.href = '../question5/index.html';
});

// Обработчик нажатия на кнопку "Нет"
noButton.addEventListener('click', () => {
    // Переход на следующую страницу вопроса
    window.location.href = '../question5/index.html';
});
