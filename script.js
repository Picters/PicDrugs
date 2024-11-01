// Функция для трансформации кнопки "Генератор" в три кнопки
function transformButton() {
    const generatorButton = document.getElementById('generatorButton');
    const buttonContainer = document.getElementById('buttonContainer');

    // Добавляем класс для анимации расширения
    generatorButton.classList.add('expand');

    // Плавно показываем три кнопки после короткой задержки
    setTimeout(() => {
        generatorButton.style.display = 'none'; // Скрываем кнопку "Генератор"
        buttonContainer.classList.add('visible'); // Показываем три кнопки
    }, 500); // Задержка в 500 мс для завершения анимации
}

// Функция для обработки нажатия кнопок
function generate(type) {
    console.log(`Генерация ${type}`);
}
