
.x + 65, card_rect.y + 53))

        # Полоска таймера терпения клиента
        bar_bg = pygame.Rect(card_rect.x + 15, card_rect.y + 92, 270, 10)
        pygame.draw.rect(screen, (25, 25, 35), bar_bg, border_radius=5)

        ratio = customer.get_patience_ratio()
        bar_color = (80, 220, 100) if ratio > 0.35 else (230, 70, 70)
        bar_fill = pygame.Rect(card_rect.x + 15, card_rect.y + 92, int(270 * ratio), 10)
        pygame.draw.rect(screen, bar_color, bar_fill, border_radius=5)

    def _draw_heat_bar(self, screen, temperature):
        """Отрисовка вертикальной шкалы перегрева котла слева."""
        label = self.font_small.render("НАГРЕВ", True, (255, 140, 100))
        screen.blit(label, (48, 175))

        bar_bg = pygame.Rect(60, 200, 30, 200)
        pygame.draw.rect(screen, (35, 35, 45), bar_bg, border_radius=8)

        # Заполнение снизу вверх (temperature от 0 до 100)
        clamped_temp = max(0, min(100, temperature))
        fill_height = int(200 * (clamped_temp / 100.0))
        fill_rect = pygame.Rect(60, 200 + (200 - fill_height), 30, fill_height)

        # Цвет меняется от зеленого к красному при перегреве
        if clamped_temp < 50:
            heat_color = (70, 210, 90)
        elif clamped_temp < 80:
            heat_color = (240, 180, 40)
        else:
            heat_color = (240, 50, 50)

        pygame.draw.rect(screen, heat_color, fill_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 200), bar_bg, width=2, border_radius=8)

    def _draw_buttons(self, screen):
        """Отрисовка кнопок ингредиентов и действий."""
        # 1. Кнопки трех ингредиентов
        labels = {"red": "Красный", "blue": "Синий", "yellow": "Желтый"}
        for key in ["red", "blue", "yellow"]:
            rect = self.buttons[key]
            pygame.draw.rect(screen, (50, 50, 65), rect, border_radius=12)
            pygame.draw.rect(screen, (150, 150, 170), rect, width=2, border_radius=12)

            # Иконка колбы
            icon = self.icons[key]
            screen.blit(icon, (rect.x + 25, rect.y + 8))

            # Подпись
            txt = self.font_small.render(labels[key], True, (240, 240, 240))
            screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.y + 68))

        # 2. Кнопка "Отдать зелье"
        serve_rect = self.buttons["serve"]
        pygame.draw.rect(screen, (45, 150, 85), serve_rect, border_radius=10)
        serve_txt = self.font_medium.render("Отдать зелье", True, (255, 255, 255))
        screen.blit(serve_txt, (serve_rect.centerx - serve_txt.get_width() // 2, serve_rect.centery - 12))

        # 3. Кнопка "Помешать (остудить)"
        cool_rect = self.buttons["cool"]
        pygame.draw.rect(screen, (55, 115, 185), cool_rect, border_radius=10)
        cool_txt = self.font_medium.render("Остудить", True, (255, 255, 255))
        screen.blit(cool_txt, (cool_rect.centerx - cool_txt.get_width() // 2, cool_rect.centery - 12))
