from flask import Flask, render_template, request
from flask_mysqldb  import MySQL
import pandas as pd

app = Flask(__name__, instance_relative_config=False)

app.config['MYSQL_USER'] = 'sql3328725'
app.config['MYSQL_PASSWORD'] = '768K4VAYyz'
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql3328725'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', methods=['post', 'get'])
def result():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name AS University, City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', ROUND((OutStateTuition*RequiredCredits), 2) AS 'Total Cost' FROM Programs ORDER BY (OutStateTuition*RequiredCredits) ASC;")
    result = cur.fetchall()
    df = pd.DataFrame.from_dict(result)
    title = 'Programs'
    df = df[['University','City','State','Type','In State Tuition','Out of State Tuition','Required Credits','Total Cost']]
    if request.method == 'POST':
        if request.form.get("submit") == "Show Programs":
            maxtuition = str(request.form.get("tuition"))
            gre = str(request.form.get("GRE"))
            recommendations = str(request.form.get("recommendations"))
            if maxtuition == "":
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', ROUND((OutStateTuition*RequiredCredits), 2) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements ORDER BY (OutStateTuition*RequiredCredits) ASC;"
            else:
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', ROUND((InStateTuition*RequiredCredits), 2) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID AND OutStateTuition<="+maxtuition+" AND GRE='"+gre+"' AND Recommendations<="+recommendations+" ORDER BY (OutStateTuition*RequiredCredits) ASC;"  
            cur.execute(query)
            result = cur.fetchall()
            df = pd.DataFrame.from_dict(result)
            df = df[['University','City','State','Type','In State Tuition','Out of State Tuition','Required Credits','Total Cost','Essay', 'GRE', 'Recommendations']]
        if request.form.get("submit") == "Show Concentrations":
            university = str(request.form.get("university"))
            if university == "":
                query = "SELECT * FROM Concentrations;"
            else:
                query = "SELECT * FROM Concentrations WHERE University='"+university+"';"
            cur.execute(query)
            result = cur.fetchall()
            title = 'Concentrations'
            df = pd.DataFrame.from_dict(result)
            df = df[['University','Concentration']]
    return render_template('home.html',tables=[df.to_html(classes='data')], titles=df.columns.values, variable=title)



