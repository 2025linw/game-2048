from game2048 import Board

def main():
    game = Board()
    game.start()

    running = True
    while running:
        game.print()
        user_input = input("> ")

        match user_input:
            case "quit" | "q":
                running = False
            case "new" | "n":
                game.start()

            case "up" | 'u':
                game.move("up")
            case "down" | 'd':
                game.move("down")
            case "left" | 'l':
                game.move("left")
            case "right" | 'r':
                game.move("right")

            case _:
                print("Invalid Input")

if __name__ == "__main__":
    main()
