from flask import Flask, render_template, redirect, flash, session
from flask_cors import CORS
from datetime import timedelta
from services.models import db, User, Log
from forms.signUp import SignUpForm
from forms.login import LoginForm
from forms.edit import EditForm
import os
import uuid as uuid
from PIL import Image
from ML import functionML

##### CONSTANTS #####
PORT = 5000
DB_FILENAME = 'dbfile.db'
INIT_DB = True  

def create_app():
    
    # create flask app
    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(minutes=30)

    # create database extension
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DB_FILENAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']='41e856c5d1833e5d9836c355e738135e'
    db.init_app(app)

    # create flask cors extension
    CORS(app)

    return app, db


# create flask app
app, db = create_app()

# create db file on demand
if INIT_DB:
    db.create_all(app=app)


@app.route("/")
def home():
    
    user_title = session.get('title')
    if user_title == 'admin':
        users=User.getNamesID()
        logsDateFlag= Log.getDateFlagId()
        userName=session.get('name')
        return render_template("home.html", title='Home',user_title=user_title,users=users, logsDateFlag=logsDateFlag, register='Sign Up', logout='logout', userName=userName)
    elif user_title=='user':
        userName=session.get('name')
        return render_template("home.html", title='Home',user_title=user_title, logout='logout', userName=userName)
    else:
        return render_template("home.html",title='Home', login='Login')


    

@app.route('/signUp', methods=['GET','POST'])
def signUp():
    form = SignUpForm()
    print('here1')
    if form.validate_on_submit():
        print('here2')
        imagesList= []
        for image in form.images.data:
            imageName =str(uuid.uuid1())+"_"+image.filename
            image.save(os.path.join('static/images/signUpImgs',imageName))
            imagesList.append(imageName)
        try:
            User.insert(name=form.name.data, user_id=form.user_id.data, password=form.password.data,pic1=imagesList[0],pic2=imagesList[1],pic3=imagesList[2])
        except:
            flash(f'Error: Please register again !', 'danger')
            return redirect("/signUp")
        
        flash(f'Account created for {form.name.data} !', 'success')
        return redirect('/')
    return render_template('registerPage.html',title="signup", logout='logout', form=form)
 

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        print(form.user_id.data,type(form.user_id.data))
        print(form.password.data,type(form.password.data))

        print('here2')
        if form.user_id.data== "1" and form.password.data== "1":
            print('here3')
            session.permanent = True
            session['title'] = 'admin'
            session['user_id'] = 1
            session['name']= 'admin'
            flash(f' login successfully !', 'success')
            return redirect('/')


        try:
           user= User.getByUserId(user_id=form.user_id.data)
        except:
            flash(f'Error: Please login again !', 'danger')
            return redirect("/login")

        image_name=str(uuid.uuid1())+"_"+form.image.data.filename
        form.image.data.save(os.path.join('static/images/loginImgs',image_name))
        
        

        if user==None or user.password != form.password.data :
            print('here4')
            Log.insert(id_entered=form.user_id.data,password_entered=form.password.data, pic=image_name,flag=False,user_id=None )
            flash(f' Wrong data entered !', 'danger')
            return redirect("/login")
        
        

        filename1=user.pic1
        filename2=user.pic2
        filename3=user.pic3
        filename4=image_name

        image1 = Image.open(os.path.join("static/images/signUpImgs",filename1))
        image2 = Image.open(os.path.join("static/images/signUpImgs",filename2))
        image3 = Image.open(os.path.join("static/images/signUpImgs",filename3))
        image4 = Image.open(os.path.join("static/images/loginImgs",image_name))

        if functionML(image4, [image1,image2, image3]): ################### ML function ####################
            
            session.permanent = True
            session['title'] = 'user'
            session['user_id'] = form.user_id.data
            session['name']= User.getByUserId(form.user_id.data).name
            Log.insert(id_entered=form.user_id.data,password_entered=form.password.data, pic=image_name,flag=True, user_id=form.user_id.data)
            flash(f' login successfully !', 'success')
            return redirect('/')
        else:
            Log.insert(id_entered=form.user_id.data,password_entered=form.password.data, pic=image_name,flag=False,user_id=None)
            flash(f' Wrong data entered !', 'danger')
            return redirect("/login")

    return render_template('loginPage.html',title="login",form=form)


@app.route('/logout')
def logout():

    session.clear()
    return redirect("/")

@app.route('/<id>/data')
def user_data(id):

    userData = User.getById(id)
    print(userData)
    return render_template('userdataPage.html',title="data",id=id, userData=userData, logout='logout')

@app.route('/<id>/edit', methods=['GET','POST'] )
def edit_user(id):
    form = EditForm()
    if form.validate_on_submit():
        try:
            User.update(id=id,name=form.name.data, user_id=form.user_id.data, password=form.password.data)
        except:
            flash(f'Error: Please try again!', 'danger')
            return redirect("/")
        
        flash(f'Data updated successfully!', 'success')
        return redirect('/')

    user= User.getById(id)
    form.name.data=user.name
    form.user_id.data=user.user_id

    return render_template('userEditPage.html', title="edit",form=form, logout='logout')

@app.route('/<id>/delete')
def delete_user(id):

    User.delete(id)
    flash(f' deleted successfully ', 'success')
    return redirect('/')    

@app.route('/<id>/view')
def logData(id):

    logData = Log.get(id)
    return render_template('logDataPage.html', title="log",logData=logData, logout='logout')

@app.errorhandler(404)
def error_404(e):
    return render_template("404Page.html"),404

if __name__=='__main__':
    app.run(debug=True,port=PORT)
