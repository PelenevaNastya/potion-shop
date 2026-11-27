import random
import pygame
import sys
import settings
from cauldron import Cauldron
from customer import Customer
from ui import GameUI

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption(settings.TITLE)
clock = pygame.time.Clock()

cauldron = Cauldron()
customer = Customer(settings.RECIPES, settings.CUSTOMER_WAIT_TIME)
ui = GameUI(settings.WIDTH, settings.HEIGHT)
score = 0
current_visitor = random.choice(ui.visitors)
game_over = False  # Флаг окончания игры при перегреве
font_over_large = pygame.font.SysFont("arial", 32, bold=True)
font_over_medium = pygame.font.SysFont("arial", 24, bold=True)
font_over_small = pygame.font.SysFont("arial", 18)
running = True
while running:
    dt = clock.tick(settings.FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Если игра окончена — ждём нажатия Пробела или клика для рестарта
        if game_over:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                score = 0
                cauldron.clear()
                customer.generate_new_order()
                current_visitor = random.choice(ui.visitors)
                game_over = False
            continue

        # Обычное управление во время игры
        action = ui.handle_click(event)
        if action == "ADD_RED" and len(cauldron.ingredients) < 3:
            cauldron.add_ingredient("red")
        elif action == "ADD_BLUE" and len(cauldron.ingredients) < 3:
            cauldron.add_ingredient("blue")
        elif action == "ADD_YELLOW" and len(cauldron.ingredients) < 3:
            cauldron.add_ingredient("yellow")
        elif action == "STIR":
            cauldron.cool()
        elif action == "CLEAR":
            cauldron.clear()
        elif action == "SERVE":
            if customer.check_potion(cauldron.ingredients):
                score += 10
                customer.generate_new_order()
                current_visitor = random.choice(ui.visitors)
            cauldron.clear()

    # Обновляем таймеры, только пока игра не окончена
    if not game_over:
        cauldron.update(dt)
        if cauldron.temperature >= settings.MAX_TEMP:
            game_over = True  # Котёл взорвался — игра окончена!

        if customer.update(dt):
            customer.generate_new_order()  # Клиент не дождался
            current_visitor = random.choice(ui.visitors)
        
    # Отрисовка фона лавки
    screen.blit(ui.bg_shop, (0, 0))

    # 1. Посетитель за прилавком (сдвинули вправо на X=480, чтобы не прятался за котлом)
    if customer.is_active:
        screen.blit(current_visitor, (500, 195))

    # 2. Сначала рисуем сам котёл (сдвинули чуть левее на X=240)
    screen.blit(ui.img_cauldron, (240, 240))

    # 3. Перекрашиваем спрайт liquid.png в цвет текущего зелья и рисуем поверх котла
    colored_liquid = ui.img_liquid.copy()
    colored_liquid.fill(cauldron.color, special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(colored_liquid, (240, 240))

    # Готовим данные заказа для карточки клиента
    order_info = None
    if customer.is_active:
        order_info = {
            "name": customer.order_data["name"],
            "color": customer.order_data["color"],
            "time_left": customer.current_patience
        }

    ui.draw_hud(screen, score, cauldron.temperature, order_info)

    # Экран окончания игры при перегреве
    if game_over:
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title_txt = font_over_large.render("ПЕРЕГРЕВ! КОТЁЛ ВЗОРВАЛСЯ!", True, (255, 80, 80))
        score_txt = font_over_medium.render(f"Заработано монет: {score}", True, settings.WHITE)
        restart_txt = font_over_small.render("Нажмите ПРОБЕЛ или кликните мышью, чтобы начать заново", True, (220, 220, 220))

        screen.blit(title_txt, (settings.WIDTH // 2 - title_txt.get_width() // 2, 210))
        screen.blit(score_txt, (settings.WIDTH // 2 - score_txt.get_width() // 2, 270))
        screen.blit(restart_txt, (settings.WIDTH // 2 - restart_txt.get_width() // 2, 330))

    pygame.display.flip()

pygame.quit()
sys.exit()
