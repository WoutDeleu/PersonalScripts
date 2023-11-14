import os
# os.rename(r'file path\OLD file name.file type', r'file path\NEW file name.file type')


def del_char(string, indexes):
    return "".join((char for idx, char in enumerate(string) if idx not in indexes))


def printIntro():
    print(
        "Welkom bij de File Extractor. \n" +
        "Deze tool is gemaakt om alle bestanden vanuit alle mappen en submapppen in deze directory te extracten!"
    )
    print()
    print()


def extract_files(old_location, new_location):
    directories = os.listdir(old_location + "/")
    for entry in directories:
        if os.path.isdir(entry):
            extract_files(old_location + "/" + entry, new_location)
        else:
            os.rename(old_location + "/" + entry, new_location + "/" + entry)


printIntro()

print("Plak de adres van de locatie (vorm: /home/woutd/Videos/Series/Ms Marvel/)")
location = input()

directories = os.listdir(location)

for directory in directories: 
    extract_files(location + "/" + directory, location)


