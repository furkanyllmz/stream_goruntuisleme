const character = document.getElementById("character");
const obstacle = document.getElementById("obstacle");
const scoreDisplay = document.getElementById("score");
const starsContainer = document.getElementById("stars");

let isJumping = false;
let score = 0;
let gameStarted = false;

// ⭐ Yıldız üretimi
function createStar() {
  const star = document.createElement("div");
  star.classList.add("star");
  star.style.top = Math.random() * 180 + "px";
  star.style.left = "800px";
  starsContainer.appendChild(star);
  setTimeout(() => starsContainer.removeChild(star), 6000);
}
setInterval(createStar, 1000);

// 🧍 Karakter seçimi
document.querySelectorAll(".char-icon").forEach(icon => {
  icon.addEventListener("click", () => {
    document.querySelectorAll(".char-icon").forEach(i => i.classList.remove("selected"));
    icon.classList.add("selected");
    const selectedChar = icon.getAttribute("data-char");
    character.style.backgroundImage = `url(${selectedChar})`;
  });
});

// 🦘 Zıplama (%15 daha hızlı)
function jump() {
  if (!gameStarted || isJumping) return;

  isJumping = true;
  let position = 0;
  let up = setInterval(() => {
    if (position >= 115) {
      clearInterval(up);
      let down = setInterval(() => {
        if (position <= 0) {
          clearInterval(down);
          isJumping = false;
        } else {
          position -= 6; // daha hızlı düşüş
          character.style.bottom = position + "px";
        }
      }, 17);
    } else {
      position += 6; // daha hızlı çıkış
      character.style.bottom = position + "px";
    }
  }, 17);
}

// 🚧 Engel oluşturma (sağdan sola, çarpışma kutusu ile)
function startGame() {
  if (gameStarted) return;
  gameStarted = true;

  function spawnObstacle() {
    const type = Math.random() > 0.5 ? "small" : "big";
    obstacle.style.height = type === "big" ? "50px" : "30px";
    obstacle.style.backgroundImage = `url(obstacle_${type}.png)`;

    let pos = 800;
    obstacle.style.left = pos + "px";
    obstacle.style.right = ""; // sağ tanımını temizle

    const move = setInterval(() => {
      if (pos < -40) {
        clearInterval(move);
        score += 4;
        scoreDisplay.textContent = `Skor: ${score}`;
        setTimeout(spawnObstacle, 600); // %25 daha az aralık
      } else {
        pos -= 5;
        obstacle.style.left = pos + "px";

        // 🎯 Çarpışma kutusu kontrolü
        const charBox = character.getBoundingClientRect();
        const obsBox = obstacle.getBoundingClientRect();

        const isColliding = !(
          charBox.top + 5 > obsBox.bottom ||
          charBox.bottom - 5 < obsBox.top ||
          charBox.right - 5 < obsBox.left ||
          charBox.left + 5 > obsBox.right
        );


        if (isColliding) {
          alert("💥 Oyun Bitti!\nToplam Skor: " + score);
          location.reload();
          clearInterval(move);
        }
      }
    }, 20);
  }

  spawnObstacle();
}

// 🔘 Space tuşu kontrolü
document.addEventListener("keydown", (e) => {
  if (e.key === " ") {
    if (!gameStarted) startGame();
    jump();
  }
});
