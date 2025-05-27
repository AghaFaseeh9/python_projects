import random

def roll_dice():
    # Roll two dice and return the results
    die1 = random.randint(1, 6)  # Roll the first die
    die2 = random.randint(1, 6)  # Roll the second die
    
    return die1, die2

def  main():
    # Simulate rolling two dice
    die1, die2 = roll_dice()
    
    # Calculate the total
    total = die1 + die2
    
    # Print the results of each roll and the total
    print(f"Roll results: Die 1 = {die1}, Die 2 = {die2}")
    print(f"Total: {die1} + {die2} = {total}")

# Call the main function
if __name__ == "__main__":
    main()
