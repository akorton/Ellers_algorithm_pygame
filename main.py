import pygame
import random

# region CONSTANTS
NUMBER_OF_CELLS: int = 50
WIDTH: int = 800
HEIGHT: int = 800
OFFSET_WIDTH: int = 10
OFFSET_HEIGHT: int = 10
CELL_WIDTH: int = (WIDTH - 2 * OFFSET_WIDTH) // NUMBER_OF_CELLS
CELL_HEIGHT: int = (HEIGHT - 2 * OFFSET_HEIGHT) // NUMBER_OF_CELLS
FPS: int = 30
BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (0xFF, 0xFF, 0xFF)


# endregion

# region Main functions
def merge_sets(row: list[int], set_number1, set_number2) -> list[int]:
    for i in range(len(row)):
        if row[i] == set_number2:
            row[i] = set_number1
    return row


def generate_right_borders(row: list[int]) -> tuple[list[bool], list[int]]:
    borders: list[bool] = [False for _ in range(len(row))]

    for i in range(len(row) - 1):
        choice: bool = bool(random.randint(0, 1))
        if choice or row[i] == row[i + 1]:
            borders[i] = True
        else:
            row = merge_sets(row, row[i], row[i + 1])
    borders[-1] = True
    return borders, row


def number_of_elements_in_set(row: list[int], set_number: int) -> int:
    count: int = 0
    for i in row:
        if i == set_number:
            count += 1
    return count


def number_of_horizontal_borders_in_set(row: list[int], set_number: int, borders: list[bool]) -> int:
    count: int = 0
    for i in range(len(row)):
        if row[i] == set_number and borders[i]:
            count += 1
    return count


def generate_down_borders(row: list[int]) -> list[bool]:
    borders: list[bool] = [False for _ in range(len(row))]

    for i in range(len(row)):
        choice: bool = bool(random.randint(0, 1))
        if choice and number_of_elements_in_set(row, row[i]) - \
                number_of_horizontal_borders_in_set(row, row[i], borders) != 1:
            borders[i] = True
    return borders


def generate_labyrinth(number_of_cells: int) -> tuple[list[list[bool]], list[list[bool]]]:
    # initial setup
    next_set: int = 1
    matrix_right_borders = []
    matrix_down_borders = []

    # create first line with no cells added to any set
    sets: list[int] = [0 for _ in range(number_of_cells)]

    # main cycle for the algorithm
    for row in range(number_of_cells):
        # step 2: assign set to cells without it
        for col in range(number_of_cells):
            if sets[col] == 0:
                sets[col] = next_set
                next_set += 1
        # step 3: add right borders
        cur_right_borders, sets = generate_right_borders(sets)
        matrix_right_borders.append(cur_right_borders)
        # step 4: add down borders
        matrix_down_borders.append(generate_down_borders(sets))
        if row != number_of_cells - 1:  # not the last line
            for i in range(len(sets)):
                if matrix_down_borders[row][i]:
                    sets[i] = 0
        else:
            for i in range(number_of_cells):
                matrix_down_borders[row][i] = True
                if i != number_of_cells - 1 and sets[i] != sets[i + 1]:
                    matrix_right_borders[row][i] = False
                    sets = merge_sets(sets, sets[i], sets[i + 1])

    return matrix_right_borders, matrix_down_borders


def get_left_top_cell_coords(i, j):
    return OFFSET_WIDTH + j * CELL_WIDTH, OFFSET_HEIGHT + i * CELL_HEIGHT


def add_coords(coords1, coords2):
    return coords1[0] + coords2[0], coords1[1] + coords2[1]


def draw(matrix_right_borders: list[list[bool]], matrix_down_borders: [list[list[bool]]]) -> None:
    for i in range(NUMBER_OF_CELLS):
        for j in range(NUMBER_OF_CELLS):
            if matrix_right_borders[i][j]:
                pygame.draw.line(screen, WHITE, add_coords((CELL_WIDTH, 0), get_left_top_cell_coords(i, j)),
                                 add_coords((CELL_WIDTH, CELL_HEIGHT), get_left_top_cell_coords(i, j)))
            if matrix_down_borders[i][j]:
                pygame.draw.line(screen, WHITE, add_coords((0, CELL_HEIGHT), get_left_top_cell_coords(i, j)),
                                 add_coords((CELL_WIDTH, CELL_HEIGHT), get_left_top_cell_coords(i, j)))
            if j == 0:  # leftmost column => add left border
                pygame.draw.line(screen, WHITE, get_left_top_cell_coords(i, j),
                                 add_coords((0, CELL_HEIGHT), get_left_top_cell_coords(i, j)))
            if i == 0:  # topmost row => add top border
                pygame.draw.line(screen, WHITE, get_left_top_cell_coords(i, j),
                                 add_coords((CELL_WIDTH, 0), get_left_top_cell_coords(i, j)))


# endregion

# region setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eller's algorithm")
clock = pygame.time.Clock()
running: bool = True
screen.fill(BLACK)
pygame.display.flip()
labyrinth: tuple[list[list[bool]], list[list[bool]]] = generate_labyrinth(NUMBER_OF_CELLS)
draw(*labyrinth)
# endregion

# region Main cycle
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
# endregion
