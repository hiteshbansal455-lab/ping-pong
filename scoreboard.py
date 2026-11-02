"""Score display for both players."""

import turtle

import settings


class Scoreboard(turtle.Turtle):
    """Tracks and displays the left and right player scores."""

    def __init__(self):
        super().__init__()
        self.color(settings.SCORE_COLOR)
        self.penup()
        self.hideturtle()
        self.left_score = 0
        self.right_score = 0
        self.status = turtle.Turtle()
        self.status.hideturtle()
        self.status.penup()
        self.status.color(settings.ACCENT_COLOR)
        self.update()

    def update(self):
        """Redraw the score and player labels at the top of the screen."""
        self.clear()
        self.goto(-150, settings.SCREEN_HEIGHT / 2 - 55)
        self.write(self.left_score, align="center", font=settings.FONT)
        self.goto(150, settings.SCREEN_HEIGHT / 2 - 55)
        self.write(self.right_score, align="center", font=settings.FONT)
        self.goto(-150, settings.SCREEN_HEIGHT / 2 - 83)
        self.write("PLAYER 1", align="center", font=("Arial", 10, "bold"))
        self.goto(150, settings.SCREEN_HEIGHT / 2 - 83)
        self.write("PLAYER 2", align="center", font=("Arial", 10, "bold"))

    def point_for_left(self):
        self.left_score += 1
        self.update()

    def point_for_right(self):
        self.right_score += 1
        self.update()

    def set_status(self, message):
        """Show a short pause message beneath the court."""
        self.status.clear()
        if message:
            self.status.goto(0, -settings.SCREEN_HEIGHT / 2 + 8)
            self.status.write(message, align="center", font=("Arial", 12, "bold"))
