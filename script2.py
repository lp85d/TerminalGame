import curses
import random

def generate_map(size=32):
    return [[" " if random.random() >= 0.1 else "#" for _ in range(size)] for _ in range(size)]

def place_player(game_map):
    while True:
        y = random.randint(0, len(game_map) - 1)
        x = random.randint(0, len(game_map[0]) - 1)
        if game_map[y][x] == " ":
            return y, x

def draw_map(screen, game_map, player_pos):
    screen.clear()
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            screen.addstr(y, x * 2, cell)

    py, px = player_pos
    screen.attron(curses.color_pair(3))
    screen.addstr(py, px * 2, "O")
    screen.attroff(curses.color_pair(3))

    screen.attron(curses.color_pair(2))
    screen.addstr(len(game_map) + 3, 0, "[q] Выйти из программы")
    screen.attroff(curses.color_pair(2))

    screen.refresh()

def handle_mouse_click(mouse_event, game_map):
    _, mx, my, _, _ = mouse_event
    if my == len(game_map) + 3 and 0 <= mx < 20:
        return "exit"
    return f"Mouse clicked at ({my}, {mx})"

def move_player(game_map, player_pos, direction):
    y, x = player_pos
    moves = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1), curses.KEY_UP: (-1, 0), curses.KEY_LEFT: (0, -1), curses.KEY_DOWN: (1, 0), curses.KEY_RIGHT: (0, 1)}
    if direction in moves:
        dy, dx = moves[direction]
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(game_map) and 0 <= nx < len(game_map[0]) and game_map[ny][nx] == " ":
            return ny, nx
    return player_pos

def main(screen):
    curses.curs_set(0)
    screen.timeout(100)
    curses.start_color()
    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    game_map = generate_map(32)
    player_pos = place_player(game_map)
    draw_map(screen, game_map, player_pos)

    while True:
        try:
            key = screen.getch()
            if key == curses.KEY_MOUSE:
                try:
                    mouse_event = curses.getmouse()
                    action = handle_mouse_click(mouse_event, game_map)
                    if action == "exit":
                        screen.addstr(len(game_map) + 4, 0, "Выход через 3 секунды... До свидания!")
                        screen.refresh()
                        curses.napms(3000)
                        break
                except curses.error:
                    pass
            elif key in map(ord, 'wasd') or key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                player_pos = move_player(game_map, player_pos, key if key not in map(ord, 'wasd') else chr(key))
                draw_map(screen, game_map, player_pos)
            elif key == ord('q'):
                screen.addstr(len(game_map) + 4, 0, "Выход через 3 секунды... До свидания!")
                screen.refresh()
                curses.napms(3000)
                break
        except KeyboardInterrupt:
            break

curses.wrapper(main)
