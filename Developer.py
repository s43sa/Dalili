from flask import render_template, request, session
import MySQLdb.cursors
import csv
from DataBase import app,mysql


@app.route("/SignAdmin", methods=['GET','POST'])
def SignAdmin():  
    msg=''
        # Check if "id" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'ID' in request.form and 'pass' in request.form:

        # Create variables
        Id = request.form['ID']
        password = request.form['pass']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        account=checkAdmin(Id,password,cursor)
        # If account exists in Developer table in Dalili database
        if account:
            # Create session data
            session['loggedinA'] = True
            session['Id'] = account['Id']
            session['Fname'] = account['Fname']
            
            # Redirect to Add project page  
            return render_template("Admin.html", title='Admin page')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template("Sign.html", msg=msg)
      


 
@app.route("/Admin", methods=['GET','POST'])
def Admin():
   # check if developer submitted the add new project form
    if request.method == 'POST' and'sel' in request.form   and 'Descrip' in request.form  and 'lang' in request.form and 'uni' in request.form  and 'link' in request.form and 'hw' in request.form:
       # get the values from the form
        category=request.form['sel']
        summary = request.form['Descrip']
        university= request.form['uni']
        link = request.form['link']
        language=request.form.getlist('lang')
        hw = request.form['hw']
        AddProject(category,summary,university,link,language,hw)
        msg = 'The project has been added successfully'
        return render_template("Admin.html",msg=msg)    
         
    return render_template('Sign.html')   
              
 
def checkAdmin(Id,password,cursor):
        # Check if account exists using MySQL
        
        cursor.execute('SELECT * FROM Developer WHERE Id = %s AND password = %s', (Id, password,))
        # Fetch  record and return result
        account = cursor.fetchone()
        if account:
            
            return account

        else:
            return None


def AddProject(category,summary,university,link,language,hw):

 # the header of the scv file(Dalili's project ideas)
    try:
     fieldnames = ['Category', 'Summary','Languages','University','Link','HardWare']
     project={'Category': category, 'Summary': summary, 'Languages': language, 'University': university, 'Link': link, 'HardWare': hw}
 
      # append the new project to the Dalili_DB file
      
     with open('Dalili_DB.csv','a+',encoding='UTF8', newline='') as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames)
            writer.writerow(project)
            inFile.close() 
    except:
        print("no file named Dalili")


