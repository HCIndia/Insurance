from app import db
from datetime import datetime
from dataclasses import dataclass


class PersonDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date_of_insurance = db.Column(db.String(40))
    Customer_name = db.Column(db.String(40))
    Model = db.Column(db.String(40), nullable=False)
    Year_of_mfg = db.Column(db.String(120))
    Regd_No = db.Column(db.String(120))

'''
@dataclass
class PersonDetails(db.Model):
    id:str
    Date_of_insurance,
    Customer_name,
    Model,
    Year_of_mfg,
    Regd_No,
    Old_ID_value,
    New_ID_value,
    Old_OD_value,
    New_OD_value,
    Old_final_premium,
    New_final_premium,
    Ncb,
    Discount,
    Terms,
    Insured_Company,
    New_Company,
    Policy_No,
    Contact_remarks,
    Transfer_to

    
    id = db.Column(db.Integer,primary_key=True)
    Date_of_insurance = db.Column(db.DateTime,nullable=False)
    Customer_name = db.Column(db.String(30),nullable=False, default=True)
    Model = db.Column(db.String(30),nullable=False)
    Year_of_mfg = db.Column(db.Integer,nullable=False)
    Regd_No = db.Column(db.String(30),nullable=False)
    Old_ID_value = db.Column(db.String(30),nullable=False)
    New_ID_value = db.Column(db.String(30),nullable=False)
    Old_OD_value = db.Column(db.String(30),nullable=False)
    New_OD_value = db.Column(db.String(30),nullable=False)
    Old_final_premium = db.Column(db.String(30),nullable=False)
    New_final_premium = db.Column(db.String(30),nullable=False)
    Ncb = db.Column(db.String(30),nullable=False)
    Discount = db.Column(db.String(30),nullable=False)
    Terms = db.Column(db.String(30),nullable=False)
    Insured_Company = db.Column(db.String(30),nullable=False)
    New_Company = db.Column(db.String(30),nullable=False)
    Policy_No = db.Column(db.String(30),nullable=False)
    Contact_remarks = db.Column(db.String(100),nullable=False)
    Transfer_to = db.Column(db.String(30),nullable=False)'''