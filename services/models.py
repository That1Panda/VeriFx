from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable=False)
    name=db.Column(db.String(100), nullable=False )
    user_id=db.Column(db.Integer, unique=True, nullable=False)
    password=db.Column(db.String(100), nullable=False)
    pic1=db.Column(db.Text,nullable=False)
    pic2=db.Column(db.Text,nullable=False)
    pic3=db.Column(db.Text,nullable=False)
    created_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    logs=db.relationship('Log', backref='user', lazy=True)

    def __init__(self, name, user_id, password, pic1, pic2, pic3):
        self.name= name
        self.user_id = user_id
        self.password = password
        self.pic1=pic1
        self.pic2=pic2
        self.pic3=pic3

    def __repr__(self):
        return f"<User({self.id}, {self.name}, {self.user_id}, {self.password}>"

    @classmethod
    def insert(self, name, user_id, password, pic1, pic2, pic3):

        user = User(name=name, user_id=user_id, password=password, pic1=pic1, pic2=pic2, pic3=pic3)

        db.session.add(user)
        db.session.commit()

    @classmethod
    def update(self, id, name, user_id, password):

        query = self.query.filter_by(id=id).first()

        query.name= name
        query.user_id = user_id
        query.password = password

        db.session.commit()

    @classmethod
    def getByUserId(self, user_id):

        query = self.query.filter_by(user_id=user_id).first()
        return query

    @classmethod
    def getById(self, id):

        query = self.query.filter_by(id=id).first()
        print("dB")
        print(query)
        return query

    @classmethod
    def delete(self,id):

        user=self.query.get(id)
        db.session.delete(user)
        db.session.commit()

    @classmethod
    def getNamesID(self):

        users1=db.session.query(User.name,User.id).all()
        users3=[]
        for i in users1:
            users2=[i.name,i.id]
            users3.append(users2)
        return users3

class Log(db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable=False)
    id_entered=db.Column(db.Integer, nullable=False)
    password_entered=db.Column(db.String(100), nullable=False)
    pic=db.Column(db.Text,nullable=False)
    flag=db.Column(db.Boolean,default=False, nullable=False)
    created_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id= db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, id_entered, password_entered, pic, flag, user_id):
        self.id_entered= id_entered
        self.password_entered = password_entered
        self.pic=pic
        self.flag=flag
        self.user_id=user_id

    def __repr__(self):
        return f"<Log({self.id}, {self.id_entered}, {self.password_entered}, {self.pic}, {self.flag} )>"

    @classmethod
    def insert(self, id_entered, password_entered, pic, flag, user_id):

        log=Log(id_entered=id_entered, password_entered=password_entered, pic=pic, flag=flag, user_id=user_id)

        db.session.add(log)
        db.session.commit()

    @classmethod
    def get(self,id):

        log=self.query.get(id)
        return log

    @classmethod
    def delete(self,id):

        log=self.query.get(id)
        db.session.delete(log)
        db.session.commit()

    @classmethod
    def getDateFlagId(self):

        dateFlagId1=db.session.query(Log.created_date, Log.flag, Log.id).all()
        dateFlagId2=[]
        dateFlagId3=[]
        for i in dateFlagId1:
            dateFlagId3=[i.created_date,i.flag, i.id]
            dateFlagId2.append(dateFlagId3)

        return dateFlagId2
