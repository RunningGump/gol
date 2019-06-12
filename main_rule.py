import constants
import time

gameMap = []


def init_map(mode='random'):
    return [[0]*(constants.width+2) for _ in range(constants.height+2)]


def load_pattern(name, start_height=1, start_width=1):
    with open('pattern/' + name, 'r') as file:
        lines = [x.strip('\n') for x in file.readlines()]
    pattern_height = len(lines)
    pattern_width = len(lines[0])
    for i in range(pattern_height):
        for j in range(pattern_width):
            gameMap[start_height + i][start_width + j] = int(lines[i][j])


def get_next_step():
    new_map = init_map()
    for i in range(1, constants.height + 1):
        for j in range(1, constants.width + 1):
            live_cnt = 0
            for i_bias in range(-1, 2):
                for j_bias in range(-1, 2):
                    if i_bias == 0 and j_bias == 0:
                        continue
                    if gameMap[i + i_bias][j + j_bias] == 1:
                        live_cnt += 1
            if live_cnt == 2:
                new_map[i][j] = gameMap[i][j]
            elif live_cnt == 3:
                new_map[i][j] = 1
            else:
                new_map[i][j] = 0
    return new_map


def print_map():
    ans = []
    # print(gameMap)
    for line in gameMap:
        print(line)
    print('#' * 40)
    # for i in range(1, constants.height + 1):
    #     for j in range(1, constants.width + 1):
    #         ans.append(str(gameMap[i][j]))
    #         ans += ['\n' if j == constants.width else ' ']
    # print(ans)

if __name__ == "__main__":
    gameMap = init_map()
    load_pattern('oscillators.txt', 6, 6)
    while True:
        time.sleep(constants.sleep_time)
        print_map()
        gameMap = get_next_step()
