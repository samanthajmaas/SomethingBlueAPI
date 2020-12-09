# rm -rf somethingblueapi/migrations
# rm db.sqlite3
python manage.py makemigrations somethingblueapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata brides
