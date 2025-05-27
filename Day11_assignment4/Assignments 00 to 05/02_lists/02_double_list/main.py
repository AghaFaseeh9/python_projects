def double_numbers(numbers: list[int]) -> list[int]:
 
    return [num * 2 for num in numbers]  #

def main():
    numbers = [1, 2, 3, 4] 
    doubled_numbers = double_numbers(numbers) 
    print(doubled_numbers)  


if __name__ == '__main__':
    main()
