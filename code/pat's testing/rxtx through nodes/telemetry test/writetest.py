import os

text = "This is a test message to be written to a file."

#with open("test.txt", 'w') as file:
#    file.write(text)
    
with open("test.txt", 'r') as file:
    print(file.read())
# Add this at the end of your script to verify

    