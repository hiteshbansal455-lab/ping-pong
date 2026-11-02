"""The ball and its movement and collision behavior."""

import turtle

import settings


class Ball(turtle.Turtle):
    """A ball that bounces off the top, bottom, and paddles."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color(settings.BALL_COLOR)
        self.shapesize(settings.BALL_SIZE / 20)
        self.penup()
        self.speed_x = settings.BALL_SPEED
        self.speed_y = settings.BALL_SPEED

    def move(self):
        """Advance the ball by one frame."""
        self.setx(self.xcor() + self.speed_x)
        self.sety(self.ycor() + self.speed_y)

    def bounce_vertical(self):
        """Reverse vertical direction after hitting a horizontal wall."""
        self.speed_y *= -1

    def bounce_paddle(self, hit_offset, direction):
        """Bounce away from a paddle, changing angle based on the hit position."""
        self.speed_x = direction * min(
            abs(self.speed_x) + settings.BALL_SPEED_INCREASE,
            settings.BALL_MAX_SPEED,
        )
        # A hit near the paddle's edge sends the ball upward or downward.
        hit_offset = max(-1, min(hit_offset, 1))
        self.speed_y = max(
            -settings.BALL_MAX_SPEED,
            min(settings.BALL_MAX_SPEED, hit_offset * settings.BALL_MAX_SPEED),
        )
        if abs(self.speed_y) < 1:
            self.speed_y = 1 if hit_offset >= 0 else -1

    def reset(self, direction):
        """Return the ball to the center and serve toward the player who lost."""
        self.goto(0, 0)
        self.speed_x = settings.BALL_SPEED * direction
        self.speed_y = settings.BALL_SPEED
