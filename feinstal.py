# list = {"products": []}
# # это dictionary

# print(type(list))

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def show_age(self):
        return self.age

    def __str__(self):
        return self.name

class Employee(Person):
    def show_nage(self):
        return self.age+self.age

fields = ('jopa', 'piska')
list = []
nlist = {}

print(f'fields = type of {type(fields)}')
print(f'list = type of {type(list)}')
print(f'nlist = type of {type(nlist)}')