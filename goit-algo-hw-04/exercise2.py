import argparse
import turtle

def koch_segment(t: turtle.Turtle, order: int, size: float) -> None:
    if order == 0:
        t.forward(size)
    else:
        size /= 3.0
        koch_segment(t, order - 1, size)
        t.left(60)
        koch_segment(t, order - 1, size)
        t.right(120)
        koch_segment(t, order - 1, size)
        t.left(60)
        koch_segment(t, order - 1, size)

def draw_snowflake(order: int, size: float = 300) -> None:
    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха (order={order})")
    screen.bgcolor("white")

    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.penup()
    t.goto(-size/2, size/3)
    t.pendown()

    t.color("royalblue")
    t.pensize(2)

    for _ in range(3):
        koch_segment(t, order, size)
        t.right(120)

    t.hideturtle()
    turtle.done()

def main():
    ap = argparse.ArgumentParser(description="Візуалізація 'сніжинки Коха'.")
    ap.add_argument("--level", "-l", type=int, default=3, help="Рівень рекурсії (0..7 рекомендовано)")
    ap.add_argument("--size", "-s", type=float, default=300, help="Базовий розмір фігури")
    args = ap.parse_args()
    draw_snowflake(args.level, args.size)

if __name__ == "__main__":
    main()
