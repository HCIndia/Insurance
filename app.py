from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging
from typing import Final
from openpyxl import load_workbook
from pathlib import Path
from flask_cors import CORS
from datetime import datetime



app = Flask(__name__)

"""
Development should be done on this branch.
Later should be merge with the main branch. 
"""

"""
Adding some more spice to it.
Some more spice
this is the last
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///personDetails.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'MyInsAPP'

logging.basicConfig(level=logging.DEBUG)

CORS(app)  # Enable CORS for cross-origin requests
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

@app.route("/")
def start():
    return render_template("StartPage.html")

@app.route("/index",  methods=['GET', 'POST'])
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
    #if request.method == 'POST':
        #get_Person_Detail_by_reg_no = request.form.get("regNo")
    get_Person_Detail_by_reg_no = request.args.get('selected')
    
    full_detail = PersonDetails.query.filter_by(Regd_No=get_Person_Detail_by_reg_no).first()   #exact search command 

    return render_template("FullPersonDetails.html", full_detail= full_detail)


@app.route("/searchByMonth", methods=['GET', 'POST'])
def searchByMonth():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form  # Handles form submissions

        app.logger.info(f"Received Data: {data}")

        month_name = data.get("month")
        if not month_name:
            return render_template("SearchByMonth.html", error="Month is required")

        try:
            month_number = datetime.strptime(month_name, "%B").month
            app.logger.info(f"Converted Month Name '{month_name}' to Number: {month_number}")
        except ValueError:
            return render_template("SearchByMonth.html", error="Invalid month name")

        results = PersonDetails.query.filter(
            db.extract('month', PersonDetails.Date_of_insurance) == month_number
        ).all()

        app.logger.info(f"Query Results: {results}")

        if not results:
            return render_template("SearchByMonth.html", error="No records found for this month")

        reg_list = [res.Regd_No for res in results]
        app.logger.info(f"Extracted Registration Numbers: {reg_list}")
        return render_template("SearchByMonth.html", result=results)

    return render_template("SearchByMonth.html")

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
    
    folder_path = Path("/Users/sukant/Documents/Python_Workspace/Python_Flask/Insurance/DataFiles")  
    #folder_path = Path("/home/Sukant/basic/DataFiles")

    xl_file = [str(file) for file in folder_path.glob("*.xlsx")]

    for file in xl_file:

        wb = load_workbook(file)
        ws = wb.active  # Select the active sheet

        # Iterate through rows (values only)
        for row in ws.iter_rows(min_row=3, values_only=True):
            row_data = row[:5] + row[6:] 
            if any(row_data):  # Checks if the row has at least one non-empty cell

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
        
        #db.drop_all()
        db.create_all()
        app.run(debug=True)


