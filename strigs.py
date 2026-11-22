a = "gulabjamun"
print(a[0:5])
print(a[5:])

print(a.find("mu"))
print(a.replace("jamun","pani"))
print(a.count("a"))

practice Question 3

sen = input("Enter a sentence : ")
print("LowerCase : ",sen.lower())
print("Replaces all Spaces with underscore : ",sen.replace(" ","_"))
newstr = sen.lower()
newstr= sen.replace(" ","_")
print("New String : ",newstr)



"""Formatted Strings"""

name = "Ravi"
age = 17
print(f"my nameis : {name} and age is : {age}.")

"""Escape Sequence """

print("Hello \nWorld")
print("Hello \tWorld")# to make space of tab
