pip3 install -r requirements.txt
mongod --dbpath ./logs/mongo --fork --syslog
python3 app.py
