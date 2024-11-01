// Находим элементы
const codeInput = document.getElementById('codeInput');
const submitButton = document.getElementById('submitButton');

// Обработчик нажатия на кнопку отправки
submitButton.addEventListener('click', () => {
    const code = codeInput.value;

    if (code === "666") {
        activateBlackout();
    } else if (code === "333") {
        simulateHighLoad();
    } else {
        alert("Неверный код. Попробуйте снова.");
    }
});

// Функция для черного экрана с надписью "Зря"
function activateBlackout() {
    document.body.innerHTML = "<div id='blackout'>Зря.</div>";
    localStorage.setItem('siteBlocked', 'true');
}

// Функция для симуляции высокой нагрузки
function simulateHighLoad() {
    let heavyCalculation = 0;

    // Нагрузочный цикл
    for (let i = 0; i < 1e8; i++) {
        heavyCalculation += Math.sqrt(i);
    }

    alert("Тест завершен. Нагрузка симулирована.");
}

// Проверка блокировки при загрузке страницы
if (localStorage.getItem('siteBlocked') === 'true') {
    activateBlackout();
}
