// Загрузка Lottie-анимации
lottie.loadAnimation({
    container: document.getElementById('lottieContainer'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'animation.json'
});

// Функция для преобразования кнопки
function transformButton() {
    const generatorButton = document.getElementById('generatorButton');
    const buttonContainer = document.getElementById('buttonContainer');

    // Анимация кнопки "Генератор" при помощи GSAP
    gsap.to(generatorButton, {
        duration: 0.5,
        scaleX: 2,
        scaleY: 0.5,
        borderRadius: "10%",
        backgroundColor: "#ff0000",
        onComplete: () => {
            generatorButton.style.display = 'none'; // Скрываем кнопку "Генератор"
            buttonContainer.style.opacity = '1'; // Показываем новые кнопки
            buttonContainer.style.pointerEvents = 'auto';
            animateButtons();
        }
    });
}

// Функция для анимации новых кнопок
function animateButtons() {
    const buttons = document.querySelectorAll('.transform-button');
    buttons.forEach((button, index) => {
        gsap.fromTo(button, {
            scale: 0,
            rotation: 360
        }, {
            duration: 0.6,
            scale: 1,
            rotation: 0,
            delay: index * 0.2,
            ease: "back.out(1.7)"
        });
    });
}

// Функция для Canvas-анимации
function canvasAnimation() {
    const canvas = document.getElementById('backgroundCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function drawCircle(x, y, radius, color) {
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < 30; i++) {
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            const radius = Math.random() * 5 + 2;
            const color = `rgba(0, 150, 255, ${Math.random()})`;
            drawCircle(x, y, radius, color);
        }
        requestAnimationFrame(animate);
    }

    animate();
}

// Запускаем Canvas-анимацию
canvasAnimation();

// Функция для работы с WebGL (Three.js)
function initWebGL() {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x0077ff });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    camera.position.z = 5;

    function animate() {
        requestAnimationFrame(animate);
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
        renderer.render(scene, camera);
    }

    animate();
}

// Запускаем WebGL-анимацию
initWebGL();

function generate(type) {
    console.log(`Генерация ${type}`);
}
