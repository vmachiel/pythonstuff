from itertools import combinations
import operator
import sys
import time


class Song:
    """
    The structure of a song. Has a default score of 0. Create an instance
    with song and artist name. Has methods scoreplus and scoreminus to increase
    and descrease the scores.
    """

    def __init__(self, name="no name", artist="no artist"):
        self.name = name
        self.artist = artist
        self._score = 0

    # make score a private property
    @property
    def score(self):
        return self._score

    def scoreplus3(self):
        """Adds 3 points for when this songs is the favorite"""
        self._score += 3

    def scoretie(self):
        """Adds one point for when this song is a tie"""
        self._score += 1

    @classmethod
    def from_tuple(cls, songdata_tuple):
        """Creates a instance from a tuple containing a song name and artist"""
        name, artist = songdata_tuple
        return cls(name, artist)

    def __getattr__(self, name):
        if name == "album" or name == "Album":
            return "Album titles aren't used."
        else:
            return "The class has no attribute called {}".format(name)

    def __repr__(self):
        return "{}: ({})".format(self.__class__.__name__, self.__dict__)

    def __str__(self):
        return "Song called: {} by {} with a score of {}.".format(self.name,
                                                                  self.artist,
                                                                  self.score)


def import_songs():
    """
    Imports the songs from the file, and returns them in the form of Song
    classes in the only global variable
    """
    # Opens songs and writes them into temporary songlist1
    try:
        with open("songs.txt", "r", encoding="UTF-8") as x:
            songlist_raw = x.readlines()
    except IOError:
        raise IOError()
    # Stripgs the newlines
    songlist = [line.rstrip('\n') for line in songlist_raw]
    # Adds each song/artist combo to the songlist as Song class
    songclass = []
    for x in songlist:  # Splits the song and artist and creates classes
        y = x.split(", ")
        songclass.append(Song(y[0], y[1]))
    return songclass


def combomaker(songclass):
    """
    Returns a list of index combinations for all song combinations. Returns
    a list with tulips containing of 2 intergers. Takes a list of instances of
    the Song class
    """
    count = list(range(0, len(songclass)))  # The ammount of songs you have
    return list(combinations(count, 2))  # All possible combinations


def compare(song1, song2):
    """
    Compares two songs and returns which is prefferec (1 or 2) or returns
    0 if it's a tie. Numbers are returned as strings
    """
    print("1:", song1.name, "by", song1.artist, "or,")
    print("2:", song2.name, "by", song2.artist, "?")
    # x is evaluated as a string and acts as a menu choice
    while True:
        x = input("Chose by selecting 0, 1 or 2 ")
        if x == "1":
            return 1
        elif x == "2":
            return 2
        elif x == "0":
            return 0
        else:
            print("Please try again ")


def comparing(songclass, combos):
    """
    Takes two arguments: songclass and combos. Does all the comparisons for
    the combinations you supply it (combo), and changes the scores of the
    songs (songclass) Uses the compare function to chose what happens. Returns
    the result as a list of sorted Song classes by score.
    """
    print("What song do you like better? Type 1 of 2 to chose")
    print("Type 0 to indicate no preferrence")
    for x in range(0, len(combos)):  # all the combinations
        # Runs compare function for the two songs in the current combo
        # Checks the return favorite, and adds scores appropriately
        comparison = compare(songclass[combos[x][0]], songclass[combos[x][1]])
        if comparison == 1:
            songclass[combos[x][0]].scoreplus3()
        elif comparison == 2:
            songclass[combos[x][1]].scoreplus3()
        else:
            songclass[combos[x][0]].scoretie()
            songclass[combos[x][1]].scoretie()
    # Sorts the songs by highest score from low to high The inverse is returned
    result = sorted(songclass, key=operator.attrgetter('score'))
    return result[::-1]


def recordResults(result):
    """
    Writes the results to a textfile in the same directory called
    Songresults.txt. Takes list of Songclass in order of scored points
    from high to low. Old results are not overwritten.
    """
    with open("SongResult.txt", "a", encoding="UTF-8") as sr:
        currentDate = time.strftime("%d/%m/%Y")
        currentTime = time.strftime("%H:%M:%S")
        sr.write("This is the result of: ")
        sr.write(currentDate)
        sr.write(", taken at: ")
        sr.write(currentTime)
        sr.write("\n\n")
        for x in range(len(result)):
            sr.write("{0}: {1} by {2} with a score of {3}.\n".
                     format(x + 1, result[x].name, result[x].artist,
                            result[x].score))
        sr.write("\n")


def printResult(result):
    """
    Prints the result to the console. Takes list of Songclass in order
    of scored points from high to low.
    """
    print("Your favorite song is {0}, by {1}".format(result[0].name,
                                                     result[0].artist))
    print("It had a score of: ", result[0].score)
    print("Here is a summary of all the songs and their scores: ")
    for x in range(0, len(result)):
        print("{0}: {1} by {2} with a score of {3}".format(
              x + 1, result[x].name, result[x].artist, result[x].score))


def main():
    try:
        songclass = import_songs()  # Imports songs into a list of classes
    except IOError:
        print("There is no file with songs and artist in this directory")
        print("The program will now exit")
        sys.exit()
    combos = combomaker(songclass)  # Creates a list with all combinations
    result = comparing(songclass, combos)  # Executes the comparison
    recordResults(result)  # records result to txt file
    printResult(result)  # print results to the user


if __name__ == "__main__":
    main()
