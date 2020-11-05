# Car Year Extractor
# Created On: 2020-11-04
# Updated On: 2020-11-04
# Written By: BZ

# Purpose: Extract the model year of a car from the title

# Input: string of Craigslist ad, delimited by spaces
# Returns: string value of car year

'''
Notes:
  Requires there to be no additional characters in the year cell (e.g. cannot accept '2001,' or ',2001')
'''

def car_year_extractor(input):
  line = input.split(' ')
  for element in line:
    try:
      if int(element) in range(1900,2050):
        return element
    except:
      continue