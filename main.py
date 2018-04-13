from connection import *


CONSUMER_KEY = 'qf8PgvKdBPu2RynHWfpA9MKOL'
CONSUMER_SECRET = 'ROjmfNDVOad47cvSXRS3rPtrn0r0zceAieajR46E8EmPLZ8lVL'
ACCESS_KEY = '319102708-Sjt9HwUsZPbcwSAaOwHUeUg37mTAJyX6tv09nSOJ'
ACCESS_SECRET = 'uLUpsT1hXEIIc8m34vmAFG81Ne08bwpJwQFsq49so2RJA'




def UserDataTwitter(Id):
    auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    api = tweepy.API(auth)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    #search
    api = tweepy.API(auth)
    try :   
        user = api.lookup_users(user_ids=[Id])

    except:
        return json.dumps({"error": "No user matches for this id"  })


    dataDetails = user[0]
    user = users(name = dataDetails.name , tw_id = Id , picture = dataDetails.profile_image_url_https)

    return user        




@app.route("/tweets/<Id>", methods=['POST','GET'])
def UsertweetsTwitter(Id):
    auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    api = tweepy.API(auth)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    #search
    api = tweepy.API(auth)
   
    try :   
        posts = api.user_timeline(id=Id, count = 25 ,include_rts = True)

    except:
        return json.dumps({"error": "No user matches for this id"  })
    return posts   
    # return str(posts[0].text) +"   "+ str(posts[0].created_at) +"   "+ str(posts[0].id_str) +"   "+ str(posts[1].id_str)  


'''   it  scrap user data and save to DB '''
@app.route("/users/<twId>", methods=['POST','GET'])
def UserData(twId):

    local = request.args.get('local')
    if local == None:
        local = False
    else :
        local = True
        userData = getByTwID(twId) 

        if userData is None :
            return  json.dumps({"error": "User not exist in the Database"  })
        else :
            return  json.dumps({"name": userData.name , "picture" :userData.picture , "tw_id" :userData.tw_id }, sort_keys=True,
                   indent=4, separators=(',', ': '))            


   
    user = UserDataTwitter(twId)
    


 

    userObj = CheckIfexist(user)
    return json.dumps({"name": userObj.name , "picture" :userObj.picture , "tw_id" :userObj.tw_id  }, indent=4 ,separators=(',', ': '))


@app.route("/users/<accID>/posts", methods=['POST','GET'])
def getposts(accID):

    local = request.args.get('local')
    if local == None:
        local = False
    else :
        local = True
        tweets = getTweetsByID(accID) 

        if tweets is None :
            return  json.dumps({"error": "User not exist in the Database"  })
        else :
            return  printTweets(tweets,accID)          


   
    tweetsnew = UsertweetsTwitter(accID)
    


 

    tweets = CheckIfTweetsExist(tweetsnew,accID)
    return printTweets(tweets,accID)

def printTweets(tweets,accID):
    json_Data =[]
    i=0
    # print(str(tweets))
    for tweet in tweets:

    
        post = posts( acc_id= accID, tw_id=tweet.id_str ,message=tweet.text ,createdTime=tweet.created_at)

        json_Data.append(str(post))

    return json.dumps(json_Data)

def CheckIfTweetsExist(tweets , accid):
    tweetsdb = getTweetsByID(accid)
   
    if len(tweetsdb) ==0 :
        
        tweets = Addtweets(tweets,accid)

    else :
        tweets = UpdateTweets(tweetsdb,tweets)



    return tweets

def getTweetsByID(accID):
    tweets = posts.query.filter_by(acc_id=accID).all()
    return tweets


def Addtweets(tweets,accID):
    i=0
    for tweet in tweets:

        post = posts( acc_id= accID, tw_id=tweet.id_str ,message=tweet.text ,createdTime=tweet.created_at)
        db.session.add(post)
        db.session.commit()
        print(i)
        i=i+1

    return tweets
def UpdateTweets(tweetsdb,tweets):
    i=0
    if tweetsdb[0].tw_id == tweets[0].id_str:
        return tweets
    else :
        for tweet in tweetsdb:
            tweet.tw_id =  tweets[i].id_str
            tweet.message = tweets[i].text
            tweet.createdTime =tweets[i].created_at
            db.session.commit()
            i = i + 1


        
    return tweets


    


''' end'''
def getByTwID(id):
    userObj = users.query.filter_by(tw_id=id).first()
    return userObj

def AddUser(user):
    userObj = users(tw_id=user.tw_id ,name=user.name,  picture =user.picture)
    db.session.add(userObj)
    db.session.commit()
    return userObj
    
def CheckIfexist(user):
    userObj = users.query.filter_by(tw_id=user.tw_id).first()
    if userObj is None :
        userObj = AddUser(user)

    else :
        userObj = UpdateUser (userObj,user)



    return userObj

def UpdateUser (userObj,user):
    
    if userObj.name != user.name :
        userObj.name = user.name 
    if userObj.picture != user.picture:
        userObj.picture = user.picture
    db.session.commit()
    return userObj


    


    

 



if __name__ == '__main__':
   app.run(debug = True)