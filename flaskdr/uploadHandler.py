
#sorry, the code is under repair
"""
class uploadHandler(BaseHandler):

@tornado.web.authenticated

def get(self):

    self.render("upload.html",user=self.current_user)

def post(self):
    db = pymongo.Connection('mongodb+srv://dbDevelepner:54321@cluster0-dbjfp.azure.mongodb.net/test?retryWrites=true&w=majority').heroku_appxxxx
    user = db.userInfo.find_one({'Username':self.current_user})
    file1 = self.request.files['images'][0]
    original_fname = file1['filename']

    print "file: " + original_fname + " is uploaded"

    fs = gridfs.GridFS(user)
    fs.put(file1)
    #db.userInfo.update({'Username':self.current_user},{'$push':{'Images': file1}})  

    self.redirect('/upload')
    """