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
    alert('Вы выбрали: Да');
    // Здесь можно добавить логику для начала теста
});

// Обработчик нажатия на кнопку "Нет"
noButton.addEventListener('click', () => {
    alert('Вы выбрали: Нет');
    // Здесь можно добавить логику для отмены теста
    switchScreen(questionScreen, mainScreen); // Возвращение на начальный экран
});
