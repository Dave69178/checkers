Installation:
Easiest method is to use the conda environment.yml.
  In the checkers/ directory that contains main.py, enter the following command:
    "conda env create --file=environment.yml". (conda must already be installed and callable from the terminal)
  This will create a conda environment called "checkers_env".
  Run "conda activate checkers_env" to activate the environment.
  In the checkers/ directory, run "python3 main.py" and the program should start.

If not using conda, the dependencies are specified in the environment.yml file and can be installed with pip.
The only dependencies are:
 - python=3.10
 - numpy=1.23
 - pygame


Uninstallation:
To remove the conda environment: "conda remove -n checkers_env".

This was created on Linux and doesn't run as cleanly on Windows, but functionality should be fine.

Some other notes regarding performance are within the report.
