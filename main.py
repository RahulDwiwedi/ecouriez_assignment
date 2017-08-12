from flask import Flask,render_template,request
import pymongo
from pymongo import Connection,MongoClient

app = Flask(__name__)

##con = Connection()
##db=con.my_db
##ecouriez=db.ecouriez

con = MongoClient("mongodb://rahul:rahul0577@ds115573.mlab.com:15573/my_db")
db=con.my_db
ecouriez=db.ecouriez

s=db.ecouriez.count()
result=db.ecouriez.find()
req_query={}
page=""

service_query=""

def pagination():
    offset=int(request.args['offset'])
    limit=int(request.args['limit'])

    starting_id=db.ecouriez.find().sort('_id',pymongo.ASCENDING)
    last_id=starting_id[offset]['_id']
    if offset==0:
        prev_url='/?limit='+str(limit)+'&offset='+str(0)
        next_url='/?limit='+str(limit)+'&offset='+str(offset+limit)
    else:
        next_url='/?limit='+str(limit)+'&offset='+str(offset+limit)
        prev_url='/?limit='+str(limit)+'&offset='+str(offset-limit)

    page=(offset/limit)+1
     
        
    return next_url,prev_url,last_id,limit,offset,page


@app.route('/', methods=["GET","POST"])
def index():
    next_url,prev_url,last_id,limit,offset,page=pagination()
    query={'_id':{'$gte':last_id}}
     
    try:
        if request.method == "POST":
            starttime_query= request.form['starttime']
            endtime_query = request.form['endtime']
            masterband_query= request.form['masterband']
            global service_query
            service_query = request.form['service']
            seriestitle_query= request.form['seriestitle']
            episodetitle_query = request.form['episodetitle']
            category_query = request.form['category']
            tags_query = request.form['tags']
            
            if request.form.getlist('audio'):
                media_query= request.form.getlist('audio')[0]
            elif request.form.getlist('video'):
                media_query= request.form.getlist('video')[0]
            else:
                media_query=""

            if request.form.getlist('clip'):
                clip_query= True
            else:
                clip_query=""

            
                

            my_s={"start_time":starttime_query,
                  "end_time":endtime_query,
                  "master_brand":masterband_query,
                  "service":service_query,
                  "title.Series Title":seriestitle_query,
                  "title.Episode Title":episodetitle_query,
                  "categories":category_query,
                  "tags":tags_query,
                  "media":media_query,
                  "is_clip":clip_query}
            
            global req_query
            req_query=dict((k, v) for k, v in my_s.iteritems() if v)
            
            result=db.ecouriez.find(req_query).sort('_id',pymongo.ASCENDING).limit(limit)
            global s
            s=result.count()
                
            err=str(page)
            return render_template("index.html",data=result,message=req_query,size=s,error=err,next_url=next_url,prev_url=prev_url)

        query.update(req_query)
        err=str(page)
        
        result=db.ecouriez.find(query).sort('_id',pymongo.ASCENDING).limit(limit)
     
        return render_template("index.html",data=result,message=req_query,size=s,error=err,next_url=next_url,prev_url=prev_url)
        
    except Exception as e:
        er=str(page) + str(e)
        data=db.ecouriez.find({'_id':{'$gte':last_id}}).sort('_id',pymongo.ASCENDING).limit(limit)
        return render_template("index.html",data=data,size=s,error=er,next_url=next_url,prev_url=prev_url)

if __name__=='__main__':
    app.run()
