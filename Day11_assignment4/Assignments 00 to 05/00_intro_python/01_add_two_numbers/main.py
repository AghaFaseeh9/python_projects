def main():
    # Prompt the user to enter the first number
    num1 = input("Enter the first number: ")
    
    # Convert the input to an integer
    num1 = int(num1)
    
    # Prompt the user to enter the second number
    num2 = input("Enter the second number: ")
    
    # Convert the input to an integer
    num2 = int(num2)
    
    # Calculate the sum of the two numbers
    total = num1 + num2
    
    # Print the total sum with an appropriate message
    print("The total sum is: " + str(total))

# Ensure the main() function is called when the script is executed
if __name__ == "__main__":
    main()
