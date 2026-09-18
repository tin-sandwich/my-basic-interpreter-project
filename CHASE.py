import random
import sys

def print_instructions():
    print(" " * 30 + "CHASE")
    print(" " * 15 + "CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY")
    print("\n")
    print("YOU ARE IN A HIGH-VOLTAGE AREA PREYED UPON BY CHASERS.")
    print("THE AREA IS AN 8 X 8 MATRIX SURROUNDED BY A HIGH-VOLTAGE FENCE.")
    print("THERE ARE ALSO SECURITY INTERCEPTORS INSIDE THE AREA.")
    print("IF YOU TOUCH A CHASER OR A SECURITY INTERCEPTOR OR")
    print("THE FENCE, YOU ARE DEAD.")
    print("THE SECURITY INTERCEPTORS MOVE TWICE AS FAST AS THE CHASERS.")
    print("YOUR ONLY HOPE IS TO DRAG THE CHASERS AND INTERCEPTORS")
    print("INTO COUPLING WITH EACH OTHER OR RUNNING INTO THE FENCE.")
    print("\nYOUR MOVE NUMBERS SPECIFY DIRECTIONS ACCORDING TO A")
    print("STANDARD NUMERIC COMPASS GRID KEYPAD:")
    print("  7  8  9")
    print("  4     6")
    print("  1  2  3")
    print("ENTER 5 TO STAND STILL FOR A TURN.")
    print("-" * 50)

def main():
    print_instructions()
    
    # 8x8 Grid initialization (1-indexed for simplicity matching BASIC logic)
    # The original game typically populates you, 3 chasers, and 2 security interceptors.
    while True:
        # Initial positions
        player_x = random.randint(1, 8)
        player_y = random.randint(1, 8)
        
        # 3 Chasers (C) and 2 Security Interceptors (I)
        chasers = []
        for _ in range(3):
            chasers.append([random.randint(1, 8), random.randint(1, 8)])
        interceptors = []
        for _ in range(2):
            interceptors.append([random.randint(1, 8), random.randint(1, 8)])
            
        # Ensure nothing spawns right on top of the player at turn 0
        collision = False
        for c in chasers + interceptors:
            if c[0] == player_x and c[1] == player_y:
                collision = True
        if not collision:
            break

    # Main game loop
    turns = 0
    while True:
        turns += 1
        print(f"\n--- TURN {turns} ---")
        print(f"YOUR POSITION IS: ROW {player_y}, COLUMN {player_x}")
        
        # Display enemy positions
        for i, c in enumerate(chasers):
            print(f"CHASER {i+1} POSITION: ROW {c[1]}, COLUMN {c[0]}")
        for i, ic in enumerate(interceptors):
            print(f"INTERCEPTOR {i+1} POSITION: ROW {ic[1]}, COLUMN {ic[0]}")
            
        # Get Player Move
        while True:
            try:
                move = int(input("\nYOUR MOVE (1-9)? "))
                if move in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    break
                print("INVALID DIRECTION. USE STANDARD KEYPAD DIRECTIONS (1-9).")
            except ValueError:
                print("PLEASE ENTER A VALID INTEGER COMPASS DIRECTION.")
                
        # Move Player map (dx, dy) matching numeric keypad configuration
        move_map = {
            7: (-1, -1), 8: (0, -1),  9: (1, -1),
            4: (-1, 0),  5: (0, 0),   6: (1, 0),
            1: (-1, 1),  2: (0, 1),   3: (1, 1)
        }
        
        dx, dy = move_map[move]
        player_x += dx
        player_y += dy
        
        # Check if Player hit the boundaries/fence
        if player_x < 1 or player_x > 8 or player_y < 1 or player_y > 8:
            print("\n*** YOU RAN INTO THE HIGH-VOLTAGE FENCE AND FRIED! ***")
            print("GAME OVER.")
            sys.exit()

        # Update Enemy Positions (Chasers move 1 step towards player)
        for c in chasers:
            if c[0] < player_x: c[0] += 1
            elif c[0] > player_x: c[0] -= 1
            if c[1] < player_y: c[1] += 1
            elif c[1] > player_y: c[1] -= 1

        # Interceptors move twice as fast (2 steps towards player)
        for ic in interceptors:
            for _ in range(2):
                if ic[0] < player_x: ic[0] += 1
                elif ic[0] > player_x: ic[0] -= 1
                if ic[1] < player_y: ic[1] += 1
                elif ic[1] > player_y: ic[1] -= 1
                
        # Check Player-Enemy Collisions
        for c in chasers:
            if c[0] == player_x and c[1] == player_y:
                print("\n*** A CHASER CAUGHT YOU! YOU ARE DEAD. ***")
                sys.exit()
        for ic in interceptors:
            if ic[0] == player_x and ic[1] == player_y:
                print("\n*** AN INTERCEPTOR SLAMMED INTO YOU! YOU ARE DEAD. ***")
                sys.exit()

        # Handle Enemy-to-Enemy crashes or deaths on boundaries
        # Active lists to store who survived this turn
        surviving_chasers = []
        surviving_interceptors = []

        for c in chasers:
            # Check if chaser hit an outer fence boundary
            if c[0] < 1 or c[0] > 8 or c[1] < 1 or c[1] > 8:
                print("A CHASER CRASHED INTO THE HIGH-VOLTAGE FENCE!")
                continue
            surviving_chasers.append(c)

        for ic in interceptors:
            if ic[0] < 1 or ic[0] > 8 or ic[1] < 1 or ic[1] > 8:
                print("AN INTERCEPTOR EXPLODED AGAINST THE FENCE!")
                continue
            surviving_interceptors.append(ic)

        # Look for cross-collisions between enemies
        # We flag indices that collide
        c_remove = set()
        ic_remove = set()

        for i, c in enumerate(surviving_chasers):
            for j, ic in enumerate(surviving_interceptors):
                if c[0] == ic[0] and c[1] == ic[1]:
                    print(f"CRASH! A CHASER AND AN INTERCEPTOR DESTROYED EACH OTHER AT ROW {c[1]}, COL {c[0]}!")
                    c_remove.add(i)
                    ic_remove.add(j)

        # Filter out destroyed units
        chasers = [c for idx, c in enumerate(surviving_chasers) if idx not in c_remove]
        interceptors = [ic for idx, ic in enumerate(surviving_interceptors) if idx not in ic_remove]

        # Check Win Condition
        if len(chasers) == 0 and len(interceptors) == 0:
            print(f"\nVICTORY! YOU CLEARED THE GRID IN {turns} TURNS!")
            print("ALL PURSUERS HAVE BEEN INCINERATED.")
            sys.exit()

if __name__ == "__main__":
    main()
