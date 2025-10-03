# pythagoras_tree.py
# Фрактал "дерево Піфагора" (лінійна версія) з рекурсією.
# Користувач задає глибину, базову довжину та кут.
# Без зовнішніх бібліотек — використовуємо стандартний turtle.

import math
import turtle

# --- параметри від користувача ---
def ask_int(prompt, default):
    try:
        v = input(prompt + f" [{default}]: ").strip()
        return int(v) if v else default
    except Exception:
        return default

def ask_float(prompt, default):
    try:
        v = input(prompt + f" [{default}]: ").strip()
        return float(v) if v else default
    except Exception:
        return default

DEPTH = ask_int("Вкажіть рівень рекурсії (0..14)", 10)
BASE = ask_int("Довжина базової гілки (пікселі)", 120)
ANGLE = ask_float("Кут відхилення гілок у градусах", 45)

# --- налаштування полотна ---
turtle.colormode(255)
turtle.title("Фрактал: дерево Піфагора")
turtle.setup(width=1000, height=800)
turtle.bgcolor("white")

pen = turtle.Turtle(visible=False)
pen.speed(0)
pen.hideturtle()
pen.pensize(2)

# плавний перехід кольору від темного до світлого з глибиною
def color_for(depth, max_depth):
    # від коричневого до зеленого
    t = depth / max_depth if max_depth else 0
    r = int(120 * (1 - t) + 30)   # 150..30
    g = int(60  * (1 - t) + 140)  # 200..140
    b = int(40  * (1 - t) + 60)   # 100..60
    return (r, g, b)

# Рекурсивний малюнок дерева (лінійна версія — гілки як відрізки)
def draw_tree(length, depth):
    if depth == 0 or length < 2:
        # листок
        pen.pencolor(30, 170, 60)
        pen.forward(length)
        pen.backward(length)
        return

    pen.pencolor(color_for(depth, DEPTH))
    # Стовбур
    pen.forward(length)

    # ліва гілка
    pen.left(ANGLE)
    draw_tree(length * math.cos(math.radians(ANGLE)), depth - 1)
    pen.right(ANGLE)

    # права гілка
    pen.right(ANGLE)
    draw_tree(length * math.cos(math.radians(ANGLE)), depth - 1)
    pen.left(ANGLE)

    pen.backward(length)

# Початкове позиціювання — “знизу по центру”, ріст вгору
pen.up()
pen.setheading(90)           # вгору
pen.goto(0, -350)            # низ екрана
pen.down()

draw_tree(BASE, DEPTH)

turtle.done()

