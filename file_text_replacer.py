import os

def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield os.path.join(path, file)
        else:
            # print(os.path.join(path, file))
            yield from get_files(os.path.join(path, file))


    
# creating a variable and storing the text
# that we want to search
search_text = "schemdraw"

# creating a variable and storing the text
# that we want to add
replace_text = "py_and_id"

# Opening our text file in read only
# mode using the open() function
for file in get_files('tests'):
    print(file)
    with open(file, encoding="utf8") as f:
        newText=f.read().replace('schemdraw', 'py_and_id')

    with open(file, "w", encoding="utf8") as f:
        f.write(newText)

# Printing Text replaced
print("Text replaced")
