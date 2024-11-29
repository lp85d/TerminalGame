import curses
import random

players = ["Ivan", "Petr", "Oleg"]
positions = {"Ivan": (1, 1), "Petr": (3, 1), "Oleg": (5, 1)}
roles = {player: "Crewmate" for player in players}
tasks_completed = 0
sabotaged_players = set()
current_player_index = 0
tasks_total = 5

def assign_roles():
    imposter = random.choice(players)
    roles[imposter] = "Imposter"

def generate_large_map():
    return [[" " if random.random() >= 0.2 else "#" for _ in range(40)] for _ in range(40)]

def draw_map(screen):
    screen.clear()
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            screen.addstr(y, x * 2, cell)
    for player, (y, x) in positions.items():
        color = 3 if player in sabotaged_players else 1
        screen.attron(curses.color_pair(color))
        screen.addstr(y, x * 2, player[0])
        screen.attroff(curses.color_pair(color))

    # Отображение кнопок управления
    screen.attron(curses.color_pair(1))
    screen.addstr(41, 0, "[W] - Вверх  [A] - Влево  [S] - Вниз  [D] - Вправо")
    screen.attroff(curses.color_pair(1))

    screen.attron(curses.color_pair(2))
    screen.addstr(42, 0, "[T] - Выполнить задачу  [M] - Созвать собрание")
    screen.attroff(curses.color_pair(2))

    screen.attron(curses.color_pair(4))
    screen.addstr(43, 0, "[Space] - Передать ход  [Ctrl+C] - Выход")
    screen.attroff(curses.color_pair(4))

    screen.addstr(44, 0, f"Ход игрока: {players[current_player_index]} ({roles[players[current_player_index]]})")
    screen.addstr(45, 0, f"Задачи выполнены: {tasks_completed}/{tasks_total}")
    screen.refresh()

def move_player(player, direction):
    y, x = positions[player]
    moves = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
    dy, dx = moves.get(direction, (0, 0))
    ny, nx = y + dy, x + dx
    if 0 <= ny < len(game_map) and 0 <= nx < len(game_map[0]) and game_map[ny][nx] == " ":
        positions[player] = (ny, nx)

def perform_task(screen, player):
    global tasks_completed
    if roles[player] == "Crewmate":
        tasks_completed += 1
        if tasks_completed >= tasks_total:
            screen.addstr(46, 0, "Победа команды!")
            screen.refresh()
            curses.napms(3000)
            exit()

def call_meeting(screen):
    screen.clear()
    screen.addstr(20, 10, "Собрание! Кто предатель?", curses.color_pair(2))
    screen.refresh()
    curses.napms(3000)  # Простая имитация собрания
    exit()

def sabotage(player):
    global sabotaged_players
    y, x = positions[player]
    for other, (oy, ox) in positions.items():
        if other != player and (oy, ox) == (y, x):
            sabotaged_players.add(other)

def handle_mouse_click(mouse_event):
    _, mx, my, _, _ = mouse_event
    if my == 41:  # Первая строка кнопок
        if 0 <= mx < 10:  # W
            return 'w'
        elif 12 <= mx < 22:  # A
            return 'a'
        elif 24 <= mx < 34:  # S
            return 's'
        elif 36 <= mx < 46:  # D
            return 'd'
    elif my == 42:  # Вторая строка кнопок
        if 0 <= mx < 20:  # T
            return 't'
        elif 22 <= mx < 42:  # M
            return 'm'
    elif my == 43:  # Третья строка кнопок
        if 0 <= mx < 20:  # Space
            return 'space'
    return None

def main(screen):
    global current_player_index, game_map
    curses.curs_set(0)
    screen.timeout(100)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    game_map = generate_large_map()
    assign_roles()
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    draw_map(screen)

    while True:
        player = players[current_player_index]
        draw_map(screen)

        try:
            key = screen.getch()
        except KeyboardInterrupt:
            break

        if key == curses.KEY_MOUSE:
            try:
                mouse_event = curses.getmouse()
                action = handle_mouse_click(mouse_event)
                if action in 'wasd':
                    move_player(player, action)
                elif action == 't':
                    if roles[player] == "Imposter":
                        sabotage(player)
                    else:
                        perform_task(screen, player)
                elif action == 'm':
                    call_meeting(screen)
                elif action == 'space':
                    current_player_index = (current_player_index + 1) % len(players)
            except curses.error:
                pass
        elif key in map(ord, 'wasd'):
            move_player(player, chr(key))
        elif key == ord('t'):
            if roles[player] == "Imposter":
                sabotage(player)
            else:
                perform_task(screen, player)
        elif key == ord('m'):
            call_meeting(screen)
        elif key == 32:
            current_player_index = (current_player_index + 1) % len(players)
        elif key == 3:
            break

curses.wrapper(main)
