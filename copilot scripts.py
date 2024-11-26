import re

text = """
9 ; 11 tochni sostojbi
12 ; 11 tochni sostojbi uzhasni potezi
15 ; 11 tochni sostojbi losh tek na potezi
25 ; 11 tochni sostojbi
32 ; 11 tochni sostojbi
35 ; 11 ok
36 ; 11
54 ; 11
56 ; 11
65 ; 11
73 ; 11
78 ; 11
81 ; 11
90 ; 11
93 ; 11
98 ; 11
"""

# Extract numbers at the start of each line
numbers = re.findall(r'^\d+', text, re.MULTILINE)
numbers = [int(number) for number in numbers]
print(numbers)