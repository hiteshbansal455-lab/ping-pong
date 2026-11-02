"""Player paddle controlled by the keyboard."""

import turtle

import settings


class Paddle(turtle.Turtle):
    """A vertically moving paddle on one side of the screen."""

    def __init__(self, x_position):
        super().__init__()
        self.shape("square")
        self.color(settings.PADDLE_COLOR)
        self.shapesize(
            stretch_wid=settings.PADDLE_HEIGHT / 20,
            stretch_len=settings.PADDLE_WIDTH / 20,
        )
        self.penup()
        self.goto(x_position, 0)

    def move(self, direction):
        """Move continuously in the requested direction, within the court."""
        top_limit = settings.COURT_TOP - settings.PADDLE_HEIGHT / 2
        bottom_limit = settings.COURT_BOTTOM + settings.PADDLE_HEIGHT / 2
        next_y = self.ycor() + direction * settings.PADDLE_SPEED
        self.sety(max(bottom_limit, min(next_y, top_limit)))
