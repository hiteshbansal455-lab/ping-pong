"""Draw the static court markings behind the game."""

import turtle

import settings


class Court(turtle.Turtle):
    """A non-interactive turtle that draws the court and center line."""

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.speed("fastest")
        self.color(settings.COURT_COLOR)
        self.pensize(3)

        # Outline the playing area, leaving room above for the score.
        left = settings.COURT_LEFT
        right = settings.COURT_RIGHT
        top = settings.COURT_TOP
        bottom = settings.COURT_BOTTOM
        self.penup()
        self.goto(left, top)
        self.pendown()
        for x, y in ((right, top), (right, bottom), (left, bottom), (left, top)):
            self.goto(x, y)

        # Draw a dashed center line.
        self.penup()
        self.goto(0, bottom)
        self.setheading(90)
        while self.ycor() < top:
            self.pendown()
            self.forward(12)
            self.penup()
            self.forward(10)
