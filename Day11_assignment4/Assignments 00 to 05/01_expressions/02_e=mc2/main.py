# Constant for speed of light in meters per second
C = 299792458  # speed of light in m/s

def calculate_energy(mass):
    # E = m * c^2
    energy = mass * C**2
    return energy

def main():
    while True:
        # Prompt the user to enter the mass in kilograms
        mass_input = input("Enter kilos of mass: ")
        
        # Exit the loop if the user presses Enter without input
        if mass_input == "":
            print("Exiting program.")
            break
        
        # Convert the input to a float (mass in kilograms)
        try:
            mass = float(mass_input)
            energy = calculate_energy(mass)
            
            # Output the results
            print(f"\nE = m * C^2...\n")
            print(f"m = {mass} kg")
            print(f"C = {C} m/s")
            print(f"{energy} joules of energy!\n")
        
        except ValueError:
            print("Please enter a valid number for mass.")

# Ensure the main function is called when the script is executed
if __name__ == "__main__":
    main()
