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

    query = "SecurityEvent | where TargetAccount contains "azure" and ((EventID==4624 and (LogonType ==2 or LogonType == 11)) or (EventID == 4800) or (EventID == 4801) or (EventID == 4647) or (EventID == 4802) or (EventID == 4803) or (EventID == 4608))| project TimeGenerated,LogonTypeName,Activity,TargetUserName,TargetLogonId | summarize take_any(Activity,TargetUserName,TargetLogonId) by letemps=format_datetime(TimeGenerated+1h, 'dd/MM/yyyy HH:mm') | sort by letemps desc"
    sp_token = LogAnalyticsDataReader.get_token(tenant=app.config["TENANT"], sp_id=app.config["SP_ID"], sp_secret=app.config["SP_SECRET"])
    data = LogAnalyticsDataReader.get_data(query=query,token=sp_token, azure_log_customer_id=app.config["AZURE_LOG_CUSTOMER_ID"])
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0')
