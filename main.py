import pygame
import random
from math import sqrt, pow

# Инициализирует pygame
pygame.init()

# Создает новый экран
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Title and logo
pygame.display.set_caption("Space aggressors")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Background
bgcolor = (50, 50, 50)
bgpicture = pygame.image.load("clouds-space-purple.jpg")

# Player
playerImage = pygame.image.load("player.png")
playerX = width / 2 - 30  # 370
playerY = height / 3 * 2 + 80  # 480
playerX_d = 0  # Скорость движение по горизонтали

# Enemy
# Делаем несколько врагов и помещаем их данные в отдельные массивы
num_of_enemy = 6
enemyImage = []
enemyX = []
enemyY = []
enemyX_d = []
enemyY_d = []

for i in range(num_of_enemy):
    enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(1, 740))  # Спаунится в рандомном месте по горизонтали
    enemyY.append(10)  # 480
    enemyX_d.append(random.choice([-0.2, 0.2]))
    enemyY_d.append(0.1)

# Bullet
# Ready - пулю не видно; Fire - пуля на экране
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_d = 0
bulletY_d = 0.7
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 24)

################
###-Functions-##
################

# FPS
clock = pygame.time.Clock()


def player():
    screen.blit(playerImage, (playerX, playerY))


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    # global bulletImage
    bullet_state = 'fire'
    screen.blit(bulletImage, (x + 16, y))


# Функция проверки коллизии пули и врага
def is_collision(enemyX, enemyY, bulletX, bulletY):
    # Формула расчета дистанции между точками
    distance = sqrt((pow(enemyX - bulletX, 2)) + (pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text

def score_render():
    score_text = font.render("Score: " + str(score), True, [255, 255, 255])
    return score_text


# Game Loop
running = True
fps_enable = False
while running:
    screen.fill(bgcolor)  # Устанавливаем цвет заливки экрана
    screen.blit(bgpicture, (0, 0))
    screen.blit(score_render(), (10, 10))
    if fps_enable:
        screen.blit(update_fps(), (750, 10))

    for event in pygame.event.get():  # Создаем цикл, перебирающий все происходящие эвенты
        # Если нажимается крестик на окне => игра закрывается
        if event.type == pygame.QUIT:
            running = False

        # Обработка нажатий клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_d = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_d = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                playerX_d = 0

    # Передвижение игрока
    playerX += playerX_d  # Реализация перемещения с помощью стрелок клавиатуры
    if playerX <= 0:  # Барьеры слева и справа
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Передвижение врага
    for i in range(num_of_enemy):
        enemyX[i] += enemyX_d[i]
        if enemyX[i] <= 0:  # Барьеры слева и справа
            enemyX_d[i] = 0.2
            enemyY[i] += 50
        elif enemyX[i] >= 738:
            enemyX_d[i] = -0.2
            enemyY[i] += 50

        # Коллизия пули и врага
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(1, 740)
            enemyY[i] = 10
            score += 1
        # Отображаем всех врагов
        enemy(enemyX[i], enemyY[i], i)

    # Исчезновение пули, когда она вверху
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Передвижение пули
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_d

    player()
    # clock.tick(60)
    pygame.display.update()  # Обновляем экран
print('Привет как дела'
      'иди нафиг азаза')