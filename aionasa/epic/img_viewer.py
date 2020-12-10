import os.path

import PySimpleGUI as sg


def scan_folder(folder):
    try:
        # Get list of files in folder
        file_list = os.listdir(folder)
    except Exception as e:
        print(f'error reading folder {folder}\n{e.__class__.__name__}: {e}')
        file_list = []

    return [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".gif", ",jpg"))]


def open_gui(img_folder):
    # First the window layout in 2 columns
    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [sg.Text("Choose an image from list on left:")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")],
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ]
    ]

    window = sg.Window("Image Viewer", layout)

    # automatically read the folder we dumped the images to
    fnames = scan_folder(img_folder)
    window.finalize()
    window["-FILE LIST-"].update(fnames)

    # event loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            fnames = scan_folder(folder)
            window["-FILE LIST-"].update(fnames)

        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(filename=filename)
            except Exception as e:
                print(f'error reading file {filename}\n{e.__class__.__name__}: {e}')
