def main():
    # Prompt the user to enter the temperature in Fahrenheit
    fahrenheit = input("Enter temperature in Fahrenheit: ")
    
    # Convert the input to a float to handle decimal values
    fahrenheit = float(fahrenheit)
    
    # Convert Fahrenheit to Celsius using the formula
    celsius = (fahrenheit - 32) * 5.0 / 9.0
    
    # Display the result
    print(f"Temperature: {fahrenheit}F = {celsius}C")

# Ensure the main() function is called when the script is executed
if __name__ == "__main__":
    main()
