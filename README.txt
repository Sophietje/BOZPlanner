To be able to run a local version of this project, please follow these steps:

- Make sure that Python version 3.4 or 3.5 is installed. You can check this by running the following command in your terminal: "python -V". Please note that it is possible that you have two versions of python installed.
- In case Python is not installed on your computer, please follow the steps on: https://www.python.org/downloads/ (NOTE: Install Python 3.4.X or 3.5.X!)

- Start your favourite Python IDE (for example Pycharm, https://www.jetbrains.com/pycharm/download/)
- Import all files of this project

- Make sure that you have pip installed. Pip can be installed by following the steps on: https://pip.pypa.io/en/stable/installing/

- This directory ("bozplanner" which also contains the README.txt) contains a file called "requirements.txt." This file lists all dependencies of the project. Run the following commands from a command line to install several dependencies:
	"pip install Django"
	"pip install icalendar"
	"pip install celery"
	"pip install django-celery"
	"pip install django-celery-email"
	"pip install django_extensions"

- Now in your IDE open local.template.py (located in "bozplanner/bozplanner/"), copy its contents. Make a new file in the same directory as local.template.py, name it "local.py". 
- Open a python interpreter 
- Execute the following command: "from django.utils.crypto import get_random_string; print(get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))"
- Copy the output of the command, to your local.py as value for SECRET_KEY. Such that SECRET_KEY = None changes to SECRET_KEY = #output_of_command. With #output_of_command equals the generated value.

- Now you should be able to run the application 'bozplanner' in your IDE. In the run configurations you are able to change the port on which the server should be run. 

