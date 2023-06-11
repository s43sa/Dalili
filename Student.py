from flask import render_template, request, redirect, url_for, session
import MySQLdb.cursors
import re
import numpy as np
import pandas as pd
from DataBase import app,mysql
from Developer import SignAdmin,AddProject


# Below libraries are for text processing using NLTK
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Below libraries are for similarity matrices using sklearn and gensim
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
import gensim.models.keyedvectors as word2vec





ideas =pd.read_csv("/Users/macbook/Desktop/Deena/level10/G_project-499/Dalili/Dalili_DB.csv")# read the data set that contains the stored ideas
ideas_temp = ideas.copy()
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()



model = word2vec.KeyedVectors.load_word2vec_format('/Users/macbook/Downloads/SO_vectors_200.bin', binary=True) # model 1(software model)
G_model=word2vec.KeyedVectors.load_word2vec_format('/Users/macbook/Downloads/wiki-news-300d-1M.vec') # model 2 (general model )

num_similar_items=6 # number of idea that  will be shown to the user
w1=0.5 # weight corresponding to model 1
w2=0.4 # weight corresponding to model 2
w3=0.05 # weight corresponding to Category
w4=0.05 # weight corresponding to Languages


   

@app.route("/")
def pre_processing():
    NLP()
    
    return render_template('index.html')   


@app.route("/index")   
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', Fname=session['Fname'])
    elif   'loggedinA' in session:
          return render_template('Admin.html', Fname=session['Fname']) 
    # by defualt the home page will be shown
    return render_template('index.html')

     

@app.route("/Quiz",  methods=['GET','POST'])
def Quiz():
   if request.method == 'POST' and 'sel2' in request.form and 'Descrip1' in request.form and 'lang1' in request.form: 
      Rec_ideas=[0]*5
      LangListToStr = ' '.join(map(str,request.form.getlist('lang1')))
      row_index=request.form['Descrip1'] #user discription about what he/she search
      cat=request.form['sel2'] #user selected category
      lang1=LangListToStr #user selected languages
      #model 1
      vocabulary = model
      w2v_ideas = []
      w2v_ideas_user=[]
      w2Vec_word_user = np.zeros(200, dtype="float32") 
      #model 2
      vocabulary2 = G_model
      w2v_ideas2 = []
      w2v_ideas_user2=[]
      w2Vec_word_user2 = np.zeros(300, dtype="float32") 

      # apply the W2V on Summary using  model 1
      for i in ideas_temp['Summary']:
        # np.zeros(shape, dtype=float),Return a new array of given shape and type, filled with zeros.
          w2Vec_word = np.zeros(200, dtype="float32") 
          for word in i.split():
              if word in vocabulary:
                  w2Vec_word = np.add(w2Vec_word, model[word])
          w2Vec_word = np.divide(w2Vec_word, len(i.split()))
          w2v_ideas.append(w2Vec_word)
      w2v_ideas = np.array(w2v_ideas)
      
      # apply the W2V on Summary using  model 2
      for i in ideas_temp['Summary']:
          w2Vec_word2 = np.zeros(300, dtype="float32") # np.zeros(shape, dtype=float),Return a new array of given shape and type, filled with zeros.
          for word in i.split():
             if word in vocabulary2:
                 w2Vec_word2 = np.add(w2Vec_word2, G_model[word])
          w2Vec_word2 = np.divide(w2Vec_word2, len(i.split()))
          w2v_ideas2.append(w2Vec_word2)
      w2v_ideas2 = np.array(w2v_ideas2)

    
      # apply the W2V on user input based on model 1
      for word in row_index.split():
         if word in vocabulary:
               w2Vec_word_user = np.add(w2Vec_word_user, model[word])      
      w2Vec_word_user = np.divide(w2Vec_word_user, len(i.split()))
      w2v_ideas_user.append(w2Vec_word_user)
      w2v_ideas_user = np.array(w2v_ideas_user)

      # apply the W2V on user input based on model 2
      for word in row_index.split():
          if word in vocabulary2:
              w2Vec_word_user2 = np.add(w2Vec_word_user2, G_model[word])      
      w2Vec_word_user2 = np.divide(w2Vec_word_user2, len(i.split()))
      w2v_ideas_user2.append(w2Vec_word_user2)
      w2v_ideas_user2 = np.array(w2v_ideas_user2)

      # Bag of Word(BOW) on Languages and user selected Languages
      Languages_vectorizer = CountVectorizer()
      Languages_features   = Languages_vectorizer.fit_transform(ideas_temp["Languages"])
      User_encoded_lang = Languages_vectorizer.transform(np.array(lang1).ravel())

      # One hot encoded on Category and user selected Category
      Category_encoder = OneHotEncoder()
      Category_onehot_encoded = Category_encoder.fit_transform(np.array(ideas_temp["Category"]).reshape(-1,1))
      User_onehot_encoded_cat = Category_encoder.transform(np.array(cat).reshape(-1,1))

      # calculate the distance
      w2v_dist = pairwise_distances(w2v_ideas,w2v_ideas_user.reshape(1,-1),metric='cosine')#model 1
      couple_dist2 = pairwise_distances(w2v_ideas2,w2v_ideas_user2.reshape(1,-1),metric='cosine') #model 2
      category_dist = pairwise_distances(Category_onehot_encoded,User_onehot_encoded_cat,metric='cosine') + 1 # Category 
      Languages_dist = pairwise_distances(Languages_features,User_encoded_lang,metric='cosine') + 1 # Language
       # average distance
      weighted_couple_dist   = (w1 * w2v_dist +  w2 * couple_dist2 + w3 * category_dist + w4 * Languages_dist)/float(w1+w2+w3+w4) 

      indices = np.argsort(weighted_couple_dist.flatten())[0:num_similar_items].tolist()# Returns the indices that would sort an array.  

      df = pd.DataFrame({'Category':ideas['Category'][indices].values,
                'Summary':ideas['Summary'][indices].values,
                'Languages':ideas['Languages'][indices].values,   
                'University':ideas['University'][indices].values,
               'Link': ideas['Link'][indices].values,
                'HrdWare':ideas['HardWare'][indices].values
                })

      Rec_ideas=np.array(df)
      
    
      return render_template('Quiz.html',Rec_ideas=Rec_ideas) 


   return render_template('Quiz.html',title='Start Searching')    
    

