import json


rootUI: str = """
    FFmpeg Settings

(1) Input File
(2) Output File
(3) Global Options
(4) Input Options
(5) Output Options
(0) Compile Command

{}Selection (x): """

rootOptions = {
    "1": "inFile",
    "2": "outFile",
    "3": "settingsGlobal",
    "4": "settingsInput",
    "5": "settingsOutput",
    "0": "compile",
}

settingsInUI: str = """
    Input Options

(1) Video Codec
(2) Audio Codec
(c) Direct FFmpeg Input
(0) Confirm & Exit
(r) Reset all output options

{}Selection (x): """

settingsInOptions = {
    "1": "vcodec",
    "2": "acodec",
    "c": "custom",
    "0": "exit",
    "r": "reset",
}

settingsOutUI: str = """
    Output Options

(1) Video Codec
(2) Audio Codec
(c) Direct FFmpeg Input
(0) Confirm & Exit
(r) Reset all output options

{}Selection (x): """

settingsOutOptions = {
    "1": "vcodec",
    "2": "acodec",
    "c": "custom",
    "0": "exit",
    "r": "reset",
}

menus: dict = {
    "root": {"ui": rootUI, "options": rootOptions},
    "inFile": {"ui": "{}Path to input file: ", "options": {"any": None}},
    "outFile": {"ui": "{}Path to output file: ", "options": {"any": None}},
    "settingsGlobal": {},
    "settingsInput": {"ui": settingsInUI, "options": settingsInOptions},
    "settingsOutput": {"ui": settingsOutUI, "options": settingsOutOptions},
    "vcodecSet": {
        "ui": '{}Enter "list" for list of avaliable coders.\nName of video codec/coder: ',
        "options": {"any": None},
    },
    "acodecSet": {
        "ui": '{}Enter "list" for list of avaliable coders.\nName of audio codec/coder: ',
        "options": {"any": None},
    },
    "customSet": {
        "ui": "{}Input ffmpeg options: ",
        "options": {"any": None},
    },
}


with open("menus.json", "w") as f:
    json.dump(menus, f, indent=4)
