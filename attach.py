r"""
This is a GUI app that finds all the attachments you've sent or have received
via iMessage. This are visible in the app, but the actual files are all over
the place. This app finds them and puts them in a folder that you name in the
user's downloads folder. This is intended as a "my first GUI" app, since a
single script could find all the files and move them to a standard downloads
folder far more efficiently.
"""

from tkinter import *
import os
import re
import shutil


def copy_file(src, dest):
    """
    This function copes a file from one location to another. Takes two
    parameters, the path the source, and the path to the destination. Both as
    strings. Requires the shutil module.
    """
    try:
        shutil.copy(src, dest)
    # src and dest are the same file
    except shutil.Error as e:
        print("Error: ", e)
    # source or destination doesn't exist
    except IOError as e:
        print("Error: ", e.strerror)


def find_attachments(pathToFiles):
    """
    This function takes a string with the path to the files
    It returns a tuple with full paths to all the files you'll want to copy
    """
    # Perform an os.walk in the path passed to the function. Return to old
    # wd afterwards for consistency.
    oldWorkingDir = os.getcwd()
    os.chdir(pathToFiles)
    list_of_files = list(os.walk(os.getcwd()))  # list() dir to use len() later
    os.chdir(oldWorkingDir)
    # The os.walk generates tuples in the form of (current dir, dirs in
    # that dir, files in that dir). It goes into each dir it finds. So in the
    # end, you'll want all the [0]th elements (current path it's in) and the
    # [2]th element (all the files in that dir).

    # pre compile a REX. You'll want these extensions and the end of the string
    filePattern = re.compile(r"(.mov|.jpg|.JPG|.MOV|.jpeg|.JPEG|.png|.PNG)$")
    # The two return values
    movelist = []

    # for each of the files in the [2]th element of each tuple: check if the
    # pattern matches. If it does, add the full path+file to file_to_move
    for x in range(len(list_of_files)):
        for y in range(len(list_of_files[x][2])):
            if filePattern.search(list_of_files[x][2][y]):
                movelist.append(os.path.join(list_of_files[x][0],
                                             list_of_files[x][2][y]))
    return tuple(movelist)


def destination_path_correction(oldfolder):
    """
    This function takes a foldername and returns a foldername. If the folder
    name ends in a _x where x is a number, it ads one to the number. If not,
    it'll add _2. This function can be used when a destination folder already
    exists, and will only be called if this is the case.
    """
    # First: does it have an underscore as a second to last char :
    underscore = False
    if oldfolder[-2] == "_":
        underscore = True
    # Is the last char a number and the second to last an _ like _4 : then it
    # needs to be incremented by one like _5
    lastCharacter = oldfolder[-1]
    try:
        intLastCharacter = int(lastCharacter)
        if underscore:
            new_number = str(intLastCharacter + 1)
            newfolder = oldfolder[0:-1] + new_number
        # if the last char is number but not already a _x type counter, just
        # add _2
        else:
            newfolder = oldfolder + "_2"
    # if the last char isn't a int, add _2
    except ValueError:
        if underscore or oldfolder[-1] == "_":
            newfolder = oldfolder + "2"
        else:
            newfolder = oldfolder + "_2"

    return newfolder


def main_app(username="machielvandorst", destname="Downloads",
             foldername="iMessage Attachments"):
    """
    This is the main logic of the app that's behind the GUI. It takes a
    username and a destination folder name. It has default values to make
    refactoring easy. It doesn't return anything.
    """
    # construct the paths to where the attachments are, and where they need
    # to go. Error handeling regarding the path is done in the Application
    path_to_attachment = "/Users/" + username + "/Library/Messages/Attachments"
    destination_path = "/Users/{}/{}/{}".format(username, destname, foldername)
    # Try to make the needed path, if it fails call the correction function.
    # This will happen when the foldername already exists.
    try:
        os.makedirs(destination_path)
    except OSError:
        main_app(username, destname, destination_path_correction(
                 foldername))
    # Finally, create the moveList (return value of find_attachments) and
    # perform the copy.
    movelist = find_attachments(path_to_attachment)
    for n in range(len(movelist)):
        copy_file(movelist[n], os.path.join(destination_path,
                                            os.path.basename(movelist[n])))


"""
From here on out, the file copying logic is done. All the following code is
used to build the main GUI and methods to deal with user input.
"""


