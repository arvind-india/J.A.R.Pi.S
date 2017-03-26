from pathlib import Path
from os import sep as path_separator

# This fixes the Path.resolve() issue for the local dev systems.
# Path.resolve() tries to resolve from the current working directory (os.getcwd())
# but while testing the cwd is the jarpis project root, and there is no "recordings"
# folder. Therefore we need the relative path inside the project here.
#
# IMPORTANT: When in the jasper application the cwd is again different!
#            But it should be possible to set the cwd to the directory this file resides in
#            for a temporary manner.
audiofile_path = str(Path("jarpis", "recognition",
                          "recordings").resolve()) + path_separator
