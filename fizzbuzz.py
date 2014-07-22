"""
For a range of numbers going from 1 to 100: 
a) if the number is a multiple of 3 or contains the number 3, print "Fizz"
b) if the number is a multiple of 5 or contains the number 5, print "Buzz"
c) if a) and b), print "FizzBuzz"
d) otherwise print the number
"""

output = ''
for i in range(1, 100):
    print_number = True

    if i % 3 == 0 or '3' in str(i):
        output += 'Fizz'
        print_number = False
    if i % 5 == 0 or '5' in str(i):
        output += 'Buzz'
        print_number = False

    if print_number:
        output += str(i)

    output += '\n'

# Following the preconditions, 3 and 5 shouldn't occur in the final output
assert('3' not in output and '5' not in output)

print output
