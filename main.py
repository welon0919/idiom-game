import tkinter as tk
import random

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 800
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
        self.root = root
        self.root.title("貪吃蛇遊戲")
        self.idiom_display = tk.Label(font=("Arial",70))
        self.idiom_display.pack()
        self.canvas = tk.Canvas(root, width=self.GAME_WIDTH, height=self.GAME_HEIGHT, bg="white")
        self.canvas.pack()

        # 初始化遊戲變數
        self.snake = [(240, 240), (230, 240), (220, 240)]  # 初始蛇身
        
        self.food_options = ["快", "智", "勇", "和", "友", "希"]  # 隨機中文文字
        self.direction = "Right"
        self.running = True
        self.score = 0

        self.food = None
        self.food_text = None
        self.foods = []
        self.food_texts = []
        self.idiom = "畫龍點睛" # *This is a test value
        # 畫蛇和食物
        self.draw_snake()
        self.spawn_idiom()

        # 綁定鍵盤事件
        self.root.bind("<Up>", lambda e: self.change_direction("Up"))
        self.root.bind("<Down>", lambda e: self.change_direction("Down"))
        self.root.bind("<Left>", lambda e: self.change_direction("Left"))
        self.root.bind("<Right>", lambda e: self.change_direction("Right"))
        self.canvas.configure(bg="black")
        # 開始遊戲
        self.run_game()

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x, y, x + self.SNAKE_SIZE, y + self.SNAKE_SIZE,
                fill=self.SNAKE_COLOR, tag="snake"
            )

    def spawn_food(self,character):
        # if self.food:
        #     self.canvas.delete(self.food_text)
        while True:
            x = random.randint(0, (self.GAME_WIDTH // self.SNAKE_SIZE) - 1) * self.SNAKE_SIZE
            y = random.randint(0, (self.GAME_HEIGHT // self.SNAKE_SIZE) - 1) * self.SNAKE_SIZE
            if ((x, y) not in self.snake) and ((x,y) not in self.foods):
                self.food = (x, y)
                self.foods.append((x,y))
                break
        food_text = self.canvas.create_text(
            x + self.SNAKE_SIZE // 2, y + self.SNAKE_SIZE // 2,
            text=character, fill=self.TEXT_COLOR,
            font=("Arial", self.FONT_SIZE), tag="food"
        )
        self.food_text = food_text
        self.food_texts.append(food_text)

    def change_direction(self, new_direction):
        # 防止蛇逆行
        opposite_directions = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left",
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def move_snake(self):
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
            return

        # 更新蛇身
        self.snake.insert(0, new_head)
        if new_head == self.foods[0]:

            self.score += 1
            self.foods.pop(0)
            self.canvas.delete(self.food_texts.pop(0))
            if len(self.food_texts) == 0:
                self.spawn_idiom()
        else:
            self.snake.pop()

    def run_game(self):
        if self.running:
            self.move_snake()
            self.draw_snake()
            self.root.after(100, self.run_game)
        else:
            self.game_over()

    def game_over(self):
        self.canvas.create_text(
            self.GAME_WIDTH // 2, self.GAME_HEIGHT // 2,
            text=f"Game Over!\nscore={self.score}", fill="white", font=("Arial", 20)
        )
    def spawn_idiom(self):
        for character in self.idiom:
            self.spawn_food(character)
        self.idiom_display.config(text=self.idiom)

# 啟動遊戲
if __name__ == "__main__":
    root = tk.Tk()
    
    game = SnakeGame(root)
    root.mainloop()
