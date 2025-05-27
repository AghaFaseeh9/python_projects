def convert_feet_to_inches(feet):
    # 1 foot is equal to 12 inches
    inches = feet * 12
    return inches

def main():
    # Ask the user for the length in feet
    feet = float(input("Enter the length in feet: "))
    
    # Convert feet to inches
    inches = convert_feet_to_inches(feet)
    
    # Output the result
    print(f"{feet} feet is equal to {inches} inches.")

# Ensure the main function is called when the script is executed
if __name__ == "__main__":
    main()
