import math

def calculate_hypotenuse(ab, ac):
    # Using the Pythagorean theorem: BC^2 = AB^2 + AC^2
    bc = math.sqrt(ab**2 + ac**2)
    return bc

def main():
    # Prompt the user for the lengths of the two perpendicular sides
    ab = float(input("Enter the length of AB: "))
    ac = float(input("Enter the length of AC: "))
    
    # Calculate the length of the hypotenuse
    bc = calculate_hypotenuse(ab, ac)
    
    # Output the result
    print(f"The length of BC (the hypotenuse) is: {bc}")

# Ensure the main function is called when the script is executed
if __name__ == "__main__":
    main()
