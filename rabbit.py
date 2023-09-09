import random
from collections import deque

class RabbitGame:
    def __init__(self, grid_size, num_carrots, num_holes):
        self.grid_size = grid_size
        self.num_carrots = num_carrots
        self.num_holes = num_holes
        self.grid = [['-' for _ in range(grid_size)] for _ in range(grid_size)]
        self.rabbit = None
        self.carrots = []
        self.holes = []
        self.carrot_held = False

    def generate_map(self):
        # Place the rabbit randomly
        self.rabbit = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
        self.grid[self.rabbit[0]][self.rabbit[1]] = 'r'

        # Place the carrots randomly
        for _ in range(self.num_carrots):
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            while self.grid[x][y] != '-':
                x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            self.grid[x][y] = 'c'
            self.carrots.append((x, y))

        # Place the rabbit holes randomly
        for _ in range(self.num_holes):
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            while self.grid[x][y] != '-':
                x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            self.grid[x][y] = 'O'
            self.holes.append((x, y))

    def print_map(self):
        for row in self.grid:
            print(" ".join(row))

    def move_rabbit(self, direction):
        if direction == 'w':
            new_x, new_y = self.rabbit[0] - 1, self.rabbit[1]
        elif direction == 's':
            new_x, new_y = self.rabbit[0] + 1, self.rabbit[1]
        elif direction == 'a':
            new_x, new_y = self.rabbit[0], self.rabbit[1] - 1
        elif direction == 'd':
            new_x, new_y = self.rabbit[0], self.rabbit[1] + 1
        else:
            return

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            if self.grid[new_x][new_y] == 'c':
                self.grid[self.rabbit[0]][self.rabbit[1]] = '-'
                self.rabbit = (new_x, new_y)
                self.grid[new_x][new_y] = 'R'
                self.carrots.remove((new_x, new_y))
                self.carrot_held = True
            elif self.grid[new_x][new_y] == 'O':
                if self.carrot_held:
                    self.grid[self.rabbit[0]][self.rabbit[1]] = '-'
                    self.rabbit = (new_x, new_y)
                    self.grid[new_x][new_y] = 'r'
                    self.carrot_held = False

    def find_shortest_path(self):
        start = self.rabbit
        goals = self.carrots + self.holes
        visited = set()
        queue = deque([(start, [])])

        while queue:
            current, path = queue.popleft()
            if current in goals:
                return path

            for direction in ['w', 's', 'a', 'd']:
                new_x, new_y = current[0], current[1]
                if direction == 'w':
                    new_x -= 1
                elif direction == 's':
                    new_x += 1
                elif direction == 'a':
                    new_y -= 1
                elif direction == 'd':
                    new_y += 1

                new_pos = (new_x, new_y)
                if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size and new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, path + [direction]))

    def emulate_solution(self, solution):
        for direction in solution:
            self.move_rabbit(direction)
            self.print_map()

    def play(self):
        self.generate_map()
        solution = self.find_shortest_path()
        if solution:
            print("Shortest path solution:")
            print("".join(solution))
            self.print_map()  # Print the initial map
            self.emulate_solution(solution)
            print("You won! All carrots are in rabbit holes.")
        else:
            print("No solution found!")

if __name__ == "__main__":
    while True:
        user_input = input("Press Enter to play the game or any other key to quit: ")
        if user_input:
            break

        grid_size = int(input("Enter the grid size: "))
        num_carrots = int(input("Enter the number of carrots: "))
        num_holes = int(input("Enter the number of rabbit holes: "))

        game = RabbitGame(grid_size, num_carrots, num_holes)
        game.play()
