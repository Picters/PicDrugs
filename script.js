// Функция для преобразования кнопки
function transformButton() {
    const generatorButton = document.getElementById('generatorButton');
    const buttonContainer = document.getElementById('buttonContainer');
    
    // Анимация для скрытия кнопки "Генератор"
    generatorButton.style.transition = "transform 0.5s ease, opacity 0.5s ease";
    generatorButton.style.transform = "scale(0)";
    generatorButton.style.opacity = "0";
    
    // Показать новые кнопки после завершения анимации скрытия
    setTimeout(() => {
        generatorButton.style.display = 'none'; // Скрываем кнопку "Генератор"
        buttonContainer.style.opacity = '1'; // Показываем контейнер с новыми кнопками
        buttonContainer.style.pointerEvents = 'auto';
        
        // Добавляем класс видимости для каждой кнопки с задержкой для эффекта появления
        const buttons = document.querySelectorAll('.transform-button');
        buttons.forEach((button, index) => {
            setTimeout(() => {
                button.classList.add('visible');
            }, index * 100); // задержка между появлением кнопок
        });
    }, 500); // Задержка в 500 мс для завершения анимации
}

// Функция для обработки нажатия кнопок
function generate(type) {
    console.log(`Генерация ${type}`);
}
