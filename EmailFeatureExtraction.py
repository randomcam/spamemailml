import mailbox
import csv 
import features as f #features.py




#Ran for each message in getMbox
def extractFeatures(message):
    #finders = [f.numbersinEmailAddr,f.length,f.avgWordLength,f.keywordCount,f.spellingmistakes,f.fakelinks,f.capitalletters,f.linklength,f.numbersinLink] # finders in features.py
    finders = [f.length,f.numbersinEmailAddr,f.avgWordLength,f.keywordCount,f.spellingMistakes,f.capitalLetters,f.linkLength,f.numbersinLink,f.fakeLinks] # finders in features.py
    feature_ratings={} # feature values
    
    

    
    for i in finders:
        key = i(message, 1)# title
        
        value = i(message)  # passing message to finder function
        
        feature_ratings[key] = value # append
        

    soups=dict(f.emotion(message)) #add the emotions
    speech=dict(f.pos(message)) # add the POS tags

    feature_ratings.update(soups)
    feature_ratings.update(speech)
    return feature_ratings # feature values



def getMbox(mboxpath):
    mbox=mailbox.mbox(mboxpath) #open mbox file

    feature_ratings_list=[]
    for message in mbox: #for each message in mbox - get feature functions
        featurelist=extractFeatures(message) #returns a dictionary of features 
        feature_ratings_list.append(featurelist) #add dict to full list
        
        

    return feature_ratings_list # returns list of all messages features




#phishing

spam_feature_list=getMbox('emails-phishing.mbox') 

#ham


ham_feature_list=getMbox('hardham.mbox')

#new test data
newphishing_feature_list=getMbox('NewNewPhishing.mbox')
newham_feature_list=getMbox('NewNewHam.mbox')
#write new data to csv
with open('newphishingfeatures.csv',"w",newline="") as file:
    writer=csv.writer(file)
    #Header
    header=list(newphishing_feature_list[0].keys()) + ['tag']
    writer.writerow(header)
    #DATA
    for feature_dict in newphishing_feature_list:
        row=[]
        for key in header[:-1]:
            row.append(feature_dict[key])
        row.append("phishing")
        writer.writerow(row)
    for feature_dict in newham_feature_list:
        row=[]
        for key in header[:-1]:
            row.append(feature_dict[key])
        row.append("ham")
        writer.writerow(row)
        

#write phishing and ham message features to a single csv with tags
with open("features.csv","w",newline="") as file:
    writer=csv.writer(file)
    #HEADER
    header=list(spam_feature_list[0].keys()) + ['tag']
    writer.writerow(header)
    #DATA
    for feature_dict in spam_feature_list:
        row=[]
        for key in header[:-1]:
            row.append(feature_dict[key])
        row.append("phishing")
        writer.writerow(row)

    for feature_dict in ham_feature_list:
        row=[]
        for key in header[:-1]:
            row.append(feature_dict[key])
        row.append("ham")
        writer.writerow(row)





