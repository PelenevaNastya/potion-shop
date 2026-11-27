import pygame

class Button:
    """Универсальный класс для интерактивных кнопок."""
    def __init__(self, x, y, width, height, text, color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont("arial", 20, bold=True)

    def draw(self, screen):
        # Эффект подсветки при наведении курсора мыши
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            draw_color = tuple(min(255, c + 35) for c in self.base_color)
        else:
            draw_color = self.base_color

        # Отрисовка самой кнопки и ее рамки
        pygame.draw.rect(screen, draw_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)

        # Отрисовка текста по центру кнопки
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Возвращает True, если по кнопке нажали левой кнопкой мыши."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class GameUI:
    """Главный класс интерфейса игры 'Лавка зелий'."""
    def __init__(self, screen_width=800, screen_height=600):
        self.width = screen_width
        self.height = screen_height
        self.font_large = pygame.font.SysFont("arial", 28, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 20)

        # Кнопки трех базовых ингредиентов (снизу слева)
        self.btn_red = Button(50, 480, 110, 60, "Красный", (200, 45, 45))
        self.btn_blue = Button(180, 480, 110, 60, "Синий", (45, 90, 200))
        self.btn_yellow = Button(310, 480, 110, 60, "Желтый", (210, 180, 30), (20, 20, 20))

        # Кнопки действий с котлом (снизу справа)
        self.btn_stir = Button(480, 480, 130, 60, "Остудить", (70, 160, 180))
        self.btn_serve = Button(630, 480, 130, 60, "Отдать", (50, 170, 70))
        self.btn_clear = Button(630, 410, 130, 50, "Вылить", (110, 110, 110))

        # Список всех кнопок для удобной отрисовки в цикле
        self.buttons = [
            self.btn_red, self.btn_blue, self.btn_yellow,
            self.btn_stir, self.btn_serve, self.btn_clear
        ]
        # Загрузка графики из папки assets
        self.bg_shop = pygame.transform.scale(
            pygame.image.load("assets/shop.png").convert(), (screen_width, screen_height)
        )
        self.img_cauldron = pygame.transform.scale(
            pygame.image.load("assets/cauldron.png").convert_alpha(), (220, 200)
        )

        # Колбы для кнопок ингредиентов
        self.flasks = {
            "red": pygame.transform.scale(pygame.image.load("assets/flask_red.png").convert_alpha(), (40, 40)),
            "blue": pygame.transform.scale(pygame.image.load("assets/flask_blue.png").convert_alpha(), (40, 40)),
            "yellow": pygame.transform.scale(pygame.image.load("assets/flask_yellow.png").convert_alpha(), (40, 40)),
        }

        # Спрайты посетителей разных цветов
        self.visitors = [
            pygame.transform.scale(pygame.image.load("assets/visitor_blue.png").convert_alpha(), (140, 180)),
            pygame.transform.scale(pygame.image.load("assets/visitor_green.png").convert_alpha(), (140, 180)),
            pygame.transform.scale(pygame.image.load("assets/visitor_red.png").convert_alpha(), (140, 180)),
            pygame.transform.scale(pygame.image.load("assets/visitor_yellow.png").convert_alpha(), (140, 180)),
        ]

    def handle_click(self, event):
        """
        Проверяет нажатия на все кнопки и возвращает строковое название действия.
        Разработчик 1 будет использовать эти названия в main.py.
        """
        if self.btn_red.is_clicked(event):
            return "ADD_RED"
        if self.btn_blue.is_clicked(event):
            return "ADD_BLUE"
        if self.btn_yellow.is_clicked(event):
            return "ADD_YELLOW"
        if self.btn_stir.is_clicked(event):
            return "STIR"
        if self.btn_serve.is_clicked(event):
            return "SERVE"
        if self.btn_clear.is_clicked(event):
            return "CLEAR"
        return None

    def draw_heat_bar(self, screen, temperature, max_temp=100):
        """Отрисовка шкалы перегрева котла."""
        bar_x, bar_y = 50, 150
        bar_width, bar_height = 30, 250

        # Фон шкалы и рамка
        pygame.draw.rect(screen, (50, 50, 60), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Вычисление высоты заполнения
        fill_ratio = max(0, min(1, temperature / max_temp))
        fill_height = int(bar_height * fill_ratio)

        # Цвет шкалы меняется от зеленого к красному по мере нагрева
        if fill_ratio < 0.5:
            bar_color = (50, 200, 80)
        elif fill_ratio < 0.8:
            bar_color = (230, 180, 30)
        else:
            bar_color = (220, 40, 40)

        # Отрисовка заполнения снизу вверх
        fill_y = bar_y + (bar_height - fill_height)
        pygame.draw.rect(screen, bar_color, (bar_x + 2, fill_y, bar_width - 4, fill_height))

        # Подпись над шкалой
        label = self.font_medium.render("Жар", True, (255, 255, 255))
        screen.blit(label, (bar_x - 3, bar_y - 30))

    def draw_order_card(self, screen, order_name, target_color, time_left):
        """Отрисовка окна заказа посетителя (сверху по центру)."""
        card_rect = pygame.Rect(250, 20, 300, 90)
        pygame.draw.rect(screen, (45, 45, 65), card_rect, border_radius=12)
        pygame.draw.rect(screen, (200, 200, 220), card_rect, 2, border_radius=12)

        # Образец цвета нужного зелья (кружок в карточке)
        pygame.draw.circle(screen, target_color, (295, 65), 25)
        pygame.draw.circle(screen, (255, 255, 255), (295, 65), 25, 2)

        # Текст заказа и таймер ожидания
        title_surf = self.font_medium.render(f"Заказ: {order_name}", True, (255, 255, 255))
        timer_surf = self.font_medium.render(f"Осталось: {int(time_left)} сек", True, (255, 200, 100))

        screen.blit(title_surf, (335, 35))
        screen.blit(timer_surf, (335, 65))

    def draw_hud(self, screen, score, temperature, order_data=None):
        """Главная функция отрисовки всего интерфейса за один вызов."""
        # 1. Отрисовка всех кнопок и иконок колб
        for btn in self.buttons:
            btn.draw(screen)
        screen.blit(self.flasks["red"], (self.btn_red.rect.x + 5, self.btn_red.rect.y + 10))
        screen.blit(self.flasks["blue"], (self.btn_blue.rect.x + 5, self.btn_blue.rect.y + 10))
        screen.blit(self.flasks["yellow"], (self.btn_yellow.rect.x + 5, self.btn_yellow.rect.y + 10))

        # 2. Отрисовка счета (сверху слева)
        score_surf = self.font_large.render(f"Монеты: {score}", True, (255, 215, 0))
        screen.blit(score_surf, (30, 30))

        # 3. Отрисовка шкалы температуры
        self.draw_heat_bar(screen, temperature)

        # 4. Отрисовка карточки заказа (если посетитель пришел)
        if order_data:
            self.draw_order_card(
                screen,
                order_data["name"],
                order_data["color"],
                order_data["time_left"]
            )
