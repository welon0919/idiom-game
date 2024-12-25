import tkinter as tk
import random
import json
import sys
import os
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 800


def get_path(filename):
    if hasattr(sys,'_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    file_path = os.path.join(base_path,filename)
    return file_path


def load_from_json(filepath):
    filepath = get_path(filepath)
    with open(filepath,'r',encoding='utf-8') as f:
        data = json.load(f)
    return data

IDIOMS_DICT = load_from_json("./idioms.json")

class SnakeGame:
    def __init__(self, root):

        # 遊戲設定
        self.SNAKE_SIZE = 30         # 貪吃蛇身體的大小
        self.GAME_WIDTH = 600        # 遊戲寬度
        self.GAME_HEIGHT = 600       # 遊戲高度
        self.SNAKE_COLOR = "#12e655"   # 貪吃蛇顏色
        self.TEXT_COLOR = "red"
        self.FONT_SIZE = 25
              # 食物文字顏色
        # 初始化主視窗
        self.root: tk.Tk = root
        self.root.title("貪吃蛇遊戲")
        self.score_display = tk.Label(font=("Arial",20),height=1)
        self.idiom_meaning_display = tk.Label(font=("微軟正黑體",25),height=2)
        self.idiom_meaning_display.pack(fill=tk.X)
        self.score_display.pack(fill=tk.X)
        self.canvas = tk.Canvas(root, width=self.GAME_WIDTH, height=self.GAME_HEIGHT, bg="white")
        self.canvas.pack()

        # 初始化遊戲變數
        self.interval_id = None
        # 綁定鍵盤事件
        self.root.bind("<Up>", lambda e: self.change_direction("Up"))
        self.root.bind("<Down>", lambda e: self.change_direction("Down"))
        self.root.bind("<Left>", lambda e: self.change_direction("Left"))
        self.root.bind("<Right>", lambda e: self.change_direction("Right"))
        self.root.bind("<Escape>",self.pause_game)
        self.canvas.configure(bg="black")
        self.reset_game()

        # 開始遊戲
        self.canvas.create_text(self.GAME_WIDTH/2,self.GAME_WIDTH/2,text="Press Space To Start",font=('Arial',40),anchor="center",tags="start_text",fill="white")
        self.root.bind("<space>",lambda e: self.start())
        self.game_overed = False
    def reset_game(self):
        """
        Reset the attribute of the snake when restarting
        """
        self.snake = [(240, 240), (210, 240), (180, 240)]  # 初始蛇身
        
        self.direction = "Right"
        self.direction_updated = True
        self.running = True
        self.score = 0
        self.started = False

        self.food = None
        self.food_text = None
        self.foods = []
        self.food_texts = []
        self.idiom = "" # *This is a test value
        self.idiom_meaning = ""
        # 畫蛇和食物
        self.draw_snake()
        self.spawn_idiom()

    def draw_snake(self):
        """
        Display the snake on the screen
        """
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x, y, x + self.SNAKE_SIZE, y + self.SNAKE_SIZE,
                fill=self.SNAKE_COLOR, tag=("snake",f"{x},{y}")
            )
    
    def spawn_food(self,character):
        """
        Generates food base on the character given
        """
        while True:
            x = random.randint(0, (self.GAME_WIDTH // self.SNAKE_SIZE) - 1) * self.SNAKE_SIZE
            y = random.randint(0, (self.GAME_HEIGHT // self.SNAKE_SIZE) - 1) * self.SNAKE_SIZE
            if ((x, y) not in self.snake) and ((x,y) not in self.foods):
                self.foods.append((x,y))
                break
        food_text = self.canvas.create_text(
            x + self.SNAKE_SIZE // 2, y + self.SNAKE_SIZE // 2,
            text=character, fill=self.TEXT_COLOR,
            font=("微軟正黑體", self.FONT_SIZE), tag="food"
        )
        self.food_texts.append(food_text)

    def change_direction(self, new_direction):
        """
        Change the direction of the snake
        """
        # 防止蛇逆行
        opposite_directions = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left",
        }
        if new_direction != opposite_directions.get(self.direction) and self.direction_updated:
            self.direction_updated = False
            self.direction = new_direction

    def move_snake(self):
        """
        Move the snake, detect food eating, detect game over
        """
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= self.SNAKE_SIZE
        elif self.direction == "Down":
            head_y += self.SNAKE_SIZE
        elif self.direction == "Left":
            head_x -= self.SNAKE_SIZE
        elif self.direction == "Right":
            head_x += self.SNAKE_SIZE
        new_head = (head_x, head_y)

        # 檢查撞牆或撞自己
        if (
            head_x < 0
            or head_x >= self.GAME_WIDTH
            or head_y < 0
            or head_y >= self.GAME_HEIGHT
            or new_head in self.snake
        ):
            self.running = False
            self.game_over()
            return

        # 更新蛇身
        self.snake.insert(0, new_head)
        if new_head == self.foods[0]:

            self.foods.pop(0)
            self.canvas.delete(self.food_texts.pop(0))
            if len(self.food_texts) == 0:
                
                self.spawn_idiom()
                self.score += 1
        else:
            self.snake.pop()
     

    def run_game(self):
        """
        Run the game main logic
        """
        if self.running:
            self.direction_updated = True
            self.move_snake()
            self.draw_snake()
            self.score_display.config(text=f"Score : {self.score}")
            self.interval_id = self.root.after(100, self.run_game)
        else:
            pass

    def game_over(self):
        """
        Call the killsnake when game is over
        """
        self.idiom_meaning_display.config(text="")
        self.canvas.delete("food")
        self.kill_snake(-1)
        
    def spawn_idiom(self):
        """
        Generate foods with the idiom character and place the meaning
        """
        self.idiom, self.idiom_meaning = self.get_random_idiom()
        for character in self.idiom:
            self.spawn_food(character)
        # set the display
        self.idiom_meaning_display.config(text=self.idiom_meaning)
    def get_random_idiom(self):
        """
        Pick a random idiom from idioms.json
        """
        idiom, meaning = random.choice(list(IDIOMS_DICT.items()))
        return idiom,meaning
    def restart_game(self,event=None):
        """
        Restart the game when space is pressed
        """
        if self.game_overed:
            self.game_overed = False
            self.canvas.delete("game_over_text")
            self.canvas.delete("food")
            self.reset_game()
            self.run_game()
    def start(self):        
        """
        Starts the game when space is pressed
        """
        if not self.started:
            self.started = True
            self.canvas.delete("start_text")
            self.root.bind("<space>",self.restart_game)
            self.run_game()
    def show_game_over(self):
        """
        Display the game over text
        """
        self.canvas.create_text(
            self.GAME_WIDTH // 2, self.GAME_HEIGHT // 2,
            text=f"Game Over!", fill="white", font=("Arial", 60),tags="game_over_text"
        )
        self.canvas.create_text(
            self.GAME_WIDTH // 2, self.GAME_HEIGHT // 2+100,
            text=f"Press space to restart!", fill="white", font=("Arial", 20),tags="game_over_text"
        )
    def kill_snake(self,index):
        """
        Play the death animation
        """
        self.running = False
        
        if index < len(self.snake):
            
            body = self.snake[index]
            tag = f"{body[0]},{body[1]}"
            self.canvas.delete(tag)
            self.canvas.update()
            self.root.after(50,self.kill_snake,index+1)
        else:
            self.show_game_over()
            self.game_overed = True
            self.running = False
    def pause_game(self,event=None):
        if (not self.started) or self.game_overed:
            return

        if self.running == True:
            self.canvas.create_text(self.GAME_WIDTH /2, 100, text="Game Paused",fill="white",font=('Arial',30),tags="pause_text")
            self.running = False
            self.root.after_cancel(self.interval_id)
        else:
            self.running = True
            self.canvas.delete("pause_text")
            self.run_game()
# 啟動遊戲

def start_game(root):
    game = SnakeGame(root)
    root.mainloop()
    
if __name__ == "__main__":

    root = tk.Tk()
    root.geometry('+0+0')
    root.iconbitmap(get_path("snake.ico"))
    start_game(root )
    