file = open('results.txt', 'r')
lines = file.readlines()
sum = 0
for line in lines:
    sum += int(line.split(' ')[1])
print(sum/100)