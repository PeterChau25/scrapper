#!/usr/bin/env python
# coding: utf-8

# In[12]:


import cl_car

car_make = {
  "Abarth": "Abarth",
  "Alfa Romeo":  "Alfa Romeo",
  "Aston Martin": "Aston Martin",
  "Audi": "Audi",
  "Bentley": "Bentley",
  "BMW": "BMW",
  "Bugatti": "Bugatti",
  "Cadillac": "Cadillac",
  "Chevrolet": "Chevrolet",
  "Chrysler": "Chrysler",
  "Chevy": "Chevy",  
  "Citroën": "Citroën",
  "Dacia": "Dacia",
  "Daewoo": "Daewoo",
  "Daihatsu": "Daihatsu",
  "Dodge": "Dodge",
  "Ferrari": "Ferrari",
  "Fiat": "Fiat",
  "Fisker": "Fisker",
  "Ford": "Ford",
  "Honda": "Honda",
  "Hummer": "Hummer",
  "Hyundai": "Hyundai",
  "Infiniti": "Infiniti",
  "Jaguar": "Jaguar",
  "Jeep": "Jeep",
  "Kia": "Kia",
  "Lamborghini": "Lamborghini",
  "Lancia":  "Lancia",
  "Land Rover": "Land Rover",
  "Lexus":"Lexus",
  "Lotus":"Lotus",
  "Maserati": "Maserati",
  "Maybach": "Maybach",
  "Mazda": "Mazda",
  "McLaren": "McLaren",
  "Mercedes-Benz": "Mercedes-Benz",
  "Mini": "Mini",
  "Mitsubishi": "Mitsubishi",
  "Morgan": "Morgan",
  "Nissan": "Nissan",
  "Peugeot": "Peugeot",
  "Porsche": "Porsche",
  "Renault": "Renault",
  "Rolls-Royce": "Rolls-Royce",
  "Rover": "Rover",
  "Saab": "Saab",
  "Seat": "Seat",
  "Skoda": "Skoda",
  "Smart": "Smart",
  "Subaru":  "Subaru",
  "Suzuki": "Suzuki",
  "Tesla": "Tesla",
  "Toyota": "Toyota",
  "Volkswagen": "Volkswagen",
  "Volvo":  "Volvo"
}

def remove_digit(input):
    y = [x for x in b if not(x.isdigit() or x[0] == '-' and x[1:].isdigit())] #removes any digits in strings 
    
    y = [p.capitalize() for p in no_int] # capitalize first letter of string to match up against car make list    
return y

def car_make(input, car_make):
    xx = [i for i in car_make]
        for i in xx: 
           if i in car_make: 
            return xx
