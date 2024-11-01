// Находим элементы
const mainScreen = document.getElementById('mainScreen');
const questionScreen = document.getElementById('questionScreen');
const startButton = document.getElementById('startButton');
const yesButton = document.getElementById('yesButton');
const noButton = document.getElementById('noButton');

// Функция для плавного переключения экранов
function switchScreen(from, to) {
    from.style.opacity = '0';
    setTimeout(() => {
        from.style.display = 'none';
        to.style.display = 'block';
        setTimeout(() => {
            to.style.opacity = '1';
        }, 50);
    }, 500);
}

// Обработчик нажатия на кнопку "Начать тест"
startButton.addEventListener('click', () => {
    switchScreen(mainScreen, questionScreen);
});

// Обработчик нажатия на кнопку "Да"
yesButton.addEventListener('click', () => {
    // Переход на страницу в папке question1
    window.location.href = './question1/index.html';
});

// Обработчик нажатия на кнопку "Нет"
noButton.addEventListener('click', () => {
    // Плавное возвращение к начальному экрану
    switchScreen(questionScreen, mainScreen);
});
