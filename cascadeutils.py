import os

# A function to automate data aquisition of negative image examples for cascade classifier in
def generate_negative_description_file():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

generate_negative_description_file()