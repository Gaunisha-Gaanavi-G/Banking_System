import uuid 
from datetime import date
from flask import *
from model.model import Bank;

app=Flask(__name__)
app.secret_key = "abc"

@app.route("/",methods = ["POST","GET"])
def Home():
    return render_template("home.html")

@app.route("/view_customers",methods=["POST","GET"])
def View_Customers():
    if request.method=="GET":
        b=Bank()
        data=b.get_customers()
        return render_template("view_customers.html",data=data)

@app.route('/transfer/<id>',methods=["POST","GET"])
def Transfer(id):
    b=Bank()
    data=b.get_customers_info(id)
    all_data=b.get_customers()
    return render_template("transfer.html",data=data,all_data=all_data,id=id)

@app.route("/transfer_direct/<id>",methods=["POST","GET"])
def Transfer_direct(id):
    trans_id = uuid.uuid4().hex
    b=Bank()
    data=b.get_customers_info(id)
    all_data=b.get_customers()
    receiver_info=b.get_receiver_info(request.form['account_no'])
    data_insert={
        'Trans_id': trans_id,
        'Sender_name': data['Name'],
        'Receiver_name': request.form['name'],
        'Transfered_amount': request.form['amount'],
        'Sender_account' : data['Account_number'],
        'Receiver_account' : receiver_info['Account_number'],
        'Date' : date.today(),
        'Message':request.form['msg']
    }
    b.insert_into_transaction(data_insert)
    current_bal_sender = data['Balance']
    current_bal_receiver = receiver_info['Balance']
    current_bal_sender-=int(request.form['amount'])
    current_bal_receiver +=int(request.form['amount'])
    receiver_id=receiver_info['Customer_Id']
    b.update_customers(current_bal_sender,current_bal_receiver,id,receiver_id)
    flash("Transaction successfull")
    data=b.get_customers_info(id)
    return render_template('transfer.html',data=data,all_data=all_data,id=id)

@app.route("/history",methods=["POST","GET"])
def History():
    if request.method=="GET":
        b=Bank()
        data=b.get_history()
        return render_template("history.html",data=data)

@app.route("/new_transfer",methods=["POST","GET"])
def New_transfer():
    b=Bank()
    trans_id = uuid.uuid4().hex
    all_data=b.get_customers()
    if request.method=="GET":
        return render_template("new_transfer.html",all_data=all_data)
    if request.method=="POST":
        data_insert={
            'Trans_id':trans_id,
            'Sender_name':request.form['sender_name'],
            'Receiver_name' : request.form['receiver_name'],
            'Sender_account' : request.form['sender_account'],
            'Receiver_account' : request.form['receiver_account'],
            'Transfered_amount' : request.form['amount'],
            'Message' : request.form['msg'],
            'Date': date.today()
        }
        b.insert_into_transaction(data_insert)
        data_sender=b.get_receiver_info(request.form['sender_account'])
        data_receiver = b.get_receiver_info(request.form['receiver_account'])
        current_bal_sender = data_sender['Balance']
        current_bal_receiver = data_receiver['Balance']
        current_bal_sender-=int(request.form['amount'])
        current_bal_receiver +=int(request.form['amount'])
        receiver_id=data_receiver['Customer_Id']
        sender_id=data_sender['Customer_Id']
        b.update_customers(current_bal_sender,current_bal_receiver,sender_id,receiver_id)
        flash("Transaction successfull")
        data=b.get_customers_info(id)
        return render_template('new_transfer.html',all_data=all_data)

        

        

if __name__=="__main__":
    app.run(debug=True)