'''
name = "mohamed"
age = 35 
hobby = "reading"

print ("My name is " , name)
print ("iam" , age , "years old")
print ("i like" , hobby)
'''
'''
age = int(input("enter your age:  "))
if age < 18 :
    print("you are to young")
elif age <= 60:
    print("welcome")
else :
    print("enjoy your time")
'''
'''
for i in range (1 , 11):
    print(i)
'''
'''
i = 1 
while i <= 10 :
    print (i)
    i += 1
'''
'''
total = 0 
for i in range(1,10):
    total += i
print ("total :" , total)
'''
'''
name = input("enter your name")
print ("Hello," , name)
'''
'''
num = int(input("enter you number : "))
square = num * num
print (square)
'''
'''
number = int(input("enter your number : "))
if number % 2 == 0 :
    print(True)
else :
    print (False)
'''
'''
def greet(name):
    print("Hello,", name)

# تجربة
greet("Mohamed")
'''
'''
def square (num):
    return num * num

print (square(5))
'''
'''
def is_even (number):
    return number % 2 == 0

print (is_even(8))
print (is_even (7))
'''
'''
def reverse (name):
    return name [::-1]

print (reverse("Python"))
'''
'''
def word_count(sentence):
    return len(sentence.split())
print(word_count("i love learning python"))
'''
def count_vowels(text):
    vowels = set("aeiouAEIOU")
    return sum(1 for char in text if char in vowels)
print(count_vowels("Hello"))