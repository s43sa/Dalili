
import unittest
import Student
import mysql.connector
import MySQLdb.cursors
import Developer

class Test_TestViewsClass(unittest.TestCase):
  connection = None


  def setUp(self):
 
   self.connection= mysql.connector.connect(user = 'root',password = '',host = '127.0.0.1',database = 'Dalili' )
   
   


  def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
   
  def test_connection(self):
        # test database connection
        self.assertTrue(self.connection.is_connected()) 

      
  def test_NLP(self):
        #Views.NLP() Function: will remove the stop word and do the lemmatization(NLP) on all the Summarys in the data set
        # in this test we will check "for example we choose the Summary in index 0" if it did the NLP 

        result=Student.NLP()
        ExpResult="propose project application design blind people analyze video use deep learn algorithm extract textual information describe videos"  
        self.assertEqual(result, ExpResult)

  def test_SignIn(self):
        #Views.check_signin(email,password) function: we will send the email and the password that the user enters and check if it store in the database
        #if the user is sign to the system the function will return the user information and log him to his acount otherwise it will return None and display 
        # an error message 
       self.setUp()
       email="dalmadani0005@stu.kau.edu.sa"
       password="Aa123456"
       cnx=self.connection
       cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
       result=Student.check_signin(email,password,cursor)
       ExpResult=('dalmadani0005@stu.kau.edu.sa', 'Deena', 'Almadani', 'Aa123456')
      
       self.assertEqual(result,ExpResult)   
       
  def test_AdminSignIn(self):
        #Views.checkAdmin_signin(Id,password) function: we will send the Id and the password that the Admin enters and check if it store in the 
        #database(Table Devaloper)if the Admin is sign to the system the function will return the
        #Admin information and log him to Add project page otherwise it will return None and display  an error message 

        Id="1808251"
        password="Aa12345"
        cnx=self.connection
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        result=Developer.checkAdmin(Id,password,cursor)
        ExpResult=(1808251, 'Deena', 'Almadani', 'Aa12345')
        self.assertEqual(result,ExpResult)    

  def test_SignUp(self):  
        # Views.checkSignUP function: it will take the user input and check:
        # if user exit --> it will return --> Account already exists! 
        # if user not exit --> it will save the user info in the database and  return meassage -->You have successfully registered!
        
        email="sara@gmail.com"
        Fname="Sara"
        Lname="Alzahrani"
        password="Aa54321"
        cnx=self.connection
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        result=Student.checkSignUP(Fname,Lname,password,email,cursor)
        
        ExpResult="You have successfully registered!"
        self.assertEqual(result,ExpResult)   

  def test_AddProject(self): 
        # Views.AddProject function: it will take the Admin input  about the new project details and save it  the Dalili_DB.csv file: 
        # in this test we will check if it been save in the file or not

        category="Artificial Intelligence"
        summary="Add project for testing"
        university="UMM ALQura"
        link="https://uqu.edu.sa/"
        language="Java"
        hw="0" 
        Developer.AddProject(category,summary,university,link,language,hw)
        ExpResult="Project saved in the file"
        NewRow=['Artificial Intelligence', 'Add project for testing', 'Java', 'UMM ALQura', 'https://uqu.edu.sa/', '0'] #how the data will be save in the file

        with open('Dalili_DB.csv') as file1:
            existing_lines = Developer.csv.reader(file1)
            for row in existing_lines:
                if NewRow !=  row:
                    result="Project not saved in the file"
                    
                else:
                    result="Project saved in the file"       
        self.assertEqual(result,ExpResult) 

   


if __name__ == '__main__':
    unittest.main()

