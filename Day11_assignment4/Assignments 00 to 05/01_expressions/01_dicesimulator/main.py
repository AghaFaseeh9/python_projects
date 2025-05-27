import random

def roll_dice():
    # Local variables for the dice rolls
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    
    return die1, die2

def main():
    # Simulate rolling the dice three times
    for i in range(1, 4):
        die1, die2 = roll_dice()  # Roll dice and get results
        print(f"Roll {i}: Die 1 = {die1}, Die 2 = {die2}")
        
# Ensure the main function runs when the script is executed
if __name__ == "__main__":
    main()
