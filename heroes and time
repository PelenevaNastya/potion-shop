import random
import pygame

class Customer:
    def __init__(self, recipes, patience_time=15.0):
        """
        recipes: словарь рецептов из settings.py, например:
        {
            "health": {"name": "Здоровье", "recipe": (2, 0, 0), "color": (220, 50, 50)},
            ...
        }
        """
        self.recipes = recipes
        self.max_patience = patience_time
        self.current_patience = patience_time
        self.order_key = None
        self.order_data = None
        self.is_active = False

        # Генерируем первый заказ при создании
        self.generate_new_order()

    def generate_new_order(self):
        """Выбирает случайное зелье из доступных рецептов."""
        self.order_key = random.choice(list(self.recipes.keys()))
        self.order_data = self.recipes[self.order_key]
        self.current_patience = self.max_patience
        self.is_active = True

    def update(self, dt):
        """
        Обновляет таймер терпения.
        dt: время в секундах, прошедшее с прошлого кадра (clock.tick(60) / 1000.0).
        Возвращает True, если время вышло и клиент ушел злым.
        """
        if not self.is_active:
            return False

        self.current_patience -= dt
        if self.current_patience <= 0:
            self.current_patience = 0
            self.is_active = False
            return True  # Заказ провален по времени

        return False

    def check_potion(self, cauldron_ingredients):
        """
        Проверяет, совпадает ли состав котла с заказом.
        cauldron_ingredients: кортеж или список вида (red, blue, yellow)
        """
        if not self.is_active:
            return False

        return tuple(cauldron_ingredients) == tuple(self.order_data["recipe"])

    def get_patience_ratio(self):
        """Возвращает остаток времени от 0.0 до 1.0 для отрисовки полоски."""
        return max(0.0, self.current_patience / self.max_patience)
