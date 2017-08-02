import os
import xml.etree.ElementTree as ET
import shutil


def copy_file(src, dest):
    """This function copes a file from one location to another"""
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)


def xml_import():
    """
    Copies the XML into a copy to not mess up the original by accident.
    It makes sure you return to the right current_wd
    """
    # First, make sure you delete the old copy, since the original is updated
    # a lot. If the old copy isn't there, no big deal.
    current_wd = os.getcwd()
    os.chdir("/Users/machielvandorst/Documents")
    try:
        os.remove("Copy.xml")
    except:
        pass
    # Copy the xml file
    copy_file("/Users/machielvandorst/Music/iTunes/iTunes Music Library.xml",
              "/Users/machielvandorst/Documents/Copy.xml")
    # Loads the xml file into variable.
    tree = ET.parse("Copy.xml")
    root = tree.getroot()

    # return to the starting wd.
    os.chdir(current_wd)
    return root


def data_from_xml(root):
    """
    This function assumes that a root variable exists with the XML loaded
    using x = ET.part("lkajf") and root = tree.getroot(). It also assumes the
    standards iTunes XML format. It returns a list of tuples, each tuple con-
    tains the name of the song, the artis, and if available its playcount.
    """
    songdata = []
    for x in range(0, len(root[0][13]), 2):
        # Every second element in the [0][13] is the bit that's interesting so
        # we need to take steps of 2.
        # it starts with the second [1] one, so therefore x + 1 is used.
        temp = []  # used to temp hold the extracted names etc.
        podcastflag = False  # Tracker to filter podcasts

        for y in range(0, len(root[0][13][x + 1])):
            # This loops through each songs entire tree of data. If one if them
            # has a text value of Name, the next one is the name so append that
            # same for artist and playcount. A loop is used, since the elements
            # location of the desired attributes varies per song.
            if root[0][13][x + 1][y].text == "Name":
                temp.append(root[0][13][x + 1][y + 1].text)
            if root[0][13][x + 1][y].text == "Artist":
                temp.append(root[0][13][x + 1][y + 1].text)
            if root[0][13][x + 1][y].text == "Play Count":
                temp.append(root[0][13][x + 1][y + 1].text)
            # Now, if the item y is a podcast , they will have a name, artist,
            # and playcount. We need to filter those:
            if root[0][13][x + 1][y].text == "Podcast":
                podcastflag = True

        # Now the songs data is extracted, if its has a playcount, make a tuple
        # of lenght 3 and fill it with: playcount, name, artist in that order
        if len(temp) == 3 and not podcastflag:
            temp_tuple = (int(temp[0]), temp[1], temp[2])
        # Finally, add the tuple to the final list.
            songdata.append(temp_tuple)

    return songdata


def bubblesort_xml(list_to_sort):
    """
    This is a version of bubblesort that can be used to sort the songdata
    from the xml function.
    """
    for pass_no in range(len(list_to_sort) - 1, 0, -1):
        for n in range(0, pass_no):
            if list_to_sort[n][0] > list_to_sort[n + 1][0]:
                list_to_sort[n], list_to_sort[n + 1] = \
                    list_to_sort[n + 1], list_to_sort[n]
    return list_to_sort


def write_topsongs(songs):
    """
    This takes the top songs and writes them to a textfile for use in
    the other program. Takes the songdata from the XML sorted, and the
    number of songs you want. This is done by user input.
    """
    print("How many songs do you want?\nPlease enter a whole number,",
          "negative numbers will be made positive.")
    # get and check input
    while True:
        try:
            number_of_songs = abs(int(input("No of songs ")))
            break
        except ValueError:
            print("Please enter a whole number")
    # Delete the older songs.txt if it's there:
    try:
        os.remove("songs.txt")
    except:
        pass
    # Create a new .txt file and write the song name and artist seperated by
    # a , This is what the compare program expects.
    with open("songs.txt", "w", encoding="UTF-8") as topsongs:
        for y in range(number_of_songs):
            topsongs.write(songs[y][1] + ", " + songs[y][2])
            topsongs.write("\n")


def main():
    root = xml_import()
    songdata = data_from_xml(root)
    sorted_songdata = bubblesort_xml(songdata)[::-1]
    write_topsongs(sorted_songdata)


if __name__ == "__main__":
    main()
