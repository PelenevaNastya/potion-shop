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

running = True
while running:
    dt = clock.tick(settings.FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Обновление таймеров
    cauldron.update(dt)
    if cauldron.temperature >= settings.MAX_TEMP:
        cauldron.clear()  # Котёл перегрелся

    if customer.update(dt):
        customer.generate_new_order()  # Клиент не дождался
        current_visitor = random.choice(ui.visitors)
        
    # Отрисовка фона лавки
    screen.blit(ui.bg_shop, (0, 0))

    # Отрисовка посетителя за прилавком (если он активен)
    if customer.is_active:
        screen.blit(current_visitor, (330, 115))

    # Рисуем жидкость нужного цвета и поверх неё сам котёл
    pygame.draw.ellipse(screen, cauldron.color, (320, 275, 160, 45))
    screen.blit(ui.img_cauldron, (290, 240))

    # Готовим данные заказа для карточки клиента
    order_info = None
    if customer.is_active:
        order_info = {
            "name": customer.order_data["name"],
            "color": customer.order_data["color"],
            "time_left": customer.current_patience
        }

    ui.draw_hud(screen, score, cauldron.temperature, order_info)
    pygame.display.flip()

pygame.quit()
sys.exit()
