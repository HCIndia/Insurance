from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging
from typing import Final
from openpyxl import load_workbook


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///personDetails.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'MyInsAPP'
'''app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://Sukant:Macbook_2020@Sukant.mysql.pythonanywhere-services.com/Sukant$personDetails'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False'''
db = SQLAlchemy(app)


class PersonDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date_of_insurance = db.Column(db.String(40))
    Customer_name = db.Column(db.String(40))
    Make = db.Column(db.String(40))
    Model = db.Column(db.String(40), nullable=False)
    Year_of_mfg = db.Column(db.String(120))
    Regd_No = db.Column(db.String(120))
    Old_ID_value = db.Column(db.String(120))
    New_ID_value = db.Column(db.String(120))
    Old_OD_value = db.Column(db.String(120))
    New_OD_value = db.Column(db.String(120))
    Old_final_premium = db.Column(db.String(120))
    New_final_premium = db.Column(db.String(120))
    Ncb = db.Column(db.String(120))
    Discount = db.Column(db.String(120))
    Terms_Comp = db.Column(db.String(120))
    Terms_TP = db.Column(db.String(120))
    Insured_Company = db.Column(db.String(120))
    New_Company = db.Column(db.String(120))
    Policy_No = db.Column(db.String(120))
    Contact_remarks = db.Column(db.String(120))
    Transfer_to = db.Column(db.String(120))



@app.route("/",  methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_Person_Detail_by_reg = request.form.get("searchPersonDet")
        if (search_Person_Detail_by_reg):
            app.logger.info(f"Got the data from form action :{search_Person_Detail_by_reg}")
        #person_object = PersonDetails.query.filter_by(Regd_No=search_Person_Detail_by_reg).first()   #exact search command 
            person_object = PersonDetails.query.filter(PersonDetails.Regd_No.ilike(f'%{search_Person_Detail_by_reg}%')).all()  # this is partial search
        
        if not person_object and search_Person_Detail_by_reg :
            person_object = PersonDetails.query.filter(PersonDetails.Customer_name.ilike(f'%{search_Person_Detail_by_reg}%')).all()

        if not person_object or not search_Person_Detail_by_reg :
            flash("No Records Found", "info")

        return render_template("index.html",person_object= person_object)

    return render_template("index.html")

@app.route("/fullPersonDetails", methods=['GET', 'POST'])
def fullPersonDetails():
    if request.method == 'POST':
        get_Person_Detail_by_reg_no = request.form.get("regNo")
       
        full_detail = PersonDetails.query.filter_by(Regd_No=get_Person_Detail_by_reg_no).first()   #exact search command 

    return render_template("FullPersonDetails.html", full_detail= full_detail)


@app.route("/addPerson")
def addPerson():
    return render_template("AddPerson.html")

@app.route("/successPage", methods=['GET', 'POST'])
def SuccessPage():
    '''Here we will first chekc if the the same car number is alreday registered.
    if it already registered, display already added
    if new car then dispaly a message that you data is saved in db
    and a click bar to goto index/search page
    db operations 
    1.search , 2.save/commit''' 
    if request.method == 'POST':
        date_of_insurance = request.form.get("date_of_insurance")
        customer_name = request.form.get("customer_name")
        make = request.form.get("make")
        model = request.form.get("model")
        year_of_mfg = request.form.get("year_of_mfg")
        registration_no = request.form.get("registration_no")
        old_id_value = request.form.get("old_id_value")
        new_id_value = request.form.get("new_id_value")
        old_od_value = request.form.get("old_od_value")
        new_od_value = request.form.get("new_od_value")
        old_final_premium = request.form.get("old_final_premium")
        new_final_premium = request.form.get("new_final_premium")
        ncb = request.form.get("ncb")
        discount = request.form.get("discount")
        terms_comp = request.form.get("terms_comp")
        terms_tp = request.form.get("terms_tp")
        insured_company = request.form.get("insured_company")
        new_company = request.form.get("new_company")
        policy_no = request.form.get("policy_no")
        contact_remarks = request.form.get("contact_remarks")
        transfer_to = request.form.get("transfer_to")

        insert_person = PersonDetails(Date_of_insurance=date_of_insurance,
                                    Customer_name = customer_name,Make=make, Model = model, Year_of_mfg = year_of_mfg,
                                    Regd_No= registration_no, Old_ID_value = old_id_value,New_ID_value= new_id_value
                                    ,Old_OD_value=old_od_value, New_OD_value=new_od_value,
                                     Old_final_premium=old_final_premium,New_final_premium=new_final_premium,Ncb=ncb,
                                     Discount=discount,Terms_Comp=terms_comp, Terms_TP = terms_tp, Insured_Company=insured_company,
                                     New_Company=new_company,Policy_No=policy_no, Contact_remarks=contact_remarks,Transfer_to=transfer_to)
        
        db.session.add(insert_person)
        app.logger.info("One Person is Succesfully added in Database")
        db.session.commit()
        app.logger.info("Changes have been comitted")

    return render_template("Success.html")
    


@app.route("/loadData")
def loadData():
    file_path : Final = "InsuranceData_Test.xlsx"
    wb = load_workbook(file_path)
    sheet = wb.active

    for i in range(3,16):
        row_data = [cell.value for idx, cell in enumerate(sheet[i], start=1) if idx != 6]  # sheet[3] gets all cells in row 3

        insert_person = PersonDetails(Date_of_insurance=row_data[0],
                                    Customer_name = row_data[1],Make=row_data[2], Model = row_data[3], Year_of_mfg = row_data[4],
                                    Regd_No= row_data[5], Old_ID_value = row_data[6],New_ID_value= row_data[7]
                                    ,Old_OD_value=row_data[8], New_OD_value=row_data[9],
                                        Old_final_premium=row_data[10],New_final_premium=row_data[11],Ncb=row_data[12],
                                        Discount=row_data[13],Terms_Comp=row_data[14],Terms_TP=row_data[15], Insured_Company=row_data[16],
                                        New_Company=row_data[17],Policy_No=row_data[18], Contact_remarks=row_data[19],
                                        Transfer_to=row_data[20])
        #BR01BB2649
        db.session.add(insert_person)
        app.logger.info("Person is Succesfully added in Database")
        db.session.commit()
        app.logger.info("Changes have been comitted")

    return "Data is succesfully uploaded"


if __name__ == "__main__":
    with app.app_context():
        
        db.drop_all()
        db.create_all()
        app.run()
