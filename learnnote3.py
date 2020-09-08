from flask import Flask, request
import sys
import os
try:
    import config_override as config
except ImportError:
    import config_default as config
from exts import db
from models import Label, LearnNote, FileNumber, Picture
import logging
import json
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/sync2server/', methods=['POST'])
def sync2Server():
    learnnotelist= getLearnNote2SyncList()
    filenumberlist= getFileNumber2SyncList()
    if not learnnotelist or filenumberlist:
        return json.dumps({
            "errorcode": 1, 
            "message": "同步冲突！",
            "learnnotelist":learnnotelist,
            "filenumberlist":filenumberlist
            })
    FileNumberRecords = json.loads(request.form.get("FileNumberRecords", None))
    for FileNumberRecord in FileNumberRecords:
        FileNumber.query.filter(FileNumber.id_problem== FileNumberRecord.id_problem).delete()
    for FileNumberRecord in FileNumberRecords:
        filenumber = FileNumber(
            id_problem= FileNumberRecord.id_problem,
            filenumber= FileNumberRecord.filenumber,
            filetitle=FileNumberRecord.filetitle,
            recordtime=FileNumberRecord.recordtime,
            active=FileNumberRecord.active,
            sync=1,
            )
        db.session.add(filenumber)
        db.session.commit()
    LearnNoteRecords = json.loads(request.form.get("LearnNoteRecords", None))
    for LearnNoteRecord in LearnNoteRecords:
        LearnNote.query.filter(LearnNote.id_problem== LearnNoteRecord.id_problem).delete()
        Picture.query.filter(Picture.id_problem== LearnNoteRecord.id_problem).delete()
    for LearnNoteRecord in LearnNoteRecords:
        learnnote = LearnNote(
            id_problem= LearnNoteRecord.id_problem,
            d_level= LearnNoteRecord.d_level,
            source=LearnNoteRecord.source,
            notes=LearnNoteRecord.notes,
            answer=LearnNoteRecord.answer,
            usedtime=LearnNoteRecord.usedtime,
            usedtimes=LearnNoteRecord.usedtimes,
            inputdate=LearnNoteRecord.inputdate,
            active=FileNumberRecord.active,
            sync=1,
            )
        db.session.add(learnnote)
        db.session.commit()
        for PictureRecord in FileNumberRecord.PictureRecords:
            picture = Picture(
                id_problem= PictureRecord.id_problem,
                filepath= PictureRecord.filepath,
                isanswer= PictureRecord.isanswer,
            )
            db.session.add(picture)
            db.session.commit()
    return json.dumps({"errorcode": 0, "message": "已同步！"})
def getFileNumber2SyncList():
    filenumbers= FileNumber.query.filter(FileNumber.sync==0).all()
    FileNumberDict ={}
    List=[]
    if not filenumbers: return []
    for fn in filenumbers:
        FileNumberDict ={
            "id":fn.id,
            "id_problem":fn.id_problem,
            "filenumber":fn.filenumber,
            "filetitle":fn.filetitle,
            "recordtime":fn.recordtime,
            "sync":fn.sync,
            "active":fn.active
        }
        List.append(FileNumberDict)
    return List
def getLearnNote2SyncList():
    learnnotes= LearnNote.query.filter(LearnNote.sync==0).all()
    LearnNoteDict ={}
    List=[]
    if not learnnotes: return []
    for n in learnnotes:
        List1=[]
        PictureDict={}
        for p in n.pictures:
            PictureDict={
                "id":p.id,
                "id_problem":p.id_problem,
                "filepath":p.filepath,
                "isanswer":p.isanswer
            }
            List1.append(PictureDict)
        LearnNoteDict ={
            "id_problem":n.id_problem,
            "d_level":n.d_level,
            "source":n.source,
            "notes":n.notes,
            "answer":n.answer,
            "usedtime":n.usedtime,
            "usedtimes":n.usedtimes,
            "inputdate":n.inputdate,
            "sync":n.sync,
            "active":n.active,
            "pictures":List1
        }
        List.append(LearnNoteDict)
    return List
app.debug = True
handler = logging.FileHandler(config.LOG_FILE_FULL_PATH, encoding='UTF-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
    pass


