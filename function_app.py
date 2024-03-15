import azure.functions as func
import logging
import pyodbc
from datetime import datetime, time


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="updateskillinventory")
def updateskillinventory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    driver = "{ODBC Driver 18 for SQL Server}"
    database = 'lps-sqldb-copilot-test'
    server = 'tcp:lps-sqlserver-test.database.windows.net,1433'
    username = 'terrencechan0830'
    password = 'Qa74ze7rqa74ze1r!'
    connection_string = f'Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=Yes;TrustServerCertificate=no;Connection Timeout=300;'

    name_val = req.params.get('nameval')
    if not name_val:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name_val = req_body.get('nameval')
            skill_val = req_body.get('skillval')
            date_val = req_body.get('dateval')

            # default_time = time(0, 0, 0)
            # parsed_date = datetime.strptime(date_val, "%Y-%m-%d").replace(time=default_time)
            # sql_datetime = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            insert_query = "INSERT INTO [Skill] (Name, Skill, acq_date) VALUES (?, ?, ?)"
            values = (name_val, skill_val, date_val)

            cursor.execute(insert_query, values)
            conn.commit()

    if name_val or skill_val or date_val:
        return func.HttpResponse(f"The following record has been inserted into database: {name_val}, {skill_val}, {date_val}.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )