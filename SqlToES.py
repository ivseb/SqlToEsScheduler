import json
import pymssql
import schedule
import time

import psycopg2

with open('config.json') as f:
    data = json.load(f)

print(data)


def buildJob(connection, queries):
    obj = {}
    for query_element in queries:
        cursor = connection.cursor()
        cursor.execute(query_element['query'])
        result = cursor.fetchall()
        items = []
        for row in result:
            for key in cursor.description:
                items.append({key[0]: value for value in row})

        obj[query_element['description']] = items
    print(obj)


def buildScheduler(connection, group):
    s = schedule
    if 'every' in group:
        s = s.every(group['every'])
    else:
        s = s.every()
    if group['unit'] == "hours":
        s = s.hours
    if group['unit'] == "minutes":
        s = s.minutes
    if group['unit'] == "days":
        s = s.days
    if group['unit'] == "seconds":
        s = s.seconds
    #         TODO: gestire eccezione
    s.do(buildJob,connection, group['queries'])



def buildDBGroup(config):
    connection = psycopg2.connect(host=config['host'], user=config['user'], password=config['password'])
    for group in config['groups']:
        buildScheduler(connection, group)


for database, config in data['DBS'].items():
    buildDBGroup(config)

while True:
    schedule.run_pending()
    time.sleep(1)


exit(0)

conn = psycopg2.connect(host="localhost", user="postgres", password="postgres")
cursor = conn.cursor()

query = "SELECT datname FROM pg_database WHERE datistemplate = false"

cursor.execute(query)
result = cursor.fetchall()
items = []
for row in result:
    for key in cursor.description:
        items.append({key[0]: value for value in row})

print(json.dumps({'items': items}))


def job():
    print("I'm working...")


schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)



config = {}
config['GLOBAL'] = {}
config['GLOBAL']['ES_URL'] = 'http://127...'
config['GLOBAL']['ES_INDEX'] = 'GLOBAL_INDEX'
config['DBS'] = {}
config['DBS']['DB1'] = {}
config['DBS']['DB1']['host'] = "localhost"
config['DBS']['DB1']['user'] = "postgres"
config['DBS']['DB1']['password'] = "password"
config['DBS']['DB1']['QG1'] = {}
config['DBS']['DB1']['QG1']['every'] = 10
config['DBS']['DB1']['QG1']['unit'] = 'minutes'
config['DBS']['DB1']['QG1']["queries"] = [
    {"description": "first_query", "query": "SELECT datname FROM pg_database WHERE datistemplate = false"},
    {"description": "second_query", "query": "SELECT datname FROM pg_database WHERE datistemplate = false"},
]

with open('config.json', 'w') as configfile:
    configfile.write(json.dumps(config, indent=2))
