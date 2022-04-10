
from asyncio.windows_events import NULL
from fileinput import filename
from io import BytesIO
from unicodedata import category
from flask import Blueprint, render_template, request, flash, send_file
from flask_login import  login_required, current_user

from .models import Upload
from . import db
views = Blueprint('views',__name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        file = request.files['file']
        downNum = request.form.get('note')
        downId = request.form.get('downId')
        uNum = Upload.query.filter_by(downId=downNum).first()
        if len(downNum) == 0:
            flash('Please enter 6 numbers ', category='error')
        elif len(downNum) < 6:
            flash('numbers to short, enter 6 please', category='error')
        elif len(downNum) > 6:
            flash('numbers to long, please enter 6 only!', category='error')
        elif uNum:
            flash('this unique digits is taken, please enter a new one', category='error')
        else:
            upload = Upload(filename=file.filename, data=file.read(), user_id=current_user.id, downId = downNum )
            if not file.filename:
                flash('please upload a file first', category='error')
            else:
                print(file.filename)
                db.session.add(upload)
                db.session.commit() 
                flash(f'Uploaded: {file.filename} , File number for download : {downNum}' , category='success')
    return render_template('home.html', user=current_user) 

@views.route('/downloads')
def downloads():
    return render_template('download.html', user=current_user)

@views.route('/downloads/<upload_id>')
@login_required
def download(upload_id):
    upload = Upload.query.filter_by(downId=upload_id).first()
    file = send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)
    return file 