class Application(Frame):
    """
    This class builds GUI. It has an __init__ section which intializes the
    master frame and local variables. It has a createWidgets method which
    builds and lays out all the widgets. Finally, it has methods for the button
    presses. The app has three stages, which are indicated by the control Bools
    False, False = step 1, True, False = step 2, and True, True = step 3 = done
    These conditions are reffered to throughout the class. Stage 1 is input
    username, Stage 2 is input foldername that you want, Stage 3 is done, don't
    take anymore input or do anything.
    """

    def __init__(self, master):
        """
        Intializes all the classes variables, call the createWidgets() methods,
        and calls pack() to place the main window.
        """
        Frame.__init__(self, master)
        self.root = master  # The master frame
        self.usernameSucces = False  # Username has been entered and verified
        self.transferSucces = False  # The app has done it's job.
        self.username = ""  # These two are the main goals of the GUI.
        self.foldername = ""
        self.explainText = StringVar()  # Used to display instuctions
        self.actionText = StringVar()  # Used to display action feedback.
        self.explainText.set("Please enter your Mac username \n"
                             "This is the same as your homefolder:")
        self.actionText.set("\n")  # the text widgets must be two lines always
        self.createWidgets()  # Create all the different elements of the GUI
        self.pack()  # place the main frame on screen.

    def createWidgets(self):
        """
        Creates and places all the widgets in the main frame. Uses the pack
        layout. Layout is from top to bottom: instuctions text, input for the
        user, action feedback text, row of buttons (OK, Clear, Back, Quit).
        """
        self.explainDisplay = Label(self, textvariable=self.explainText)
        self.explainDisplay.pack()

        self.inputText = Entry(self, width=20)
        self.inputText.pack()
        self.inputText.focus()  # Puts the curser in already so user can start
        # typing right away.

        self.actionDisplay = Label(self, textvariable=self.actionText)
        self.actionDisplay.pack()

        # command=x refers to application methods.
        self.okButton = Button(self, text="OK", command=self.check_action)
        self.okButton.pack(side="left", expand=YES)
        self.root.bind("<Return>", self.check_action_event)  # bind the Enter
        # button on keyboard to custom event leading to check_action

        self.inputButton = Button(self, text="Clear Text",
                                  command=self.clear_text)
        self.inputButton.pack(side="left", expand=YES)

        self.backButton = Button(self, text="Back", command=self.back)
        self.backButton.pack(side="left", expand=YES)

        self.quitButton = Button(self, text="QUIT", command=self.root.destroy)
        self.quitButton.pack(side="left", expand=YES)

    def check_action(self):
        """
        Called by the OK button. If username isn't entered and app not
        completed call extract_username (False, False) if usermame is found
        only, call extract_foldername_and_main (True, False) ,else do nothing
        because app is done (True, True).
        """
        if not self.usernameSucces and not self.transferSucces:
            self.extract_username()
        elif self.usernameSucces and not self.transferSucces:
            self.extract_foldername_and_main()
        else:
            pass

    def check_action_event(self, event):
        """Event method leading Enter to check_action"""
        self.check_action()

    def clear_text(self):
        """Called by the clear button, clears the text input field."""
        self.inputText.delete(0, 'end')

    def back(self):
        """Called by the back button, goes back one step."""
        # if you entered a username, and have not done transfer yet (True,
        # False)
        if self.usernameSucces and not self.transferSucces:
            self.username = ""  # clear username
            self.usernameSucces = False  # Make sure check_action is corrected.
            self.explainText.set("Please enter your Mac username \n"
                                 "This is the same as your homefolder:")
            self.actionText.set("\n")
        # When done, give feedback that you can't go back anymore (True, True).
        elif self.usernameSucces and self.transferSucces:
            self.actionText.set("You can't go back, you're done. \n"
                                "Made by Machiel van Dorst")
        else:
            pass

    def extract_username(self):
        """
        Called by OK if no username has been entered yet (False, False).
        Verifies username, and updates the usernameSucces bool if username is
        OK.
        """
        self.username = self.inputText.get()  # User input
        # check if the username exists, if not function is done and user can
        # try again.
        if not os.path.isdir("/Users/" + self.username + "/Movies/"):
            self.actionText.set("This isn't an existing username, please"
                                "\n try again.")
        else:
            # check if you have permission (it's your username), using test-
            # folder. If you do update instructions and control boolyan.
            try:
                os.makedirs("/Users/" + self.username + "/test/")
            except PermissionError:
                self.actionText.set("This isn't your homefolder, you do not \n"
                                    "have permission to access these files.")
            else:
                os.rmdir("/Users/" + self.username + "/test/")
                self.actionText.set("Username correct. \n")
                self.clear_text()
                self.explainText.set("Choose a folder name for your \n"
                                     "attachments:")
                self.usernameSucces = True

    def extract_foldername_and_main(self):
        """
        Called by okButton when the username has been entered but the dest
        folder hasn't yet (True, False).
        Excutes the naming of the destination folder and calls the main app
        logic. The app currently doesn't ask for a destination name.
        """
        self.foldername = self.inputText.get()  # get user input
        # Check if they contain illegal chars, if not, pass username and
        # foldername to the main function.
        chars = re.compile(r"""(\.|\:|/|\\|\$|¢|™|®|,|\[|\]|\{|\}|\(|\)|!|;|\"
                                |\'|\*|\?|<|\s|>|\|)""", re.VERBOSE)
        if chars.search(self.foldername):
            list_found = chars.findall(self.foldername)
            unique_list_found = tuple(set(list_found))
            if not unique_list_found[0] == " ":
                self.actionText.set("You can't use {} in you filename\n"
                                    "please choose another name".
                                    format(unique_list_found[0]))
            else:
                self.actionText.set("Please don't use space characters\n"
                                    "in the foldername")
        else:
            if not self.foldername:  # Is the string empty? do nothing
                pass
            else:
                main_app(username=self.username, foldername=self.foldername)
                # If all went well (True, True):
                self.explainText.set("Succes! Check your downloads folder :)\n"
                                     "You may now quit the app.")
                self.actionText.set("\nMade by Machiel van Dorst")
                self.transferSucces = True  # The GUI functions are done.


def window_size_and_space(root):
    """
    Returns a window size and placement in the format used by tkinter:
    "WidthxHeigh+Hordisplacement+Verdisplacement"
    """
    # get the systems screen width/height and set desired app width/height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app_width = 320
    app_height = 150
    # displament of the top-left corner is calculted so that app is centered.
    horizontal_displacement = int((screen_width / 2) - (app_width / 2))
    vertical_displacement = int((screen_height / 2) - (app_height / 2))
    # return is the format used by tkinter
    return "{}x{}+{}+{}".format(str(app_width), str(app_height),
                                str(horizontal_displacement),
                                str(vertical_displacement))


"""
Finally, the GUI is started using the root = Tk() --> app = *Class(root)*
--> app.mainloop() method. The root window is given a name, and geo via the
window_size_and_space function.
"""


def main():
    root = Tk()
    root.title("Attachment Organizer")
    root.geometry(window_size_and_space(root))
    root.lift()  # place it on top of other windows, doesn't work properly
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
