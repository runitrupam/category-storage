from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Prod(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    sub = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/",methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        #print(request.form['title'])
        title = request.form['title']
        sub = request.form['sub']  
        category = request.form['category']  
        t1 = Prod(title = title,sub = sub , category = category)
        db.session.add(t1)
        db.session.commit()
    allProd = Prod.query.all()
    return render_template("index.html",allProd = allProd)

@app.route("/update/<int:sno>",methods = ['POST','GET'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        sub = request.form['sub']  
        category = request.form['category']  
        prod = Prod.query.filter_by(sno=sno).first()
        prod.title = title
        prod.sub = sub
        prod.category = category
        db.session.add(prod)
        db.session.commit()
        return redirect("/")
    prod = Prod.query.filter_by(sno=sno).first()
    return render_template("update.html",prod = prod)


@app.route('/delete/<int:sno>')
def delete(sno):
    prod = Prod.query.filter_by(sno=sno).first()
    db.session.delete(prod)
    db.session.commit()
    return redirect("/")

@app.route("/show")
def products():
    allProd = Prod.query.all()
    print(allProd)
    return 'this is products page'

if __name__ == "__main__":
    app.run(debug=True, port = 8000)



