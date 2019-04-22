ACTIONS = {
    # app specific commands todo customise these from context
    "save":         "ctrl+s",
    "close":        "alt+F4",
    "pause":        "space",
    "play":         "space",
    # system commands
    "lock":         "win+l",
    # "select_all":   "ctrl+a",#
    "minimise":     "win+down",#
    # "maximize":     "win+up",
    "undo":         "ctrl+z",
    "cut":          "ctrl+x",
    "copy":         "ctrl+c",
    "paste":        "ctrl+v",
    "desktop":      "win+d",
    "screenshot":   "prtsc",#
    "switch":       "win+tab",#
    # todo account for other commands
}


## Legacy
COMMAND_SCOPE = (
"save", "pause", "close", "minimise", "lock", "maximise", "undo", "cut", "desktop", "switch", "search", "find", "sleep",
"screenshot", "eliza", "play", "launch",)
SLEEP_ACTION = "ctrl+esc"
def get_music_path():
    return "/home/karuhanga/Music"  # todo this should be a setting
HOME_PATH = "/home/karuhanga/"
