import random
import time

# Основные переменные
players = []
roles = {}
tasks = {}
completed_tasks = set()
game_over = False
impostor = None

# Функции
def display_tasks(player):
    """Отображение задач для игрока."""
    if roles[player] == "Crewmate":
        print(f"\n{player}, ваши задачи:")
        for task in tasks[player]:
            status = "✓" if task in completed_tasks else "✗"
            print(f"  [{status}] {task}")
        print()
    else:
        print(f"{player}, вы - Предатель. Ваша задача: устранить остальных игроков!\n")

def perform_task(player):
    """Игрок выполняет задачу."""
    if roles[player] != "Crewmate":
        print("Предатель не может выполнять задачи!\n")
        return
    print(f"{player}, выбирайте задачу для выполнения:")
    for i, task in enumerate(tasks[player], start=1):
        status = "✓" if task in completed_tasks else "✗"
        print(f"  {i}. {task} [{status}]")
    choice = input("Введите номер задачи: ")
    if choice.isdigit() and 1 <= int(choice) <= len(tasks[player]):
        task = tasks[player][int(choice) - 1]
        if task in completed_tasks:
            print("Эта задача уже выполнена!\n")
        else:
            print(f"Вы выполняете задачу: {task}...\n")
            time.sleep(2)
            completed_tasks.add(task)
            print("Задача выполнена!\n")
    else:
        print("Некорректный выбор.\n")

def kill_player(player):
    """Предатель устраняет игрока."""
    global game_over
    print(f"Игроки: {', '.join(players)}")
    target = input(f"{player}, выберите игрока для устранения: ")
    if target in players and roles[target] == "Crewmate":
        players.remove(target)
        print(f"Предатель {player} устранил {target}!\n")
        if len(players) == 2:  # Предатель и один член экипажа
            print("Предатель победил!")
            game_over = True
    else:
        print("Некорректный выбор или невозможно устранить этого игрока.\n")

def call_meeting():
    """Созыв собрания для голосования."""
    global game_over
    print("Собрание началось!")
    print(f"Оставшиеся игроки: {', '.join(players)}")
    votes = {player: 0 for player in players}
    for voter in players:
        vote = input(f"{voter}, за кого голосуете? ")
        if vote in players:
            votes[vote] += 1
    # Определить исключённого игрока
    ejected = max(votes, key=votes.get)
    print(f"{ejected} был исключён!")
    players.remove(ejected)
    if ejected == impostor:
        print("Предатель был найден! Экипаж победил!")
        game_over = True
    elif len(players) == 2:  # Если остался только один член экипажа
        print("Предатель победил!")
        game_over = True

def check_tasks_completed():
    """Проверяет, завершены ли все задачи экипажа."""
    all_tasks = {task for player in players if roles[player] == "Crewmate" for task in tasks[player]}
    if all_tasks == completed_tasks:
        print("Все задачи выполнены! Экипаж победил!")
        return True
    return False

# Инициализация игры
def initialize_game():
    global impostor
    num_players = int(input("Введите количество игроков (3-10): "))
    while num_players < 3 or num_players > 10:
        print("Количество игроков должно быть от 3 до 10.")
        num_players = int(input("Введите количество игроков (3-10): "))
    for i in range(num_players):
        name = input(f"Введите имя игрока {i + 1}: ")
        players.append(name)
    impostor = random.choice(players)
    for player in players:
        if player == impostor:
            roles[player] = "Impostor"
        else:
            roles[player] = "Crewmate"
            tasks[player] = [f"Задача {j}" for j in range(1, 4)]

    print("\nРоли распределены! Игра начинается!\n")

# Игровой цикл
initialize_game()
while not game_over:
    for player in players.copy():
        if game_over:
            break
        print(f"Ход игрока: {player}")
        display_tasks(player)
        if roles[player] == "Crewmate":
            print("1. Выполнить задачу\n2. Созвать собрание\n3. Пропустить ход")
            action = input("Выберите действие: ")
            if action == "1":
                perform_task(player)
            elif action == "2":
                call_meeting()
        elif roles[player] == "Impostor":
            print("1. Устранить игрока\n2. Созвать собрание\n3. Пропустить ход")
            action = input("Выберите действие: ")
            if action == "1":
                kill_player(player)
            elif action == "2":
                call_meeting()
        else:
            print("Пропуск хода.\n")
        if check_tasks_completed():
            game_over = True
        time.sleep(1)

print("Игра окончена!")
