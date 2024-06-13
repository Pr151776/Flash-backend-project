from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app=Flask(__name__)
#MySQL Connection
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Pr151776"
app.config["MYSQL_DB"]="prash"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


#Loading Home Page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM user"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)
    
#New User
@app.route("/addUser",methods=['GET','POST'])
def addUsers():
    if request.method == 'POST':
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        con=mysql.connection.cursor()
        sql="insert into user(NAME,AGE,CITY) value(%s,%s,%s);"
        con.execute(sql,[name,age,city])
        mysql.connection.commit()
        con.close()
        
        flash('User Details Added')
        #return to home page
        return redirect(url_for("home"))
    return render_template("addUsers.html")
    
#Update User
@app.route("/editUsers/<string:id>",methods=['GET','POST'])
def editUser(id):
    con=mysql.connection.cursor()
    if request.method == 'POST':
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        sql="update user set NAME=%s,AGE=%s,CITY=%s where ID=%s;"
        con.execute(sql,[name,age,city,id])
        mysql.connection.commit()
        con.close()
        
        flash('User Details Updated')
        #return to home page
        return redirect(url_for("home"))
        con=mysql.connection.cursor()
        
    sql="select * from user where ID=%s;"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("editUsers.html",datas=res)
    
#Delete User
@app.route("/deleteUsers/<string:id>",methods=['GET','POST'])
def deleteUser(id):
    con=mysql.connection.cursor()
    sql="delete from user where ID=%s;"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    
    flash('User Details Deleted')
    #return to home page
    return redirect(url_for("home"))

if(__name__ == '__main__'):
    app.secret_key="abc123"
    app.run(debug=True)