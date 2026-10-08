from collections.abc import Callable

import game


def ask_int(
    message: str,
    check_fn: Callable[[int], bool],
    fail_message: str = "must be a positive integer",
):
    while True:
        try:
            result: int = int(input(message))

            if check_fn(result):
                break
            else:
                print(fail_message)
        except ValueError:
            print(fail_message)
    return result


def submit(playable_deck: list[int], target: int):
    best = 999

    for value in playable_deck:
        if value == target:
            return 0, 10
        else:
            difference = abs(value - target)
            best = min(difference, best)

    if best <= 5:
        return best, 7
    elif best <= 10:
        return best, 5
    else:
        return best, 0


if __name__ == "__main__":
    score = 0
    while True:
        large_choice = ask_int(
            "How many larges? (0-4)\n",
            lambda x: x >= 0 and x <= 4,
            "Must be between 0 and 4",
        )

        deck = game.draw_cards(large_choice)
        target = game.get_target()

        playable_deck = deck.copy()
        while True:
            print("\n\n")
            print(playable_deck)
            print(f"your target is {target}")
            print("""
    0. Quit
    1. Submit
    2. Skip
    3. Reset
            """)
            operation = input("Enter an operation: (a (+, -, *, /) b) ").strip()
            try:
                if operation == "0":
                    exit()
                elif operation == "1":
                    best, points = submit(playable_deck, target)
                    score += points
                    print(
                        f"you were {best} away from the target! your score is {score}"
                    )
                    break
                elif operation == "2":
                    break
                elif operation == "3":
                    playable_deck = deck.copy()
                    continue

                operation = operation.split()
                n1 = int(operation[0])
                n2 = int(operation[2])
                op = operation[1]
            except IndexError, ValueError:
                print("invalid operation")
                if len(operation) < 2:
                    print("have a space between each value")
                continue

            status, value = game.is_valid_step(n1, n2, op, playable_deck)
            if status == game.Status.OK and value is not None:
                game.update_pool(n1, n2, value, playable_deck)
            print(f"{status.value},  {value}")
