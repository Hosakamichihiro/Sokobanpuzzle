import pyxel


# ウィンドウの初期化
pyxel.init(160, 120,title="SOKOBAN PUZZLE")








# タイルサイズ
TILE_SIZE = 10

# プレイヤーの初期位置
player_x = 1
player_y = 1



# マップデータの初期化 (簡易的な例として2次元リストを使用)
# 0: 床, 1: 壁, 2: 箱, 3: ゴール
# レベルデータの定義 (複数のレベルをリストで定義)
levels = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 3, 0, 3, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 2, 0, 0, 0, 1],
        [1, 0, 1, 2, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 3, 3, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 2, 0, 2, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 3, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 3, 0, 0, 1],
        [1, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 2, 2, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 3, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 3, 0, 1],
        [1, 0, 2, 0, 1, 0, 1, 1],
        [1, 0, 2, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]

]


# 現在のレベルインデックス
current_level = 0

# 現在のマップデータを取得
map_data = [row[:] for row in levels[current_level]]

# 履歴のスタック
history = []

def save_state():
    """ 現在の状態を履歴に保存 """
    history.append((player_x, player_y, [row[:] for row in map_data]))

def load_state():
    """ 履歴から直前の状態をロード """
    global player_x, player_y, map_data
    if history:
        player_x, player_y, map_data = history.pop()

def can_move(x, y):
    return map_data[y][x] == 0 or map_data[y][x] == 3 or map_data[y][x] == 4

def move_player(dx, dy):
    global player_x, player_y
    
    new_x = player_x + dx
    new_y = player_y + dy

    if can_move(new_x, new_y):
        save_state()
        player_x = new_x
        player_y = new_y
    elif map_data[new_y][new_x] == 2 or map_data[new_y][new_x] == 4:
        # 箱の位置
        box_new_x = new_x + dx
        box_new_y = new_y + dy

        if can_move(box_new_x, box_new_y):
            save_state()
            # 箱を移動
            if map_data[new_y][new_x] == 2:
                map_data[new_y][new_x] = 0
            elif map_data[new_y][new_x] == 4:
                map_data[new_y][new_x] = 3  # ゴールから外れる
                
            if map_data[box_new_y][box_new_x] == 3:
                map_data[box_new_y][box_new_x] = 4  # 新しい位置がゴールの場合、ゴール上の箱にする
            else:
                map_data[box_new_y][box_new_x] = 2  # 新しい位置に箱を移動
            player_x = new_x
            player_y = new_y

def check_win():
    """ 全てのゴールに箱が置かれているかをチェック """
    for row in map_data:
        for tile in row:
            if tile == 3:  # ゴールが空のまま
                return False
    return True

def next_level():
    """ 次のレベルに進む """
    global current_level, map_data, player_x, player_y, history
    if current_level < len(levels) - 1:
        current_level += 1
        map_data = [row[:] for row in levels[current_level]]
        player_x, player_y = 1, 1  # 初期位置に戻す
        history = []  # 履歴をクリア
        
def update():
    if pyxel.btnp(pyxel.KEY_UP):
        move_player(0, -1)
    elif pyxel.btnp(pyxel.KEY_DOWN):
        move_player(0, 1)
    elif pyxel.btnp(pyxel.KEY_LEFT):
        move_player(-1, 0)
    elif pyxel.btnp(pyxel.KEY_RIGHT):
        move_player(1, 0)
    elif pyxel.btnp(pyxel.KEY_BACKSPACE):
        load_state()

    if check_win():
        next_level()

    

def draw():
    pyxel.cls(7)

    # マップの描画
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == 1:
                pyxel.rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, 0)  # 壁
            elif tile == 2:
                pyxel.rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, 9)  # 箱
            elif tile == 3:
                pyxel.rect(x * TILE_SIZE ,y * TILE_SIZE, TILE_SIZE,TILE_SIZE, 10)  # ゴール
            elif tile == 4:
                pyxel.rect(x * TILE_SIZE ,y * TILE_SIZE, TILE_SIZE,TILE_SIZE, 6)  # ゴールした箱
    # プレイヤーの描画
    pyxel.rect(player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE, 11)
    #レベルの表示
    pyxel.text(100, 10, f"Level: {current_level + 1}", 0)  # レベル番号を表示（1から始まるようにする）
    #色の説明
    pyxel.rect(90, 20, 8, 8, 9) 
    pyxel.text(100, 20, ":Box", 0)
    pyxel.rect(90, 30, 8, 8, 10) 
    pyxel.text(100, 30, ":Goal", 0)
    pyxel.rect(90, 40, 8, 8, 6) 
    pyxel.text(100, 40, ":Goal Box", 0)
    pyxel.rect(90, 50, 8, 8, 0) 
    pyxel.text(100, 50, ":Wall", 0)
    pyxel.rect(90, 60, 8, 8, 11) 
    pyxel.text(100, 60, ":Player", 0)
# ゲームの実行
pyxel.run(update, draw)