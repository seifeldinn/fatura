Fatura 101


Installation steps

execute command
    'export FLASK_APP=manage.py'  #setting the flask app variable to point to eh entry of the app in our case manage.py
    'export FLASK_ENV=development' #enabling the development mode defined in the config.py
    'pip install -r requirements.txt' install all libraries included in requirements.txt file
    'flask run' runs the application


side note:
please use vscode as i already configured the debug mode you have all the db related commands if you want to make changes in the data base. run the migrate and then upgrade commands defined in the launch.json and then the run command for running the app to check any desired line 
