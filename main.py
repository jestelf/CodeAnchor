import pyglet
from pyglet.window import key, mouse

# Параметры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BG_COLOR = (30, 30, 30, 255)
TEXT_COLOR = (255, 255, 255, 255)
FONT_SIZE = 14

# Режимы
MODES = ["developer", "modding", "player", "debug"]
current_mode = "developer"

# Меню
menu_bar_height = 20
menu_items = ["Файл", "Настройки", "Справка"]
menu_content = ""
console_log = []

# Создание окна
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "CodeAnchor - Main Window", resizable=True)
window.set_minimum_size(400, 300)

# Шрифты и текст
font_name = "Arial"
def create_label(text, x, y, font_size=FONT_SIZE, color=TEXT_COLOR):
    return pyglet.text.Label(
        text,
        font_name=font_name,
        font_size=font_size,
        color=color,
        x=x,
        y=y,
        anchor_x="left",
        anchor_y="baseline",
    )

# Инициализация
menu_labels = []
content_label = create_label("", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
mode_label = create_label(f"Режим: {current_mode}", 10, WINDOW_HEIGHT - menu_bar_height - 10)

# Обработчики меню
def handle_file_menu():
    global menu_content
    if current_mode == "developer":
        menu_content = "Доступные проекты:\nПроект 1\nПроект 2"
    elif current_mode == "modding":
        menu_content = "Доступные модификации:\nМодификация 1\nМодификация 2"

def open_settings_window():
    print("Открыто окно настроек (заглушка)")
    settings_window = pyglet.window.Window(400, 300, "Настройки")

    @settings_window.event
    def on_draw():
        settings_window.clear()
        label = create_label("Настройки: будущие параметры", 10, 280, font_size=12)
        label.draw()


def open_help_window():
    print("Открыто окно справки")
    help_window = pyglet.window.Window(400, 300, "Справка")

    @help_window.event
    def on_draw():
        help_window.clear()
        label = create_label("jestelf - разработчик\nЦель: создать гибкий 2D-движок", 10, 280, font_size=12)
        label.draw()

menu_handlers = {
    "Файл": handle_file_menu,
    "Настройки": open_settings_window,
    "Справка": open_help_window,
}

@window.event
def on_draw():
    window.clear()
    # Отрисовка фона меню
    pyglet.graphics.draw(
        4,  # Количество вершин
        pyglet.gl.GL_QUADS,  # Тип примитива
        ('v2i', [
            0, WINDOW_HEIGHT - menu_bar_height,  # Верхний левый угол
            WINDOW_WIDTH, WINDOW_HEIGHT - menu_bar_height,  # Верхний правый угол
            WINDOW_WIDTH, WINDOW_HEIGHT,  # Нижний правый угол
            0, WINDOW_HEIGHT  # Нижний левый угол
        ]),  # Координаты вершин
        ('c4B', BG_COLOR * 4)  # Цвет для каждой вершины
    )

    # Отрисовка элементов меню
    x_offset = 10
    menu_labels.clear()
    for item in menu_items:
        label = create_label(item, x_offset, WINDOW_HEIGHT - 15)
        menu_labels.append((item, label, x_offset, x_offset + label.content_width))
        label.draw()
        x_offset += label.content_width + 20

    # Отрисовка текущего контента и режима
    content_label.text = menu_content
    content_label.x = WINDOW_WIDTH // 2 - content_label.content_width // 2
    content_label.draw()

    mode_label.text = f"Режим: {current_mode}"
    mode_label.draw()



@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        for item, label, x_start, x_end in menu_labels:
            if x_start <= x <= x_end and WINDOW_HEIGHT - menu_bar_height <= y <= WINDOW_HEIGHT:
                if item in menu_handlers:
                    menu_handlers[item]()

@window.event
def on_key_press(symbol, modifiers):
    global current_mode, menu_items
    if symbol == key.TAB:
        current_index = MODES.index(current_mode)
        current_mode = MODES[(current_index + 1) % len(MODES)]
        if current_mode == "player":
            menu_items.clear()
        else:
            menu_items[:] = ["Файл", "Настройки", "Справка"]

# Запуск
pyglet.app.run()
