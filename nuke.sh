  #!/bin/bash

rm -rf somethingblueapi/migrations
rm db.sqlite3
python manage.py makemigrations somethingblueapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata brides
python manage.py loaddata weddings
python manage.py loaddata checklistitems
python manage.py loaddata weddingchecklists
python manage.py loaddata budgetitems
python manage.py loaddata weddingbudgets