from flask import render_template, request, redirect, session, flash
from config import app, db, bcrypt
from models import User, Address, Schedule
from datetime import date, time
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index():
    print("*"*40)
    return render_template("index.html")

def about():
    return render_template("about_us.html")

def price():
    return render_template("pricing.html")

def add_user():
    if len(request.form['fname'])<2:
        flash("First name is required")
    if len(request.form['lname'])<2:
        flash("Last name is required")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Valid email is required")   
    if len(request.form['address'])<2:
        flash("Address is required")
    if len(request.form['city'])<2:
        flash("City must be at least 2 characters")
    if len(request.form['state'])<2:
        flash("State initials required, 2 characters")
    if len(request.form['password']) < 5:
        flash("password isn't long enough")
    if request.form['password'] != request.form['cpassword']:
        flash("password dont match")
    if '_flashes' not in session:
        new_user = User(
            first_name = request.form['fname'],
            last_name = request.form['lname'],
            email = request.form['email'],
            password_hash=bcrypt.generate_password_hash(request.form['password']))   
        db.session.add(new_user)
        db.session.commit()
        flash("Successfully added user")
        new_address = Address(
            user_id = new_user.id,
            address=request.form['address'], 
            city=request.form['city'],
            state = request.form['state']) 
        db.session.add(new_address)
        db.session.commit()
        flash("Address added")
        return redirect("/")
    return redirect('/')   
        

def login():
    is_valid = True
    if len(request.form['email']) < 1:
        is_valid = False
        flash("Email is required")
    if len(request.form['password']) < 1:
        is_valid = False
        flash("Password is required")

    if is_valid:
        user = User.query.filter_by(email=request.form['email']).all()
        if user:
            if bcrypt.check_password_hash(user[0].password_hash, request.form['password']):
                session['user_id'] = user[0].id
                return redirect("/user_page")
            else:
                flash("Email and/or password do not match")
        else:
                flash("Email and/or password do not match")
    return redirect("/")


def user_page():
    if 'user_id' not in session:
        return redirect("/")
    cur_user = User.query.filter_by(id=session['user_id'])
    cur_address = Address.query.filter_by(user_id = session['user_id'])
    cur_history = Schedule.query.filter_by(user_id= session['user_id'])
    return render_template("user_page.html", all_users = cur_user, all_addresses = cur_address, all_schedules = cur_history)

def schedule():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("schedule.html")


def process_schedule():
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['date']) < 1:
        is_valid = False
        flash("Date is required")
    if len(request.form['time']) < 1:
        is_valid = False
        flash("Time is required")
    if len(request.form['box']) < 1:
        is_valid = False
        flash("Please select if you'd like us to breakdown boxes")
    if len(request.form['phone']) < 10:
        is_valid = False
        flash("Phone number is required")
    if is_valid:
        cur_user = User.query.filter_by(id=session['user_id']).all()
        user_address = Address.query.filter_by(user_id = session['user_id']).all()
        if user_address:
            session['address_id'] = user_address[0].id
            new_pickup = Schedule(
                date = request.form['date'],
                time = request.form['time'],
                option = request.form['box'],
                phone = request.form['phone'],
                user_id = session['user_id'],
                address_id = session['address_id'])
            db.session.add(new_pickup)
            db.session.commit()
            flash("Successfully scheduled")
            session['schedule_id'] = new_pickup.id
            return redirect("/confirmation")
        return redirect("/schedule")
    return redirect("/schedule")

def confirm():
    if 'user_id' not in session:
        return redirect("/")
    cur_user = User.query.filter_by(id=session['user_id']).all()
    cur_address = Address.query.filter_by(user_id = session['user_id']).all()
    pickup = Schedule.query.filter_by(id = session['schedule_id']).all()
    return render_template("confirmation.html", all_users = cur_user, all_addresses = cur_address, all_schedules = pickup)


def delete_pickup(schedule_id):
    if 'user_id' not in session:
        return redirect("/")
    this_pickup = Schedule.query.filter_by(id = int(schedule_id)).first()
    if this_pickup is not None:
        db.session.delete(this_pickup)
        db.session.commit()
        flash("Successfully cancelled")
        return redirect("/confirmation")


def edit_pickup():
    if 'user_id' not in session:
        return redirect("/")
    this_pickup = Schedule.query.filter_by(id = session['schedule_id']).all()
    return render_template("edit_schedule.html", all_schedules = this_pickup )
    
def update_pickup(schedule_id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['date']) < 1:
        is_valid = False
        flash("Date is required")
    if len(request.form['time']) < 1:
        is_valid = False
        flash("Time is required")
    if len(request.form['box']) < 1:
        is_valid = False
        flash("Please select if you'd like us to breakdown boxes")
    if len(request.form['phone']) < 10:
        is_valid = False
        flash("Phone number is required")
    if is_valid:
        this_pickup = Schedule.query.filter_by(id = int(schedule_id)).first()
        if this_pickup is not None:
            this_pickup.date = request.form['date']
            this_pickup.time = request.form['time']
            this_pickup.option = request.form['box']
            this_pickup.phone = request.form['phone']
            db.session.commit()
            return redirect("/confirmation")
        return redirect("/confirmation")
    return redirect ("/edit/schedule")
    

def edit_address():
    if 'user_id' not in session:
        return redirect("/")
    this_address = Address.query.filter_by(id = session['address_id']).all()
    return render_template("edit_address.html", all_addresses = this_address)
    
def update_address(address_id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['address'])<2:
        is_valid = False
        flash("Address is required")
    if len(request.form['city'])<2:
        is_valid = False
        flash("City must be at least 2 characters")
    if len(request.form['state'])<2:
        is_valid = False
        flash("State initials required, 2 characters")      
    if is_valid:    
        this_address = Address.query.filter_by(id = int(address_id)).first()
        if this_address is not None:
            this_address.address = request.form['address']
            this_address.city = request.form['city']
            this_address.state = request.form['state']
            db.session.commit()
            return redirect("/user_page") 
        return redirect("/")
    return redirect("/edit/address")

def edit_user():
    if 'user_id' not in session:
        return redirect("/")
    this_user = User.query.filter_by(id = session['user_id']).all()
    return render_template("edit_user.html", all_users = this_user)
    
    
def update_user(user_id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['fname'])<2:
        is_valid = False
        flash("First name is required")
    if len(request.form['lname'])<2:
        is_valid = False
        flash("Last name is required")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Valid email is required")
    if is_valid:   
        this_user = User.query.filter_by(id = int(user_id)).first()
        if this_user is not None:
            this_user.first_name = request.form['fname']
            this_user.last_name = request.form['lname']
            this_user.email = request.form['email']
            db.session.commit()
            return redirect("/confirmation")
        return redirect("/")
    return redirect("/edit/user")  
        
    

def logout():
    session.clear()
    return redirect("/")