@app.route("/Sign", methods=['GET','POST'])
def Sign():  
    msg = ''
        # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables
        email = request.form['email']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        account=check_signin(email,password,cursor)
        
        # If account exists in Students table in Dalili database
        if account:
            # Create session data
            session['loggedin'] = True
            session['email'] = account['email']
            session['Fname'] = account['Fname']
            # Redirect to home page
            return render_template("index.html", title='home page')


        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template("Sign.html", msg=msg)


 

@app.route("/SignUp", methods=['GET','POST'])
def SignUp():     
  
    msg = ''

    # Check if "Fname", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Fname' in request.form and 'password' in request.form and 'email' in request.form:

        # Create variables for easy access
        Fname = request.form['Fname']
        Lname = request.form['Lname']
        password = request.form['password']
        email = request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        msg=checkSignUP(Fname,Lname,password,email,cursor)
        mysql.connection.commit()

     # Form is empty... (no POST data)    
    elif request.method == 'POST':
     msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('SignUp.html', msg=msg)





@app.route('/logout',methods=['GET','POST'])
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('email', None)
   session.pop('loggedinA', None)
   session.pop('Id', None)
   

   # Redirect to login page
   return render_template('index.html')




@app.route('/profile',methods=['GET','POST'] )
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Students WHERE email = %s', (session['email'],))
        account = cursor.fetchone()

        # Show the profile page with account info
        return render_template('profile.html', account=account)

    elif 'loggedinA' in session:
            # We need all the account info for the Admin so we can display it on the profile page
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Developer WHERE Id = %s', (session['Id'],))
        account = cursor.fetchone()

        # Show the profile page with account info
        return render_template("profile.html", account=account)     


    # User is not logged in -->redirect to Sign page
    return redirect(url_for('Sign'))


@app.route('/Check',  methods=['GET','POST'])
def Check():

    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Students WHERE email = %s ', (email,))
        account = cursor.fetchone()
        if account:
            msg=account['password']
        else:
            msg='This Email is not registered !'    
        return render_template("Check.html",msg=msg)
        
    return render_template("Check.html")


##################################################################################################################
##################################################################################################################

def NLP():
         #  start the NLP, 1- remove the stop word from Summary of the ideas
    for i in range(len(ideas_temp["Summary"])):
       string = ""
       for word in ideas_temp["Summary"][i].split():
          word = ("".join(e for e in word if e.isalnum()))
          word = word.lower()
          if not word in stop_words:
            string += word + " "  
       ideas_temp.at[i,"Summary"] = string.strip()
    #  2- do the lemmatization from Summary of the ideas
    for i in range(len(ideas_temp["Summary"])):
       string = ""
       for w in word_tokenize(ideas_temp["Summary"][i]):
          string += lemmatizer.lemmatize(w,pos = "v") + " "
       ideas_temp.at[i, "Summary"] = string.strip()

   
    return(ideas_temp['Summary'][0]) # for testing

def check_signin(email,password,cursor):

    # Check if account exists using MySQL
    
    cursor.execute('SELECT * FROM Students WHERE email = %s AND password = %s', (email, password,))
    # Fetch  record and return result
    account = cursor.fetchone()
     
     # If account exists in Students table in Dalili database
    if account:
        
        return account
    else:
         return None

def checkSignUP(Fname,Lname,password,email,cursor):

        # Check if account exists using MySQL
        
        cursor.execute('SELECT * FROM Students WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            return msg
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return msg
        elif not Fname or not password or not email:
            msg = 'Please fill out the form!'
            return msg
        else:
            # Account doesnt exists and the form data is valid, insert new account into accounts table
            cursor.execute('INSERT INTO Students(email,Fname,Lname,password) VALUES (%s, %s, %s, %s)', (email,Fname,Lname, password,))
            
            msg = 'You have successfully registered!'
            return  msg




if __name__ == '__main__':
    app.run(debug=True)
   
 

