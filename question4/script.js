// Находим элементы
const scareText = document.getElementById('scareText');
const questionContainer = document.getElementById('questionContainer');
const yesButton = document.getElementById('yesButton');
const noButton = document.getElementById('noButton');
const whiteNoise = document.getElementById('whiteNoise');

// Устанавливаем громкость белого шума на 100%
whiteNoise.volume = 1.0;

// Показать вопрос после 1 секунды
setTimeout(() => {
    scareText.style.display = 'none';
    questionContainer.style.display = 'block';

    // Устанавливаем громкость на 50% после исчезновения текста "Обернись"
    whiteNoise.volume = 0.5;
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
