from flask import Flask, render_template, request, flash
from flask_mysqldb  import MySQL
import pandas as pd

pd.options.display.float_format = '${:,.2f}'.format

app = Flask(__name__, instance_relative_config=False)

app.config['MYSQL_USER'] = 
app.config['MYSQL_PASSWORD'] = 
app.config['MYSQL_HOST'] = 
app.config['MYSQL_DB'] = 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', methods=['post', 'get'])
def result():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name AS University, City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost' FROM Programs ORDER BY (OutStateTuition*RequiredCredits) ASC;")
    result = cur.fetchall()
    df = pd.DataFrame.from_dict(result)
    title = 'Programs'
    df = df[['University','City','State','Type','In State Tuition','Out of State Tuition','Required Credits','Total Cost']]
    if request.method == 'POST':
        if request.form.get("submit") == "Show Programs":
            maxtuition = str(request.form.get("tuition"))
            gre = str(request.form.get("GRE"))
            recommendations = str(request.form.get("recommendations"))
            if recommendations == "Yes":
                recommendations = "10"
            elif recommendations == "No":
                recommendations = "0"
            if maxtuition == 'None' and gre == 'None' and recommendations == 'None':
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID ORDER BY (OutStateTuition*RequiredCredits) ASC;"
            elif maxtuition != 'None' and gre != 'None' and recommendations != 'None':
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID AND (OutStateTuition*RequiredCredits)<="+maxtuition+" AND GRE='"+gre+"' AND Recommendations<="+recommendations+" ORDER BY (OutStateTuition*RequiredCredits) ASC;"
            elif maxtuition != 'None' and gre != 'None' and recommendations == 'None':
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID AND (OutStateTuition*RequiredCredits)<="+maxtuition+" AND GRE='"+gre+"' ORDER BY (OutStateTuition*RequiredCredits) ASC;"
            elif maxtuition != 'None' and gre == 'None' and recommendations == 'None':
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID AND (OutStateTuition*RequiredCredits)<="+maxtuition+" ORDER BY (OutStateTuition*RequiredCredits) ASC;"
            elif maxtuition == 'None' and gre != 'None' and recommendations != 'None':
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID AND GRE='"+gre+"' AND Recommendations<="+recommendations+" ORDER BY (OutStateTuition*RequiredCredits) ASC;"
            elif maxtuition == 'None' and gre != 'None' and recommendations == 'None':
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID AND GRE='"+gre+"' ORDER BY (OutStateTuition*RequiredCredits) ASC;"
            elif maxtuition == 'None' and gre == 'None' and recommendations != 'None':
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID AND Recommendations<="+recommendations+" ORDER BY (OutStateTuition*RequiredCredits) ASC;"
            elif maxtuition != 'None' and gre == 'None' and recommendations != 'None':
                query = "SELECT Name AS 'University', City, State, Type, InStateTuition AS 'In State Tuition', OutStateTuition AS 'Out of State Tuition', RequiredCredits AS 'Required Credits', (OutStateTuition*RequiredCredits) AS 'Total Cost', Essay, GRE, Recommendations FROM Programs, Application_Requirements WHERE ApplicationRequirements=ID AND (OutStateTuition*RequiredCredits)<="+maxtuition+" AND Recommendations<="+recommendations+" ORDER BY (OutStateTuition*RequiredCredits) ASC;"  
            cur.execute(query)
            result = cur.fetchall()
            df = pd.DataFrame.from_dict(result)
            df = df[['University','City','State','Type','In State Tuition','Out of State Tuition','Required Credits','Total Cost','Essay', 'GRE', 'Recommendations']]
        if request.form.get("submit") == "Show Concentrations":
            university = str(request.form.get("university"))
            select = str(request.form.get("select"))
            if university == "":
                query = "SELECT * FROM Concentrations;"
            elif select == "Uni":
                query = "SELECT * FROM Concentrations WHERE University LIKE '%"+university+"%';"
            elif select == "Con":
                query = "SELECT * FROM Concentrations WHERE Concentration LIKE '%"+university+"%';"
            cur.execute(query)
            result = cur.fetchall()
            if not result:
                return render_template('error.html',tables=[df.to_html(classes='data')], titles=df.columns.values, variable=title)
            title = 'Concentrations'
            df = pd.DataFrame.from_dict(result)
            df = df[['University','Concentration']]
    return render_template('home.html',tables=[df.to_html(classes='data')], titles=df.columns.values, variable=title)



