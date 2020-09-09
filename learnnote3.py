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
import datetime
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

class DateEncoder(json.JSONEncoder): #重写json序列化类以解决datetime类型的数据不能被json的错误
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

@app.route('/sync2server/', methods=['POST','GET'])
def sync2Server():
    learnnotelist= getLearnNote2SyncList()
    filenumberlist= getFileNumber2SyncList()
    if learnnotelist or filenumberlist:
        return json.dumps({
            "errorcode": 1, 
            "message": "同步冲突！",
            "learnnotelist":learnnotelist,
            "filenumberlist":filenumberlist
            },cls=DateEncoder)

    RequestDict = json.loads(request.get_data())
    FileNumberRecords = RequestDict["FileNumberRecords"]if "FileNumberRecords" in RequestDict else []
    for FileNumberRecord in FileNumberRecords:
        FileNumber.query.filter(FileNumber.id_problem== FileNumberRecord['id_problem']).delete()
    for FileNumberRecord in FileNumberRecords:
        filenumber = FileNumber(
            id_problem= FileNumberRecord['id_problem'],
            filenumber= FileNumberRecord['filenumber'],
            filetitle=FileNumberRecord['filetitle'],
            recordtime=FileNumberRecord['recordtime'],
            active=FileNumberRecord['active'],
            sync=1,
            )
        db.session.add(filenumber)
        db.session.commit()
    LearnNoteRecords = RequestDict["LearnNoteRecords"]if "LearnNoteRecords" in RequestDict else []
    for LearnNoteRecord in LearnNoteRecords:
        Picture.query.filter(Picture.id_problem== LearnNoteRecord['id_problem']).delete()
        LearnNote.query.filter(LearnNote.id_problem== LearnNoteRecord['id_problem']).delete()

    for LearnNoteRecord in LearnNoteRecords:
        learnnote = LearnNote(
            id_problem= LearnNoteRecord['id_problem'],
            d_level= LearnNoteRecord['d_level'],
            source=LearnNoteRecord['source'],
            notes=LearnNoteRecord['notes'],
            answer=LearnNoteRecord['answer'],
            usedtime=LearnNoteRecord['usedtime'],
            usedtimes=LearnNoteRecord['usedtimes'],
            inputdate=LearnNoteRecord['inputdate'],
            active=LearnNoteRecord['active'],
            sync=1,
            )
        db.session.add(learnnote)
        db.session.commit()
    PictureRecords = RequestDict["PictureRecords"]if "PictureRecords" in RequestDict else []
    for PictureRecord in PictureRecords:
        picture = Picture(
            id_problem= PictureRecord['id_problem'],
            filepath= PictureRecord['filepath'],
            isanswer= PictureRecord['isanswer'],
        )
        db.session.add(picture)
        db.session.commit()
    return json.dumps({"errorcode": 0, "message": "已同步！"})

@app.route('/sync2access/', methods=['POST','GET'])
def sync2Access():
    learnnotelist= getLearnNote2SyncList()
    filenumberlist= getFileNumber2SyncList()
    if learnnotelist or filenumberlist:
        LearnNote.query.filter(LearnNote.sync == 0).update({"sync": 1})
        FileNumber.query.filter(FileNumber.sync == 0).update({"sync": 1})
        db.session.commit()
        return json.dumps({
            "errorcode": 0, 
            "message": "成功得到服务器数据！",
            "learnnotelist":learnnotelist,
            "filenumberlist":filenumberlist
            },cls=DateEncoder)
    else:
        return json.dumps({
            "errorcode": 1, 
            "message": "无待同步数据！",
            "learnnotelist":[],
            "filenumberlist":[]
            },cls=DateEncoder)

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


