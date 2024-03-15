import azure.functions as func
import logging
import pyodbc
from datetime import datetime


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="updateskillinventory")
def updateskillinventory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    driver = "{ODBC Driver 18 for SQL Server}"
    server = 'tcp:lps-ad-sql-server-2024jan.database.windows.net,1433'
    database = 'sql-database'
    username = 'CloudSA9d60b0b0'
    password = '@dmin2024'
    connection_string = f'Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=Yes;TrustServerCertificate=no;Connection Timeout=300;'

    name_val = req.params.get('nameval')
    if not name_val:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            cat_val = req_body.get('catval')
            name_val = req_body.get('nameval')
            ivt_val = req_body.get('ivtval')
            date_val = datetime.strptime(req_body.get('dateval'), "%d/%m/%Y").strftime("%Y-%m-%dT%H:%M:%S")

    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            if cat_val == 'Skill':
                insert_query = "INSERT INTO [Skill] (Name, Skill, acq_date) VALUES (?, ?, ?)"
            if cat_val == 'Certificate':
                insert_query = "INSERT INTO [Certificate] (Name, Certificate, acq_date) VALUES (?, ?, ?)"
            values = (name_val, ivt_val, date_val)
            cursor.execute(insert_query, values)
            conn.commit()

    if name_val or ivt_val or date_val:
        return func.HttpResponse(f"The following record has been inserted into database: {name_val}, {ivt_val}, {date_val}.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )