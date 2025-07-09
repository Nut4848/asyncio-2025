import time
from datetime import timedelta
import asyncio

speed = 100  # speed
Judit_time = 5/speed  # Judit time move
Opponent_time = 55/speed  # Opponent time move
opponents = 24  # Number of opponents
move_pairs = 30  # Number of move pairs

# Again notice that I declare the main() function as a async function
async def game(x):
    board_start_time = time.perf_counter()
    for i in range(move_pairs):
        # print(f"BOARD-{x} {i+1} Judit thinking of making a move.")
        # Don't use time.sleep in a async function. I'm using it because in reality you aren't thinking about making a
        # move on 24 boards at the same time, and so I need to block the event loop.
        time.sleep(Judit_time)
        print(f"BOARD-{x+1} {i+1} Judit made a move with {Judit_time*speed} secs.")

        # Here our opponent is making their turn and now we can move onto the next board.
        await asyncio.sleep(Opponent_time)
        print(f"BOARD-{x+1} {i+1} Opponent made move with {int(Opponent_time*speed)} secs.")
    print(f"BOARD-{x+1} -> >>>>>>>>>>>>>>>>>>>>> Finished move in {(time.perf_counter() - board_start_time)*speed:.1f} secs.\n")
    return {
        'calculated_board_time': (time.perf_counter() - board_start_time)*speed
    }

async def main():
    # Again same structure as in async-io.py
    tasks = []
    for i in range(opponents):
        tasks += [game(i)]
    await asyncio.gather(*tasks)
    print(f"Board exhibition finished for {opponents} opponents in {timedelta(seconds=speed*round(time.perf_counter() - start_time))} hr.")

if __name__ == "__main__":
    print(f"Number of games: {opponents} games.")
    print(f"Number of move: {move_pairs} pairs.")
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Finished in {round(time.perf_counter() - start_time)} secs.")
