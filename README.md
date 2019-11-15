# CZ4031-Query-Comparison-App

App currently only supports postgresql as database server. \
To connect the app with your database, \
Open `dbconfig.ini` \
Change configuration settings according to your database server. The format is:
```
host = [host address]
database = [database name]
user = [username]
password = [password]
```

Make sure you have **python 3.6 or above** installed.

Install necessary packages by running this code in the project's root directory:
```
pip install -r requirements.txt
```

Run app with
```
python app.py
```

In the window that appears, write 2 SQL queries into input field 1 and 2.\
Click `Get Plan` and wait for about 30s - 60s. \
The query plan differences will be displayed in the Difference field.

### Algorithm Explanation
The detailed algorithm can be found in [Algorithm.md](https://github.com/rhowardliu/CZ4031-Query-Comparison-App/blob/master/Algorithm.md.
