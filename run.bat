set FLASK_APP=flaskr

set FLASK_ENV=development

cd flaskr/static/styles 

sass style.sass style.css && cd ../../.. && flask run

