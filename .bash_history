cd
ls -l
pwd
pip3 install --help
pip3 install --no-cache-dir -r requirements.txt 
python3 manage.py migrate
rm -f db.sqlite3 
python3 manage.py migrate
gunicorn mysite.wsgi:application -b 0:8000
