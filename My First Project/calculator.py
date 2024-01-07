# Write your code here
income = 202 + 118 + 2250 + 1680 + 1075 + 80

print(f"""Earned amount:
Bubblegum: $202
Toffee: $118
Ice cream: $2250
Milk chocolate: $1680
Doughnut: $1075
Pancake: $80

Income: ${income}""")
staff = int(input('Staff expenses:'))
other = int(input('Other expenses:'))
print(f'Net income: ${income - staff - other}')
