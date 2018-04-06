from connection import *





'''   it  scrap user data and save to DB '''
@app.route("/users/<facebookId>", methods=['POST','GET'])
def UserData(facebookId):

    local = request.args.get('local')
    if local == None:
        local = False
    else :
        local = True
        userData = getByFbID(facebookId) 

        if userData is None :
            return  str(json.dumps({"error": "User not exist in the Database"  }))
        else :
            return  str(json.dumps({"name": userData.name , "picture" :userData.picture , "fb_id" :userData.fb_id }, indent = 4 ,separators=(',', ': ')))            


    fileData = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']
        
    app_id = fileData['app_id']
    app_secret = fileData['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&&client_id=%s&client_secret=%s' % (app_id, app_secret)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    tokenData = result.split("&")[0]
    token=json.loads(tokenData)

    url = 'https://graph.facebook.com/v2.8/%s?access_token=%s&fields=name,id,email' % (facebookId,token["access_token"])
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    dataDetails = json.loads(result)
    
    if 'error' in dataDetails :
        return  str(json.dumps({"error": "ID %s does not exist" % facebookId }))

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/%s/picture?access_token=%s&redirect=0&height=720&width=720' %  (facebookId,token["access_token"])
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    picture = data["data"]["url"]

    userObj = CheckIfexist(dataDetails,picture)
    return str(json.dumps({"name": userObj.name , "picture" :userObj.picture , "fb_id" :userObj.fb_id  }, indent=4 ,separators=(',', ': '))) 



''' end'''
def getByFbID(id):
    userObj = users.query.filter_by(fb_id=id).first()
    return userObj

def AddUser(dataDetails,picture):
    userObj = users(fb_id=dataDetails["id"] ,name=dataDetails["name"],  picture =picture)
    db.session.add(userObj)
    db.session.commit()
    return userObj
    
def CheckIfexist(dataDetails,picture):
    userObj = users.query.filter_by(fb_id=dataDetails["id"]).first()
    if userObj is None :
        userObj = AddUser(dataDetails,picture)

    else :
        userObj = UpdateUser (userObj,dataDetails,picture)



    return userObj

def UpdateUser (userObj,dataDetails,picture):
    
    if userObj.name != dataDetails["name"]:
        userObj.name = dataDetails["name"]
    if userObj.picture != picture:
        userObj.picture = picture
    db.session.commit()
    return userObj


    


    

 



if __name__ == '__main__':
   app.run(debug = True)