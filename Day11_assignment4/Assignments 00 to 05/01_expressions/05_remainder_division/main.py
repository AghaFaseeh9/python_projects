def main():
    # Ask the user for the first number (dividend)
    dividend = int(input("Please enter an integer to be divided: "))
    
    # Ask the user for the second number (divisor)
    divisor = int(input("Please enter an integer to divide by: "))
    
    # Perform the division and calculate the remainder
    result = dividend // divisor
    remainder = dividend % divisor
    
    # Print the result of the division and the remainder
    print(f"The result of this division is {result} with a remainder of {remainder}")

# Ensure the main function is called when the script is executed
if __name__ == "__main__":
    main()
