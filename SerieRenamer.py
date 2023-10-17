import os
import re

# os.rename(r'file path\OLD file name.file type', r'file path\NEW file name.file type')


def del_char(string, indexes):
    return "".join((char for idx, char in enumerate(string) if idx not in indexes))


def rename_files(oldMoviePaths, newMoviePaths, oldSubPaths, newSubPaths, folders):
    for i in range(len(oldMoviePaths)):
        # Make Folder ot save the episode in
        if len(oldSubPaths) == len(oldMoviePaths):
            os.mkdir(folders[i])
            os.rename(oldSubPaths[i], newSubPaths[i])
        os.rename(oldMoviePaths[i], newMoviePaths[i])

        print(
            " ================================================================================================== "
        )
        print()
        print("Old Movie: " + oldMoviePaths[i])
        print("New Movie: " + newMoviePaths[i])

        if len(oldSubPaths) == len(oldMoviePaths):
            print(
                " -------------------------------------------------------------------------------------------------- "
            )
            print("Old Subtitle: " + oldSubPaths[i])
            print("New Subtitle: " + newSubPaths[i])
        print(
            " ================================================================================================== "
        )
        print()


def printIntro():
    print(
        "Welkom bij SerieRenamer."
        + "\n"
        + "Deze tool is gemaakt om series te hernoemen naar een standaard vorm (bv. S08E01) en in een aparte folder te plaatsen, zodat ze makkelijker te vinden zijn en duidelijk georganiseerd."
        + "\n"
        + "Zorg dat alle afleveringen in 1 folder staan, met eventueel bijhorende ondertitels!"
        + "\n"
        + "Dit script zal ze in een aparte folder plaatsen, met de juiste naam en de juiste ondertitel erbij"
        + "\n"
        + "\n"
        + "Pas op voor uitzonderingen, bv een aflevering in 2 delen"
        + "\n"
        + "Zorg dat ze alfabetisch geordend staan"
    )
    print()
    print()


def naarJuisteVorm(pad):
    locatie = del_char(pad, [0])
    locatie = del_char(locatie, [len(locatie) - 1])
    return locatie


def filter_movies_subs(arr, movies, subs):
    for fileName in arr:
        extensie = os.path.splitext(fileName)[1]
        if extensie == ".srt":
            subs.append(fileName)
        else:
            movies.append(fileName)


def findSubtitle_reg(subs, counter, seizoen):
    seizoen = str(int(seizoen))
    episode = str(counter)
    sub_pattern = r"^.*[sS]+\.?+0?" + seizoen + r"\.?+[Ee]+\.?+0?" + episode

    found = False
    double_found = False
    for sub in subs:
        if re.search(sub_pattern, sub) or sub.find("0" + episode):
            if found and not double_found:
                print("Er zijn 2 subs voor deze aflevering - We zitten me een probleem")
                double_found = True
            result = sub
            found = True
    if found and not double_found:
        return result
    print("Fucking hell")


def findSubtitle_index(subs, counter):
    sorted_movies = sorted(subs)
    return sorted_movies[counter - 1]


printIntro()

print("Geef de naam van het seizoen (bv 08)")
seizoen = input()

print("Plak de adres van de locatie (vorm: /home/woutd/Videos/Series/Ms Marvel/)")
# locatie = naarJuisteVorm(input())
locatie = input()

counter = 1
arr = os.listdir(locatie)
movies = []
subs = []
filter_movies_subs(arr, movies, subs)

oldMoviePaths = []
oldSubPaths = []
newMoviePaths = []
newSubPaths = []
folders = []
for movie in sorted(movies):
    # print(fileName)
    oldMovieName = movie
    movie_extension = os.path.splitext(oldMovieName)[1]

    # Format episode number: bv. E07
    episode = str(counter)
    if counter < 10:
        episode = "0" + episode
    episode = "E" + episode

    newName = "S" + seizoen + episode

    # New name of files
    folders.append(locatie + newName)

    # Remember path of the old file, to use in rename
    oldMoviePaths.append(locatie + oldMovieName)

    # Find the subtitle that belongs to the movie
    if len(subs) == len(movies):
        newMoviePaths.append(locatie + newName + "/" + newName + movie_extension)
        oldSubPaths.append(locatie + findSubtitle_index(subs, counter))
        newSubPaths.append(locatie + newName + "/" + newName + ".srt")
    else:
        newMoviePaths.append(locatie + newName + movie_extension)

    counter += 1

print()

rename_files(oldMoviePaths, newMoviePaths, oldSubPaths, newSubPaths, folders)

print("============DONE============")
