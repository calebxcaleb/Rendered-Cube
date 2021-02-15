from typing import Tuple, List
import pygame as pygame
from math import sin, cos, tan, pi, inf


class Cube:
    """Class for a cube (self explanatory)
    """
    origin: Tuple[float, float, float]
    points: List[Tuple[float, float, float]]
    segments: list
    rects: list
    colour: Tuple[int, int, int]
    length: int

    def __init__(self, origin: Tuple[float, float, float]) -> None:
        """Initialize a new cube"""
        self.origin = origin
        self.points = [
            (1.0, 1.0, 1.0),
            (1.0, 1.0, -1.0),
            (-1.0, 1.0, -1.0),
            (-1.0, 1.0, 1.0),
            (1.0, -1.0, 1.0),
            (1.0, -1.0, -1.0),
            (-1.0, -1.0, -1.0),
            (-1.0, -1.0, 1.0),
        ]
        self.segments = [
            [self.points[0], self.points[1]],
            [self.points[1], self.points[2]],
            [self.points[2], self.points[3]],
            [self.points[3], self.points[0]],
            [self.points[4], self.points[5]],
            [self.points[5], self.points[6]],
            [self.points[6], self.points[7]],
            [self.points[7], self.points[4]],
            [self.points[0], self.points[4]],
            [self.points[1], self.points[5]],
            [self.points[2], self.points[6]],
            [self.points[3], self.points[7]]
        ]
        self.rects = [
            (self.points[0], self.points[1], self.points[2], self.points[3]),
            (self.points[0], self.points[1], self.points[5], self.points[4]),
            (self.points[0], self.points[4], self.points[7], self.points[3]),
            (self.points[2], self.points[3], self.points[7], self.points[6]),
            (self.points[5], self.points[4], self.points[7], self.points[6]),
            (self.points[1], self.points[2], self.points[6], self.points[5]),
        ]
        self.colour = (0, 0, 0)
        self.length = 40
        self.multiply_points()

    def multiply_points(self) -> None:
        """Multiply the points to the initial length
        """
        for i in range(0, len(self.points)):
            x = self.points[i][0]
            y = self.points[i][1]
            z = self.points[i][2]

            self.points[i] = (
                x * self.length,
                y * self.length,
                z * self.length
            )

    def draw_rects(self, screen: pygame.Surface) -> None:
        """Draw the line segments for the cube
        """
        index = 0
        average_list = []
        average_dict = {}

        for rect in self.rects:
            average_list.append((rect[0][2] + rect[1][2] + rect[2][2] + rect[3][2]) / 4)
            average_dict[average_list[index]] = rect
            index += 1

        average_list.sort(reverse=True)

        for i in range(0, len(average_list)):
            rect = average_dict[average_list[i]]
            col = int((rect[0][2] + rect[1][2] + rect[2][2] + rect[3][2]) / 4 + 80)
            col = max(col, 0)
            col = min(col, 255)
            col = 255 - col
            colour = (col, col, col)
            rectangle = ((self.to_world(rect[0])), self.to_world(rect[1]),
                         self.to_world(rect[2]), self.to_world(rect[3]))
            pygame.draw.polygon(screen, colour, rectangle, 0)

    def draw_segments(self, screen: pygame.Surface) -> None:
        """Draw the line segments for the cube
        """
        for segment in self.segments:
            col = int(min(segment[0][2], segment[1][2]) + 80)
            col = max(col, 0)
            col = min(col, 255)
            col = 255 - col
            colour = (col, col, col)
            pygame.draw.line(screen, colour, self.to_world(segment[0]), self.to_world(segment[1]), 3)

    def draw_points(self, screen: pygame.Surface) -> None:
        """Draw the points for the cube
        """
        for point in self.points:
            col = int(point[2] + 80)
            col = max(col, 0)
            col = min(col, 255)
            col = 255 - col
            colour = (col, col, col)
            pygame.draw.circle(screen, colour, self.to_world(point), 5)

    def update_segments(self) -> None:
        """Update segments to match the points
        """
        self.segments = [
            [self.points[0], self.points[1]],
            [self.points[1], self.points[2]],
            [self.points[2], self.points[3]],
            [self.points[3], self.points[0]],
            [self.points[4], self.points[5]],
            [self.points[5], self.points[6]],
            [self.points[6], self.points[7]],
            [self.points[7], self.points[4]],
            [self.points[0], self.points[4]],
            [self.points[1], self.points[5]],
            [self.points[2], self.points[6]],
            [self.points[3], self.points[7]]
        ]

    def update_rects(self) -> None:
        """Update segments to match the points
        """
        self.rects = [
            (self.points[0], self.points[1], self.points[2], self.points[3]),
            (self.points[0], self.points[1], self.points[5], self.points[4]),
            (self.points[0], self.points[4], self.points[7], self.points[3]),
            (self.points[2], self.points[3], self.points[7], self.points[6]),
            (self.points[5], self.points[4], self.points[7], self.points[6]),
            (self.points[1], self.points[2], self.points[6], self.points[5]),
        ]

    def to_world(self, point: Tuple[float, float, float]) -> Tuple[float, float]:
        """Return 2d point given a 3d point
        """
        mult = -(point[2] - 160) / 80
        new_point = (point[0] * mult + self.origin[0], point[1] * mult + self.origin[1])
        return new_point

    def rotate_around_x(self, theta: float):
        """Rotate the cube about the z-axis"""
        for i in range(0, len(self.points)):
            x = self.points[i][0]
            y = self.points[i][1]
            z = self.points[i][2]

            self.points[i] = (
                x,
                y * cos(theta) - z * sin(theta),
                y * sin(theta) + z * cos(theta)
            )

        self.update_segments()
        self.update_rects()

    def rotate_around_y(self, theta: float):
        """Rotate the cube about the z-axis"""
        for i in range(0, len(self.points)):
            x = self.points[i][0]
            y = self.points[i][1]
            z = self.points[i][2]

            self.points[i] = (
                x * cos(theta) + z * sin(theta),
                y,
                -x * sin(theta) + z * cos(theta)
            )

        self.update_segments()
        self.update_rects()

    def rotate_around_z(self, theta: float):
        """Rotate the cube about the z-axis"""
        for i in range(0, len(self.points)):
            x = self.points[i][0]
            y = self.points[i][1]
            z = self.points[i][2]

            self.points[i] = (
                x * cos(theta) - y * sin(theta),
                x * sin(theta) + y * cos(theta),
                z
            )

        self.update_segments()
        self.update_rects()


def initialize_screen(screen_size: tuple[int, int]) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill((0, 0, 0))
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT])

    return screen


def run_sim() -> None:
    """Run simulation of 3d cube
    """
    run = True
    screen_width = 800
    screen_height = 800
    screen = initialize_screen((screen_width, screen_height))
    cube = Cube((screen_width / 2, screen_height / 2, 0))

    theta = pi / 6000

    while run:
        screen.fill((255, 255, 255))

        # cube.draw_points(screen)
        # cube.draw_segments(screen)
        cube.draw_rects(screen)

        cube.rotate_around_x(theta)
        cube.rotate_around_y(theta)
        cube.rotate_around_z(theta)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.display.quit()


if __name__ == "__main__":
    run_sim()
