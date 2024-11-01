// Находим кнопки
const yesButton = document.getElementById('yesButton');
const noButton = document.getElementById('noButton');

// Обработчик нажатия на кнопку "Да"
yesButton.addEventListener('click', () => {
    // Удаляем darkMode, если он был установлен
    localStorage.removeItem('darkMode');
    // Переход на следующую страницу вопроса
    window.location.href = '../question4/index.html';
});

// Обработчик нажатия на кнопку "Нет"
noButton.addEventListener('click', () => {
    // Устанавливаем darkMode в true
    localStorage.setItem('darkMode', 'true');
    // Переход на следующую страницу вопроса
    window.location.href = '../question4/index.html';
});
