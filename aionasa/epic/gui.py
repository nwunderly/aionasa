import os.path
import PySimpleGUI as sg


def scan_folder(folder):
    try:
        # Get list of files in folder
        file_list = os.listdir(folder)
    except Exception as e:
        #Print out an error if there is a problem with getting or reading the folder
        print(f'error reading folder {folder}\n{e.__class__.__name__}: {e}')
        #Create an empty result
        file_list = []
        #Return all the files that are images of gif, png, and jpeg catgories
    return [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".gif", ",jpg"))]


def open_gui(img_folder):
    # Create the layout interface
    #The column on the left consists of the listbox, directions, and chosen file name
    column1 = [
    #This text has the direction
        [sg.Text("Choose an image from the list below")],
    #This is the size of the column and the text
        [sg.Text(size=(40, 1), key="-TOUT-")],
    #This is the listbox code, including size, values and setting events.
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    #This is the second colum with just the chosen image.
    column2 = [

        [sg.Image(key="-IMAGE-")],
    ]
    #This physically dictates layout from left to right.
    interface = [
        [
            #This is the column with the list box
            sg.Column(column1),
            #This is the line that seperates the two columns
            sg.VSeperator(),
            #This is the image column
            sg.Column(column2),
        ]
    ]
    #This dictates the window information, from title of window to layout.
    window = sg.Window("Epic Image Viewer", interface)

    #We use the first function to read the images from the folder that we put the images in
    fnames = scan_folder(img_folder)
    #This finalizes all the previous information for this window
    window.finalize()
    #This updates the list box with all the new files after rerunning the script from the documentation
    window["-FILE LIST-"].update(fnames)

    #This is the loop for the event after files are read into the listbox
    while True:
    #Read the event and the listbox values from the gui window
        event, values = window.read()
    #This if statement allows the gui to close out and resets command prompt.
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    #This is the physical code that allows the user to open the images when clicking from the listbox.
        
    #This is the event of when a file is chosen from the list box
        elif event == "-FILE LIST-": 
            filename = None
            try:
            #This is the joins all pieces of the file name together    
                filename = os.path.join(
                    img_folder, values["-FILE LIST-"][0]
                )
            #The next two lines takes the keys and opens the image in the gui
                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(filename=filename)
            #This opens an error if the image cannot be pulled from the file. If you follow the instructions this will not happen.
            except Exception as e:
                print(f'error reading file {filename}\n{e.__class__.__name__}: {e}')
