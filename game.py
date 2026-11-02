"""Game setup, input handling, and the animation loop."""

import turtle

import settings
from ball import Ball
from court import Court
from paddle import Paddle
from scoreboard import Scoreboard


class PingPongGame:
    """Coordinates the screen, players, ball, scoring, and game loop."""

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Ping-Pong")
        self.screen.bgcolor(settings.SCREEN_COLOR)
        self.screen.setup(width=settings.SCREEN_WIDTH, height=settings.SCREEN_HEIGHT)
        self.screen.tracer(0)

        self.court = Court()
        self.left_paddle = Paddle(-settings.PADDLE_X_OFFSET)
        self.right_paddle = Paddle(settings.PADDLE_X_OFFSET)
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.running = True
        self.paused = False
        self.keys_down = set()

        self._configure_controls()

    def _configure_controls(self):
        """Track held keys so paddles move smoothly instead of one step per press."""
        self.screen.listen()
        for key in ("w", "s", "Up", "Down"):
            self.screen.onkeypress(lambda key=key: self.keys_down.add(key), key)
            self.screen.onkeyrelease(lambda key=key: self.keys_down.discard(key), key)
        self.screen.onkeypress(self.toggle_pause, "space")
        self.screen.onkeypress(self.stop, "Escape")

    def _move_paddles(self):
        """Move each paddle once per frame while its key is held."""
        left_direction = int("w" in self.keys_down) - int("s" in self.keys_down)
        right_direction = int("Up" in self.keys_down) - int("Down" in self.keys_down)
        self.left_paddle.move(left_direction)
        self.right_paddle.move(right_direction)

    def _check_wall_collision(self):
        """Bounce the ball when it reaches the top or bottom edge."""
        top_limit = settings.COURT_TOP - settings.BALL_SIZE / 2
        bottom_limit = settings.COURT_BOTTOM + settings.BALL_SIZE / 2
        if self.ball.ycor() >= top_limit and self.ball.speed_y > 0:
            self.ball.sety(top_limit)
            self.ball.bounce_vertical()
        elif self.ball.ycor() <= bottom_limit and self.ball.speed_y < 0:
            self.ball.sety(bottom_limit)
            self.ball.bounce_vertical()

    def _check_paddle_collision(self, previous_x, previous_y):
        """Check whether the ball crossed a paddle face during this frame."""
        half_ball = settings.BALL_SIZE / 2
        half_paddle_height = settings.PADDLE_HEIGHT / 2
        half_paddle_width = settings.PADDLE_WIDTH / 2
        ball_x = self.ball.xcor()
        ball_y = self.ball.ycor()
        delta_x = ball_x - previous_x
        if delta_x == 0:
            return

        if (
            self.ball.speed_x < 0
            and previous_x > self.left_paddle.xcor() + half_paddle_width + half_ball
            and ball_x <= self.left_paddle.xcor() + half_paddle_width + half_ball
        ):
            contact_x = self.left_paddle.xcor() + half_paddle_width + half_ball
            contact_y = previous_y + (ball_y - previous_y) * (contact_x - previous_x) / delta_x
            if abs(contact_y - self.left_paddle.ycor()) <= half_paddle_height + half_ball:
                hit_offset = (contact_y - self.left_paddle.ycor()) / half_paddle_height
                self.ball.setx(contact_x)
                self.ball.bounce_paddle(hit_offset, direction=1)
        elif (
            self.ball.speed_x > 0
            and previous_x < self.right_paddle.xcor() - half_paddle_width - half_ball
            and ball_x >= self.right_paddle.xcor() - half_paddle_width - half_ball
        ):
            contact_x = self.right_paddle.xcor() - half_paddle_width - half_ball
            contact_y = previous_y + (ball_y - previous_y) * (contact_x - previous_x) / delta_x
            if abs(contact_y - self.right_paddle.ycor()) <= half_paddle_height + half_ball:
                hit_offset = (contact_y - self.right_paddle.ycor()) / half_paddle_height
                self.ball.setx(contact_x)
                self.ball.bounce_paddle(hit_offset, direction=-1)

    def _check_score(self):
        """Award a point and serve again when the ball passes a player."""
        if self.ball.xcor() > settings.COURT_RIGHT + settings.BALL_SIZE / 2:
            self.scoreboard.point_for_left()
            self.ball.reset(direction=-1)
        elif self.ball.xcor() < settings.COURT_LEFT - settings.BALL_SIZE / 2:
            self.scoreboard.point_for_right()
            self.ball.reset(direction=1)

    def _game_loop(self):
        """Update the screen and schedule the next animation frame."""
        if not self.running:
            return

        if not self.paused:
            self._move_paddles()
            previous_x = self.ball.xcor()
            previous_y = self.ball.ycor()
            self.ball.move()
            self._check_wall_collision()
            self._check_paddle_collision(previous_x, previous_y)
            self._check_score()
        self.screen.update()
        self.screen.ontimer(self._game_loop, settings.FRAME_DELAY_MS)

    def toggle_pause(self):
        """Pause or resume play when Space is pressed."""
        self.paused = not self.paused
        self.scoreboard.set_status("PAUSED  |  Press SPACE to resume" if self.paused else "")

    def stop(self):
        """Stop the animation loop and close the game window."""
        self.running = False
        self.screen.bye()

    def run(self):
        """Start the game and keep the window open."""
        self._game_loop()
        self.screen.mainloop()
