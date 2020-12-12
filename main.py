from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import json
import api

with open("info.json", "r") as c:
    parameters = json.load(c)["parameters"]


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = parameters["database"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parameters["track_modifications"]
app.config['SECRET_KEY'] = parameters["secret_key"]


login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)

class Hospital(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_no = db.Column(db.String(10), nullable=False)
    hospital_pass = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return self.hospital_no + ' : ' + self.hospital_pass
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    adhar_no = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return self.name + ' : ' + self.adhar_no


class Vaccine_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vaccine_id = db.Column(db.String(10), nullable=False)
    company_details = db.Column(db.String(10), nullable=False)
    batch_details = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.vaccine_id + " " + self.company_details

class Vaccinated_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    adhar_no = db.Column(db.String(20), nullable=False)
    vaccine_id = db.Column(db.String(10), nullable=False)
    company_details = db.Column(db.String(10), nullable=False)
    batch_details = db.Column(db.String(100), nullable=False)
    hospital_no = db.Column(db.String(10), nullable=False)
    hospital_pass = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return self.name + " by " + self.vaccine_id



@login_manager.user_loader
def load_user(id):
    return Hospital.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        adhar_no = request.form.get('adhar_no')
        pos_vaccinated = Vaccinated_info.query.filter_by(adhar_no=adhar_no).all()
        for i in pos_vaccinated:
            if i.adhar_no== adhar_no and i.name and i.vaccine_id and i.hospital_no:
                return render_template('index.html', msg = "You were Vaccinated")
        else:
            return render_template('index.html', msg = "You are not Vaccinated")
    return render_template('index.html')


@app.route('/ent', methods=['GET', 'POST'])
def ent():
    all_users = User.query.all()
    if request.method == 'POST':
        user = User(name = request.form.get('name'), dob = request.form.get('dob'), adhar_no = request.form.get('adhar_no'))
        db.session.add(user)
        db.session.commit()
    return render_template('ent.html', all_users = all_users)


@app.route('/hospital', methods=['GET', 'POST'])
def hospital():
    if request.method == 'POST':
        hospital_no = request.form.get('hospital_no')
        hospital_pass = request.form.get('hospital_pass')
        pos_hospital = Hospital.query.filter_by(hospital_no=hospital_no).all()
        for i in pos_hospital:
            if i.hospital_no == hospital_no and i.hospital_pass == hospital_pass:
                hospital = Hospital.query.get(i.id)
                load_user(hospital.id)
                login_user(hospital)
                return redirect(url_for('vaccine'))
            else:
                return render_template('index.html', msg = "Invalid identifier")


@app.route('/vaccine', methods=['GET', 'POST'])
@login_required
def vaccine():
    if request.method == 'POST':

        adhar_no = request.form.get('adhar_no')
        dob = request.form.get('dob')
        vaccine_id = request.form.get('vaccine_id')
        batch_details = request.form.get('batch_details')

        pos_users = User.query.filter_by(adhar_no=adhar_no).all()
        for i in pos_users:
            if i.dob == dob and i.adhar_no == adhar_no:
                user = User.query.get(i.id)
            else:
                return render_template('vacc.html',  msg = "Enter valid Adhar Details")

        pos_vaccine = Vaccine_info.query.filter_by(vaccine_id = vaccine_id).all()
        for j in pos_vaccine:
            if j.vaccine_id == vaccine_id and j.batch_details == batch_details:
                vac = Vaccine_info.query.get(j.id)
            else:
                return render_template('vacc.html', msg = "Enter valid vaccine details")

        pos_vaccinated = Vaccinated_info.query.filter_by(adhar_no=adhar_no).all()
        for k in pos_vaccinated:
            if k.dob == dob and k.adhar_no == adhar_no:
                return render_template('vacc.html', msg = "You are alerdy Vaccinated")

        if vac and user:
            new_vac = Vaccinated_info(name = user.name, dob = user.dob, adhar_no = user.adhar_no, vaccine_id = vac.vaccine_id, company_details = vac.company_details, batch_details = vac.batch_details, hospital_no = current_user.hospital_no, hospital_pass = current_user.hospital_pass)
            db.session.add(new_vac)
            db.session.commit()
            return render_template('vacc.html', msg = "You were Vaccinated succesfully")  
        else:
            return render_template('vacc.html', msg = "Some details are wrong")      
    
    return render_template('vacc.html')


if __name__ == '__main__':
    app.run(debug=True)

