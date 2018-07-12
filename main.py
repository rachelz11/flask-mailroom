import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)
#app.secret_key = b'>\xf1\xc1\x0c\x00fa\x9a\xb6\xbe=P\xbe\xbb\\\x9b\x80\x11\x85\xd2z\xcd.\x19'
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('create.jinja2')
    if request.method == "POST":
        donor_name = request.form['name']
        amount = int(request.form['amount'])
        try:
            donor = Donor.get(Donor.name == donor_name)
        except Donor.DoesNotExist:
            donor = Donor(name=donor_name)
            donor.save()
        donation = Donation(value=amount, donor=donor)
        donation.save()
        return redirect(url_for('home'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
