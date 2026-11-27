import settings

class Cauldron:
    def __init__(self):
        # Список добавленных ингредиентов
        self.ingredients = []

        # Начальная температура котла
        self.temperature = settings.START_TEMP

        # Начальный цвет жидкости
        self.color = settings.GRAY

        # Название приготовленного зелья
        self.potion_name = None

        # Счётчик времени для нагревания
        self.elapsed_time = 0

    def add_ingredient(self, ingredient):
        # Добавляем ингредиент в список
        self.ingredients.append(ingredient)

        # Если добавлен только один ингредиент
        if len(self.ingredients) == 1:
            self.color = getattr(
                settings, ingredient.upper(), settings.GRAY
            )
            return

        # Ищем рецепт по двум ингредиентам
        recipe_key = tuple(sorted(self.ingredients))
        recipe = settings.RECIPES.get(recipe_key)

        if recipe:
            self.potion_name = recipe["name"]
            self.color = recipe["color"]
        else:
            self.potion_name = None
            self.color = settings.BROWN

    def update(self, dt=1):
        self.elapsed_time += dt

        while self.elapsed_time >= 1:
            self.temperature = min(
                self.temperature + settings.TEMP_STEP,
                settings.MAX_TEMP
            )
            self.elapsed_time -= 1
    def cool(self, amount=20):
        """Остужает котёл при нажатии на кнопку."""
        self.temperature = max(settings.START_TEMP, self.temperature - amount)

    def clear(self):
        """Очищает котёл после выдачи или выброса зелья."""
        self.ingredients = []
        self.potion_name = None
        self.color = settings.GRAY
        self.temperature = settings.START_TEMP
        self.elapsed_time = 0
