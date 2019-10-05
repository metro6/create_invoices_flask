import io
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, Response, send_file
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from docx import *
from docx.shared import Inches

from app import app, db

from .forms import LoginForm, RegistrationForm, CreateFormForm, EditFormForm
from .models import Invoice, User



@app.route('/')
@app.route('/index')
@login_required
def index():
    invoices = Invoice.query.all()
    return render_template('index.html',
                           title='Список форм',
                           invoices=invoices)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Учетные данные введены неверно')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегестрировались')
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Регистрация',
                           form=form)



@app.route('/invoice/<invoice_id>', methods=['GET', 'POST'])
@login_required
def invoice(invoice_id):
    invoice = Invoice.query.filter_by(id=invoice_id).first_or_404()
    title = invoice.name
    form = EditFormForm()
    if form.validate_on_submit():
        invoice.name = form.name.data
        db.session.add(invoice)
        db.session.commit()
    elif request.method == 'GET':
        form.name.data = invoice.name
    return render_template('invoice.html',
                           title=title,
                           invoice=invoice,
                           form=form)


@app.route('/create_form', methods=['GET', 'POST'])
@login_required
def create_form():
    form = CreateFormForm()
    title = 'Создание новой формы'
    if form.validate_on_submit():
        invoice = Invoice(name=form.name.data)
        db.session.add(invoice)
        db.session.commit()
        flash('Новая форма успешно создана')
        return redirect(url_for('index'))
    return render_template('create_form.html',
                           title=title,
                           form=form)

@app.route('/get_invoice_word')
def get_invoice_word():
    invoice = Invoice.query.filter_by(id=request.args['id']).first_or_404()
    full_text = request.args['full'] == 'true'
    short_text = request.args['short'] == 'true'

    file_stream = io.BytesIO()

    document = Document()
    document.add_heading(invoice.name, 0)
    document.add_paragraph('Дата создания документа ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    document.add_page_break()
    document.save(file_stream)

    file_stream.seek(0)

    return send_file(file_stream, as_attachment=True, attachment_filename='report_.docx')