from flask import Flask, render_template, url_for
import LogAnalyticsDataReader as LogAnalyticsDataReader

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/data")
def fetch_data():

    query ="SecurityEvent | where EventID == 4634 or EventID == 4800 or EventID == 4624 | where Account contains 'alex' | project localTimeGenerated = TimeGenerated + 1h,Activity,Account | summarize by format_datetime(localTimeGenerated, 'dd/MM/yyyy'),format_datetime(localTimeGenerated, 'HH:mm'),Activity,Account"
    #query = "SecurityEvent | where EventID == 4634 or EventID == 4800 or EventID == 4624 | where Account contains 'alex'  | project localTimeGenerated=TimeGenerated+1h,Activity,Account,LogonType | summarize by localTimeGenerated,Activity,Account"
    sp_token = LogAnalyticsDataReader.get_token(tenant=app.config["TENANT"], sp_id=app.config["SP_ID"], sp_secret=app.config["SP_SECRET"])
    data = LogAnalyticsDataReader.get_data(query=query,token=sp_token, azure_log_customer_id=app.config["AZURE_LOG_CUSTOMER_ID"])
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0')
