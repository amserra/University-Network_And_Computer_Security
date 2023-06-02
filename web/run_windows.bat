@ECHO OFF 
pip3 install -r requirements.txt
set FLASK_ENV=development

flask run