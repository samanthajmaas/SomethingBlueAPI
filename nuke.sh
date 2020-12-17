  #!/bin/bash

rm -rf somethingblueapi/migrations
rm db.sqlite3
python manage.py makemigrations somethingblueapi
python manage.py migrate
python manage.py loaddata checklistitems
python manage.py loaddata budgetitems
