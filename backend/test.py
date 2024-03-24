
import math 

def calculate_area(radius):


    area = math.pi * radius ** 2 
    return area 

def calculate_perimeter(radius):

    return 2 * math.pi * radius 

if __name__ == "__main__":


    radius = 5.0 

    area = calculate_area(radius) 
    print("Area:", area) 

    perimeter = calculate_perimeter(radius) 
    print("Perimeter:", perimeter) 

