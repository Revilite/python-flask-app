from flask import Blueprint as bp
from flask import render_template as rt
from flask import request as req
from flask import flash, jsonify
from .models import Note
from flask_login import login_required as lir
from flask_login import current_user as cu
from . import db
import json

views = bp("views", __name__)

@views.route("/", methods=["GET", "POST"])
@lir
def home():
  if req.method == 'POST':
        note = req.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=cu.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')


  return rt("home.html", user=cu)


@views.route("/delete-note", methods=["POST"])
def delete_note():
  note = json.loads(req.data)
  noteId = note["noteId"]
  note = Note.query.get(noteId)
  if note:
    if note.user_id == cu.id:
      db.session.delete(note)
      db.session.commit()
  return jsonify({})