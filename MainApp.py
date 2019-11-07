import MySQLdb
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.carousel import Carousel
from google.cloud import vision
from google.cloud.vision import types
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
import io
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os.path
from kivy.cache import Cache
from kivy.base import runTouchApp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.base import EventLoop
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import time
import sys
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
import matplotlib.pyplot as plt
import requests,json
import numpy as np
import cv2
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/key.json"
f = StringProperty("/")
pop1 = Popup(title='Empty Data', content=Label(text='Empty Username and/or Password'),size_hint=(None,None),size=(280,100))
pop2 = Popup(title='Login Failed', content=Label(text='Incorrect Username and/or Password'),size_hint=(None,None),size=(280,100))
pop3 = Popup(title='TextField empty', content=Label(text='Fields are all required'),size_hint=(None,None),size=(280,100))     
pop4 = Popup(title='Password Empty', content=Label(text='Password cannot be empty'),size_hint=(None,None),size=(280,100))
pop5 = Popup(title='Password Mismatch', content=Label(text='Retype Your Password Correctly'),size_hint=(None,None),size=(280,100))
pop6 = Popup(title ='Username Already Taken', content = Label(text='Please choose different username'), size_hint= (None, None), size=(300,200))
pop7 = Popup(title ='Do you want to clear the image?', content = Label(text='Please confirm!'), size_hint= (None, None), size=(300,200))
pop16 = Popup(title ='Fill up the form', content = Label(text='Please fill up the form completely'), size_hint= (None, None), size=(300,200))
pop17 = Popup(title ='Registered Sucessfully', content = Label(text='You have successfully registered your account go back to Login Page to login'), size_hint= (None, None), size=(300,200))
class WelcomeScreen(Screen):
	pass
class LoginScreen(Screen):
    def patient_login(self,username,password):
        global patientUser
        patientUser = username
        print ('SUCCESSFULLY CONNECTED TO DATABASE!')
        if (self.txt_username.text=="" and self.txt_password.text==""):
            print (pop1.title)
            pop1.open()
        elif (query.execute("SELECT * FROM `registeredpatient` WHERE `username` ='"+username+"' AND `pass`='"+password+"'")):
            self.manager.current = 'mainscreen'
        else:
            db.commit()
            print (pop2.title)
            pop2.open()
        self.txt_password.text =""

class AdminLoginScreen(Screen):
    def admin_login(self,adminusername,adminpassword):
        global adminUser
        adminUser = adminusername
        print('SUCCESSFULLY CONNECTED TO DATABASE!') 
        if(self.txt_adminusername.text =="" and self.txt_adminpassword.text==""):
            print(pop1.title)
            pop1.open()
        elif(query.execute("SELECT * FROM `admin` WHERE `admin_user` = '"+adminusername+"' AND`admin_pwd` ='"+adminpassword+"'")):
            self.manager.current ='adminmain'
        else:
            db.commit()
            print(pop2.title)
            pop2.open()
        self.txt_adminpassword.text =""
class AdminMainScreen(Screen):
    pass
class AdminGuideScreen(Screen):
    pass
class SignupScreen(Screen):
    patientUser = StringProperty()
    def patient_signup(self,firstName,lastName,address,patient_age,gender,patientUsername,patientcontact,patientpass,patientpass_retype,checkup):
        self.patientUser = patientUsername
        if(firstName=='' or lastName=='' or address=='' or patient_age=='' or gender=='' or patientUsername =='' or patientcontact =='' or patientpass =='' or patientpass_retype =='' or checkup ==''):
            print(pop16.title)
            pop16.open()
        elif(patientpass != patientpass_retype):
            print(patientpass)
            print(patientpass_retype)
            print(pop5.title)
            self.txt_repatientpass.text = ""
            self.txt_patientpass.text = ""
            pop5.open()
        elif(query.execute("SELECT count(username) from `registeredpatient` WHERE `username` = '"+patientUsername+"'")):
            result = query.fetchone()
            if(result==(1,)):
                pop6.open()
                self.txt_patientUsername.text = ""
                self.txt_patientpass.text = ""
                self.txt_repatientpass.text = ""
            elif((firstName != '' and lastName !='' and address !='' and patient_age !='' and gender !='' and patientUsername !='' and patientcontact !='' and patientpass !='' and patientpass_retype !='' and checkup !='')
                and ((patientpass == patientpass_retype))):
                query.execute("INSERT INTO `registeredpatient`(firstName,lastName,address,age,gender,username,contactNum,pass,lastcheckup) VALUES ('"+firstName+"','"+lastName+"','"+address+"','"+patient_age+"','"+gender+"','"+patientUsername+"','"+patientcontact+"','"+patientpass+"','"+checkup+"')")
                print ('Sucessfully Inserted to the Database')
                db.commit()
                self.manager.current = 'login'
                pop17.open()
                self.txt_firstname.text = ""
                self.txt_lastname.text =""
                self.txt_address.text = ""
                self.txt_gender.text = "Gender"
                self.txt_patientUsername.text = ""
                self.txt_contact.text = ""
                self.txt_patientage.text = ""
                self.txt_patientpass.text = ""
                self.txt_repatientpass.text = ""
                self.txt_checkup = "Choose here..."
            else:
                print('Got some errors/ Cannot Connect to DB')
                db.commit()
        else:
            print('Got some errors/ Cannot Connect to DB')
            db.commit()
class ScrollableContainer1(ScrollView):
    pass
class ScrollableContainer2(ScrollView):
    pass
class ScrollableContainer3(ScrollView):
    pass
class PatientInfoScreen(Screen):
    patientname = StringProperty()
    address = StringProperty()
    gender = StringProperty()
    age = StringProperty()  
    contactNum = StringProperty()
    def patient_info(self, username): 
        query.execute("SELECT * FROM `registeredpatient` WHERE `username`='"+username+"'")
        results = query.fetchall()
        db.commit()
        for row in results:
            print (row[2] + ', ' + row[1] + ' ' + row[3] + ' ' + row[5] + ' ' + row[4] + ' ' + row[7])
            self.patientname = row[2] + ', ' + row[1]
            self.address = row[3]
            self.gender = row[5]
            self.age = row[4]
            self.contactNum = row[7]
class DiagnoseScreen(Screen):
    global diagnosis
    global g
    global f
    diagnosis = ''
    patientUser = StringProperty()
    image = StringProperty("images/noimagetooth.png")
    imageNormal = StringProperty("images/diagnosistoothnormal.png")
    imageModerate = StringProperty("images/diagnosistoothmoderate.png")
    imageSevere = StringProperty("images/diagnosistoothsevere.png")
    diagnosisTooth = StringProperty("images/diagnosistooth.png")
    notTooth = StringProperty("images/diagnosisnottooth.png")
    f = image
    g = diagnosisTooth
    def dropdown(self):
        max = 2.85
        self.toothnumber.dropdown_cls.max_height = self.toothnumber.height * max + max * 2
    def refresh2(self,*args):
        self.diagnosisTooth = g
    def refresh(self, *args):
        self.fileName = f
        self.image= f
        print(self.image)
    def clear(self, *args):
        global f
        global g
        self.image = str("images/noimagetooth.png")
        self.diagnosisTooth = str("images/diagnosistooth.png")
        self.fileName = ''
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        f = ''
        g = self.diagnosisTooth
    def process2(self, *args):
        global toothnumber
        toothnumber = self.toothnumber.text
    def process(self, *args):
        global f
        fi = str(f)
        global g
        global toothnumber
        toothnumber = self.toothnumber.text
        g = self.diagnosisTooth
        print(fi)
        global diagnosis
        diagnosis = ''
        if (toothnumber != 'Choose tooth number here' and (fi != '<StringProperty name=image>' and fi !='')):
            client = vision.ImageAnnotatorClient()
            file_name = f
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()
            image = types.Image(content=content)
            response = client.label_detection(image=image)
            newlist = []
            labels = response.label_annotations
            for label in labels:
                labelDescription = label.description
                count = labelDescription.count("tooth")
                count1 = labelDescription.count("jaw")
                count2 = labelDescription.count("lighting")
                count3 = labelDescription.count("mouth")
                count4 = labelDescription.count("dentistry")
                count5 = labelDescription.count("Tooth")
                newlist.append(count)
                newlist.append(count1) 
                newlist.append(count2)
                newlist.append(count3)
                newlist.append(count4)
                newlist.append(count5)
            if 1 in newlist:
                print('success')
                processImage = cv2.imread(f)
                boundaries = [([0,0,0], [90,90,90])]
                for(lower,upper) in boundaries:
                    lower = np.array(lower, dtype = 'uint8')
                    upper = np.array(upper, dtype = 'uint8')
                    mask = cv2.inRange(processImage, lower, upper)
                    blackValue=cv2.countNonZero(mask)
                    url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
                    data = {'file': open(f, 'rb'), \
                    'modelId': ('', '95623191-917b-4df3-9b0c-63be812287fc')}
                    response = requests.post(url, auth= requests.auth.HTTPBasicAuth('8EwgU2Y5PR6Rtkg5LKKDidl2qmGLR5asv-iqNW7Nzh9', ''), files=data)
                    info = json.loads(response.text)
                    prediction = info["result"][0]["prediction"][2]['label']
                    text=''
                    if ((blackValue>= 0 and blackValue <= 3800)and prediction =='Normal'):
                        diagnosis = "Normal"
                        print(blackValue)
                        print(prediction)
                    elif ((blackValue>= 0 and blackValue <= 3800)and prediction =='Moderate'):
                        diagnosis = "Normal"
                        print(prediction)
                    elif ((blackValue>= 0 and blackValue <= 3800)and prediction =='Severe'):
                        diagnosis = "Normal"
                        print(prediction)
                        print(blackValue)
                    elif ((blackValue>3800  and blackValue <= 10000 )and prediction =='Moderate'):
                        diagnosis = "Moderate"
                        print(blackValue)
                        print(prediction)
                    elif ((blackValue> 3800 and blackValue <= 10000 )and prediction =='Normal'):
                        diagnosis = "Moderate"
                        print(blackValue)
                        print(prediction)
                    elif ((blackValue> 3800 and blackValue <= 10000 )and prediction =='Severe'):
                        diagnosis = "Moderate"
                        print(blackValue)
                        print(prediction)
                    elif ((blackValue> 10000 and blackValue <= 230000 )and prediction =='Moderate'):
                        diagnosis = "Severe"
                        print(blackValue)
                        print(prediction)
                    elif ((blackValue> 10000 and blackValue <= 230000 )and prediction =='Severe'):
                        diagnosis = "Severe"
                        print(blackValue)
                        print(prediction)
                    elif ((blackValue> 10000 and blackValue <= 230000 )and prediction =='Normal'):
                        diagnosis = "Severe"
                        print(blackValue)
                        print(prediction)
                    else:
                        diagnosis ='Cannot be process'
                        print(diagnosis)
                        print(blackValue)
            else:
                diagnosis ="Not Tooth"
        elif(toothnumber != 'Choose tooth number here' and fi == '<StringProperty name=image>'):
            popcProcess = Popup(title='Failed to process', content=Label(text='Please capture/choose tooth'),size_hint=(None,None),size=(280,100))
            popcProcess.open()
        elif(toothnumber != 'Choose tooth number here' and fi == ''):
            popcProcess = Popup(title='Failed to process', content=Label(text='Please capture/choose tooth'),size_hint=(None,None),size=(280,100))
            popcProcess.open()
        else:
            popcProcess = Popup(title='Failed to process', content=Label(text='Please select a toothnumber'),size_hint=(None,None),size=(280,100))
            popcProcess.open()
    def updateDiagnosis(self):
        global g
        g = self.diagnosisTooth
        print(g)
        global diagnosis
        print(diagnosis)
        if diagnosis =="Normal":
            g = self.imageNormal
            print(g)
        elif diagnosis =="Moderate":
            g = self.imageModerate
            print(g)
        elif diagnosis =="Severe":
            g = self.imageSevere
            print(g)
        elif diagnosis == "Not Tooth":
            g = self.notTooth
            print(g)
        else:
            print(diagnosis)
    def saveRecord(self):
        global diagnosis
        global g
        global f
        global patientUser
        global toothnumber
        toothnumber = self.toothnumber.text
        fi = str(f)
        gi = str(g)
        newtoothnum = str(toothnumber)
        print(fi)
        if fi != '<StringProperty name=image>' and fi != '':
            date = time.strftime("%a, %d %b %Y %H:%M:%S")
            saveToothImage = open(f, 'rb').read()
            if(((diagnosis !='' and f !='') and (diagnosis !='' or f !='')) and (newtoothnum != "Choose tooth number here" and gi != 'images/diagnosisnottooth.png')):
                statementQuery = "INSERT INTO patientrecord(patientUsername,toothnumber,toothDiagnosis,currentDate,toothImage) VALUES (%s,%s,%s,%s,%s)"
                query.execute(statementQuery,(patientUser,newtoothnum,diagnosis,date,saveToothImage,))
                db.commit()
                popSave = Popup(title='Success', content=Label(text='Successfully save to the dental record'),size_hint=(None,None),size=(280,100))
                popSave.open()
            elif(((diagnosis !='' and f !='') and (diagnosis !='' or f !='') and newtoothnum == "Choose tooth number here")):
                popTN = Popup(title='Failed to save', content=Label(text='Please choose a toothnumber'),size_hint=(None,None),size=(280,100))
                popTN.open()
            elif(((diagnosis !='' and f !='') and (diagnosis !='' or f !='')) and (newtoothnum != "Choose tooth number here" and gi == 'StringProperty name=diagnosisTooth>')):
                popProcess = Popup(title='Failed to save', content=Label(text='Please process the seleceted image'),size_hint=(None,None),size=(280,100))
                popProcess.open()
            elif(((diagnosis !='' and f !='') and (diagnosis !='' or f !='')) and (newtoothnum != "Choose tooth number here" and gi == 'images/diagnosisnottooth.png')):
                popNotTooth = Popup(title='Failed to save', content=Label(text='Image is not a tooth image'),size_hint=(None,None),size=(280,100))
                popNotTooth.open()
            else:
                popProcess = Popup(title='Failed to save', content=Label(text='Please process the seleceted image'),size_hint=(None,None),size=(280,100))
                popProcess.open()
        else:
            popCapture = Popup(title='Failed to save', content=Label(text='Please capture/choose a tooth image'),size_hint=(None,None),size=(280,100))
            popCapture.open()
    def updateToothChange(self):
        global f
        self.image = str('toothimages/tooth.png')
        f = self.image
        print(f)
class DentalChartScreen(Screen):    
    molar1 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar2 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar3 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar4 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar5 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar6 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar7 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar8 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar9 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar10 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar11 = StringProperty("images/TOOTHFILE/MOLAR.png")
    molar12 = StringProperty("images/TOOTHFILE/MOLAR.png")
    premolar1 = StringProperty("images/TOOTHFILE/PREMOLAR.png")
    premolar2 = StringProperty("images/TOOTHFILE/PREMOLAR.png")
    premolar3 = StringProperty("images/TOOTHFILE/PREMOLAR.png")
    premolar4 = StringProperty("images/TOOTHFILE/PREMOLAR.png")
    premolarl1 = StringProperty("images/TOOTHFILE/PREMOLARL.png")
    premolarl2 = StringProperty("images/TOOTHFILE/PREMOLARL.png")
    premolarl3 = StringProperty("images/TOOTHFILE/PREMOLARL.png")
    premolarl4 = StringProperty("images/TOOTHFILE/PREMOLARL.png")
    canine1 = StringProperty("images/TOOTHFILE/CANINE.png")
    canine2 = StringProperty("images/TOOTHFILE/CANINE.png")
    caninel1 = StringProperty("images/TOOTHFILE/CANINEL.png")
    caninel2 = StringProperty("images/TOOTHFILE/CANINEL.png")
    incisor1 = StringProperty("images/TOOTHFILE/INCISOR.png")
    incisor2 = StringProperty("images/TOOTHFILE/INCISOR.png")
    incisor3 = StringProperty("images/TOOTHFILE/INCISOR.png")
    incisor4 = StringProperty("images/TOOTHFILE/INCISOR.png")
    incisorl1 = StringProperty("images/TOOTHFILE/INCISOR-L.png")
    incisorl2 = StringProperty("images/TOOTHFILE/INCISOR-L.png")
    incisorl3 = StringProperty("images/TOOTHFILE/INCISOR-L.png")
    incisorl4 = StringProperty("images/TOOTHFILE/INCISOR-L.png")
    molarmoderate = StringProperty("images/TOOTHFILE/MOLAR-MODERATE.png")
    molarsevere = StringProperty("images/TOOTHFILE/MOLAR-SEVERE.png")
    premolarmoderate = StringProperty("images/TOOTHFILE/ PREMOLAR-MODERATE.png")
    premolarmoderatel = StringProperty("images/TOOTHFILE/PREMOLAR-MODERATE-L.png")
    premolarsevere = StringProperty("images/TOOTHFILE/PREMOLAR-SEVERE.png")
    premolarseverel = StringProperty("images/TOOTHFILE/PREMOLAR-SEVERE-L.png")
    caninemoderate = StringProperty("images/TOOTHFILE/CANINE-MODERATE.png")
    caninemoderatel = StringProperty("images/TOOTHFILE/CANINE-MODERATE-L.png")
    caninesevere = StringProperty("images/TOOTHFILE/CANINE-SEVERE.png")
    canineseverel = StringProperty("images/TOOTHFILE/CANINE-SEVERE-L.png")
    incisormoderate = StringProperty("images/TOOTHFILE/INCISOR-MODERATE.png")
    incisormoderatel = StringProperty("images/TOOTHFILE/INCISOR-MODERATE-L.png")
    incisorsevere = StringProperty("images/TOOTHFILE/INCISOR-SEVERE.png")
    incisorseverel = StringProperty("images/TOOTHFILE/INCISOR-SEVERE-L.png")
    molarc = StringProperty("images/TOOTHFILE/MOLARC.png")
    premolarc = StringProperty("images/TOOTHFILE/PREMOLARC.png")
    premolarlc = StringProperty("images/TOOTHFILE/PREMOLARLC.png")
    caninec = StringProperty("images/TOOTHFILE/CANINEC.png")
    caninelc = StringProperty("images/TOOTHFILE/CANINELC.png")
    incisorc = StringProperty("images/TOOTHFILE/INCISORC.png")
    incisorlc = StringProperty("images/TOOTHFILE/INCISORLC.png")
    molarx = StringProperty("images/TOOTHFILE/MOLARX.png")
    premolarx = StringProperty("images/TOOTHFILE/PREMOLARX.png")
    premolarlx = StringProperty("images/TOOTHFILE/PREMOLARLX.png")
    incisorx = StringProperty("images/TOOTHFILE/INCISORX.png")
    incisorlx = StringProperty("images/TOOTHFILE/INCISORLX.png")
    caninex = StringProperty("images/TOOTHFILE/CANINEX.png")
    caninelx = StringProperty("images/TOOTHFILE/CANINELX.png")

    def updateChart(self):
        global diagnosis
        global toothnumber
        if diagnosis == "Normal" and toothnumber =="Lower Molar 1 - TN 1":
            self.molar1 = self.molar1
        elif diagnosis == "Moderate" and toothnumber=="Lower Molar 1 - TN 1":
            self.molar1 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Lower Molar 1 - TN 1":
            self.molar1 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Lower Molar 2 - TN 2":
            self.molar2 = self.molar2
        elif diagnosis == "Moderate" and toothnumber=="Lower Molar 2 - TN 2":
            self.molar2 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Lower Molar 2 - TN 2":
            self.molar2 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Lower Molar 3 - TN 3":
            self.molar3 = self.molar3
        elif diagnosis == "Moderate" and toothnumber=="Lower Molar 3 - TN 3":
            self.molar3 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Lower Molar 3 - TN 3":
            self.molar3 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber == "Lower Premolar 1 - TN 4":
            self.premolarl1 = self.premolarl1
        elif diagnosis =="Moderate" and toothnumber == "Lower Premolar 1 - TN 4":
            self.premolarl1 = self.premolarmoderatel
        elif diagnosis =="Severe" and toothnumber == "Lower Premolar 1 - TN 4":
            self.premolarl1 = self.premolarseverel
        elif diagnosis == "Normal" and toothnumber == "Lower Premolar 2 - TN 5":
            self.premolarl2 = self.premolarl2
        elif diagnosis == "Moderate" and toothnumber == "Lower Premolar 2 - TN 5":
            self.premolarl2 = self.premolarmoderatel
        elif diagnosis == "Severe" and toothnumber == "Lower Premolar 2 - TN 5":
            self.premolarl2 = self.premolarseverel
        elif diagnosis =="Normal" and toothnumber == "Lower Canine 1 - TN 6":
            self.caninel1 = self.caninel1
        elif diagnosis == "Moderate" and toothnumber == "Lower Canine 1 - TN 6":
            self.caninel1 = self.caninemoderatel
        elif diagnosis =="Severe" and toothnumber == "Lower Canine 1 - TN 6":
            self.caninel1 = self.canineseverel
        elif diagnosis == "Normal" and toothnumber == "Lower Incisor 1 - TN 7":
            self.incisorl1 = self.incisorl1
        elif diagnosis == "Moderate" and toothnumber =="Lower Incisor 1 - TN 7":
            self.incisorl1 = self.incisormoderatel
        elif diagnosis == "Severe" and toothnumber == "Lower Incisor 1 - TN 7":
            self.incisorl1  = self.incisorseverel
        elif diagnosis == "Normal" and toothnumber == "Lower Incisor 2 - TN 8":
            self.incisorl2 = self.incisorl2
        elif diagnosis == "Moderate" and toothnumber =="Lower Incisor 2 - TN 8":
            self.incisorl2 = self.incisormoderatel
        elif diagnosis == "Severe" and toothnumber == "Lower Incisor 2 - TN 8":
            self.incisorl2  = self.incisorseverel
        elif diagnosis == "Normal" and toothnumber == "Lower Incisor 3 - TN 9":
            self.incisorl3 = self.incisorl3
        elif diagnosis == "Moderate" and toothnumber =="Lower Incisor 3 - TN 9":
            self.incisorl3 = self.incisormoderatel
        elif diagnosis == "Severe" and toothnumber == "Lower Incisor 3 - TN 9":
            self.incisorl3  = self.incisorseverel
        elif diagnosis == "Normal" and toothnumber == "Lower Incisor 4 - TN 10":
            self.incisorl4 = self.incisorl4
        elif diagnosis == "Moderate" and toothnumber =="Lower Incisor 4 - TN 10":
            self.incisorl4 = self.incisormoderatel
        elif diagnosis == "Severe" and toothnumber == "Lower Incisor 4 - TN 10":
            self.incisorl4  = self.incisorseverel
        elif diagnosis =="Normal" and toothnumber == "Lower Canine 2 - TN 11":
            self.caninel2 = self.caninel2
        elif diagnosis == "Moderate" and toothnumber == "Lower Canine 2 - TN 11":
            self.caninel2 = self.caninemoderatel
        elif diagnosis =="Severe" and toothnumber == "Lower Canine 2 - TN 11":
            self.caninel2 = self.canineseverel
        elif diagnosis == "Normal" and toothnumber == "Lower Premolar 3 - TN 12":
            self.premolarl3 = self.premolarl3
        elif diagnosis =="Moderate" and toothnumber == "Lower Premolar 3 - TN 12":
            self.premolarl3 = self.premolarmoderatel
        elif diagnosis =="Severe" and toothnumber == "Lower Premolar 3 - TN 12":
            self.premolarl3 = self.premolarseverel
        elif diagnosis == "Normal" and toothnumber == "Lower Premolar 4 - TN 13":
            self.premolarl4 = self.premolarl4
        elif diagnosis == "Moderate" and toothnumber == "Lower Premolar 4 - TN 13":
            self.premolarl4 = self.premolarmoderatel
        elif diagnosis == "Severe" and toothnumber == "Lower Premolar 4 - TN 13":
            self.premolarl4 = self.premolarseverel
        elif diagnosis == "Normal" and toothnumber =="Lower Molar 4 - TN 14":
            self.molar4 = self.molar4
        elif diagnosis == "Moderate" and toothnumber=="Lower Molar 4 - TN 14":
            self.molar4 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Lower Molar 4 - TN 14":
            self.molar4 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Lower Molar 5 - TN 15":
            self.molar5 = self.molar5
        elif diagnosis == "Moderate" and toothnumber=="Lower Molar 5 - TN 15":
            self.molar5 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Lower Molar 5 - TN 15":
            self.molar5 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Lower Molar 6 - TN 16":
            self.molar6 = self.molar6
        elif diagnosis == "Moderate" and toothnumber=="Lower Molar 6 - TN 16":
            self.molar6 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Lower Molar 6 - TN 16":
            self.molar6 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Upper Molar 1 - TN 17":
            self.molar7 = self.molar7
        elif diagnosis == "Moderate" and toothnumber=="Upper Molar 1 - TN 17":
            self.molar7 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Upper Molar 1 - TN 17":
            self.molar7 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Upper Molar 2 - TN 18":
            self.molar8 = self.molar8
        elif diagnosis == "Moderate" and toothnumber=="Upper Molar 2 - TN 18":
            self.molar8 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Upper Molar 2 - TN 18":
            self.molar8 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Upper Molar 3 - TN 19":
            self.molar9 = self.molar9
        elif diagnosis == "Moderate" and toothnumber=="Upper Molar 3 - TN 19":
            self.molar9 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber == "Upper Molar 3 - TN 19":
            self.molar9 = self.molarsevere
        elif diagnosis =="Normal" and toothnumber == "Upper Premolar 1 - TN 20":
            self.premolar1 = self.premolar1
        elif diagnosis =="Moderate" and toothnumber == "Upper Premolar 1 - TN 20":
            self.premolar1 = self.premolarmoderate
        elif diagnosis == "Severe" and toothnumber == "Upper Premolar 1 - TN 20":
            self.premolar1 = self.premolarsevere
        elif diagnosis =="Normal" and toothnumber == "Upper Premolar 2 - TN 21":
            self.premolar2 = self.premolar2
        elif diagnosis =="Moderate" and toothnumber == "Upper Premolar 2 - TN 21":
            self.premolar2 = self.premolarmoderate
        elif diagnosis == "Severe" and toothnumber == "Upper Premolar 2 - TN 21":
            self.premolar2 = self.premolarsevere
        elif diagnosis =="Normal" and toothnumber == "Upper Canine 1 - TN 22":
            self.canine1 = self.canine1
        elif diagnosis =="Moderate" and toothnumber =="Upper Canine 1 - TN 22":
            self.canine = self.caninemoderate
        elif diagnosis == "Severe" and toothnumber =="Upper Canine 1 - TN 22":
            self.canine1 = self.caninesevere
        elif diagnosis == "Normal" and toothnumber =="Upper Incisor 1 - TN 23":
            self.incisor1 = self.incisor1
        elif diagnosis == "Moderate" and toothnumber =="Upper Incisor 1 - TN 23":
            self.incisor1 = self.incisormoderate
        elif diagnosis == "Severe" and toothnumber =="Upper Incisor 1 - TN 23":
            self.incisor1 = self.incisorsevere
        elif diagnosis == "Normal" and toothnumber =="Upper Incisor 2 - TN 24":
            self.incisor2 = self.incisor2
        elif diagnosis == "Moderate" and toothnumber =="Upper Incisor 2 - TN 24":
            self.incisor2 = self.incisormoderate
        elif diagnosis == "Severe" and toothnumber =="Upper Incisor 2 - TN 24":
            self.incisor2 = self.incisorsevere
        elif diagnosis == "Normal" and toothnumber =="Upper Incisor 3 - TN 25":
            self.incisor3 = self.incisor3
        elif diagnosis == "Moderate" and toothnumber =="Upper Incisor 3 - TN 25":
            self.incisor3 = self.incisormoderate
        elif diagnosis == "Severe" and toothnumber =="Upper Incisor 3 - TN 25":
            self.incisor3 = self.incisorsevere
        elif diagnosis == "Normal" and toothnumber =="Upper Incisor 4 - TN 26":
            self.incisor4 = self.incisor4
        elif diagnosis == "Moderate" and toothnumber =="Upper Incisor 4 - TN 26":
            self.incisor4 = self.incisormoderate
        elif diagnosis == "Severe" and toothnumber =="Upper Incisor 4 - TN 26":
            self.incisor4 = self.incisorsevere
        elif diagnosis == "Normal" and toothnumber == "Upper Canine 2 - TN 27":
            self.canine2 = self.canine2
        elif diagnosis == "Moderate" and toothnumber == "Upper Canine 2 - TN 27":
            self.canine2 = self.caninemoderate
        elif diagnosis == "Severe" and toothnumber == "Upper Canine 2 - TN 27":
            self.canine2 = self.caninesevere
        elif diagnosis =="Normal" and toothnumber == "Upper Premolar 3 - TN 28":
            self.premolar1 = self.premolar1
        elif diagnosis =="Moderate" and toothnumber == "Upper Premolar 3 - TN 28":
            self.premolar1 = self.premolarmoderate
        elif diagnosis == "Severe" and toothnumber == "Upper Premolar 3 - TN 28":
            self.premolar1 = self.premolarsevere
        elif diagnosis =="Normal" and toothnumber == "Upper Premolar 4 - TN 29":
            self.premolar2 = self.premolar2
        elif diagnosis =="Moderate" and toothnumber == "Upper Premolar 4 - TN 29":
            self.premolar2 = self.premolarmoderate
        elif diagnosis == "Severe" and toothnumber == "Upper Premolar 4 - TN 29":
            self.premolar2 = self.premolarsevere
        elif diagnosis =="Normal" and toothnumber == "Upper Molar 4 - TN 30":
            self.molar10 = self.molar10
        elif diagnosis =="Moderate" and toothnumber == "Upper Molar 4 - TN 30":
            self.molar10 = self.molarmoderate
        elif diagnosis =="Severe" and toothnumber =="Upper Molar 4 - TN 30":
            self.molar10 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Upper Molar 5 - TN 31":
            self.molar11 = self.molar11
        elif diagnosis == "Moderate" and toothnumber =="Upper Molar 5 - TN 31":
            self.molar11 = self.molarmoderate
        elif diagnosis == "Severe" and toothnumber == "Upper Molar 5 - TN 31":
            self.molar11 = self.molarsevere
        elif diagnosis == "Normal" and toothnumber =="Upper Molar 6 - TN 32":
            self.molar12 = self.molar12
        elif diagnosis == "Moderate" and toothnumber =="Upper Molar 6 - TN 32":
            self.molar12 = self.molarmoderate
        elif diagnosis == "Severe" and toothnumber == "Upper Molar 6 - TN 32":
            self.molar12 = self.molarsevere
        else:
            print("what happen")
    def clearChart(self):
        self.molar1 = self.molarc
        self.molar2 = self.molarc
        self.molar3 = self.molarc
        self.molar4 = self.molarc
        self.molar5 = self.molarc
        self.molar6 = self.molarc
        self.molar7 = self.molarc
        self.molar8 = self.molarc
        self.molar9 = self.molarc
        self.molar10 = self.molarc
        self.molar11 = self.molarc
        self.molar12 = self.molarc
        self.incisorl1 = self.incisorlc
        self.incisorl2 = self.incisorlc
        self.incisorl3 = self.incisorlc
        self.incisorl4 = self.incisorlc
        self.incisor1 = self.incisorc
        self.incisor2 = self.incisorc
        self.incisor3 = self.incisorc
        self.incisor4 = self.incisorc
        self.canine1 = self.caninec
        self.canine2 = self.caninec
        self.caninel1 = self.caninelc
        self.caninel2 = self.caninelc
        self.premolar1 = self.premolarc
        self.premolar2 = self.premolarc
        self.premolar3 = self.premolarc
        self.premolar4 = self.premolarc 
        self.premolarl1 = self.premolarlc
        self.premolarl2 = self.premolarlc
        self.premolarl3 = self.premolarlc
        self.premolarl4 = self.premolarlc
    def dropdown1(self):
        max = 2.85
        self.dtoothnumber.dropdown_cls.max_height = self.dtoothnumber.height * max + max * 2
    def missingtooth(self):
        dtoothnumber = self.dtoothnumber.text
        if dtoothnumber == "Lower Molar 1 - TN 1":
            self.molar1 = self.molarx
        elif dtoothnumber == "Lower Molar 2 - TN 2":
            self.molar2 = self.molarx
        elif dtoothnumber == "Lower Molar 3 - TN 3":
            self.molar3 = self.molarx
        elif dtoothnumber == "Lower Premolar 1 - TN 4":
            self.premolarl1 = self.premolarlx
        elif dtoothnumber == "Lower Premolar 2 - TN 5":
            self.premolarl2 = self.premolarx
        elif dtoothnumber == "Lower Canine 1 - TN 6":
            self.caninel1 = self.caninex
        elif dtoothnumber == "Lower Incisor 1 - TN 7":
            self.incisorl1 = self.incisorlx
        elif dtoothnumber == "Lower Incisor 2 - TN 8":
            self.incisorl2 = self.incisorlx
        elif dtoothnumber == "Lower Incisor 3 - TN 9":
            self.incisorl3 = self.incisorlx
        elif dtoothnumber == "Lower Incisor 4 - TN 10":
            self.incisorl4 = self.incisorlx
        elif dtoothnumber == "Lower Canine 2 - TN 11":
            self.caninel2 = self.caninelx
        elif dtoothnumber == "Lower Premolar 3 - TN 12":
            self.premolarl3 = self.premolarlx
        elif dtoothnumber == "Lower Premolar 4 - TN 13":
            self.premolarl4 = self.premolarlx
        elif dtoothnumber == "Lower Molar 4 - TN 14":
            self.molar4 = self.molarx
        elif dtoothnumber == "Lower Molar 5 - TN 15":
            self.molar5 = self.molarx
        elif dtoothnumber == "Lower Molar 6 - TN 16":
            self.molar6 = self.molarx
        elif dtoothnumber == "Upper Molar 1 - TN 17":
            self.molar7 = self.molarx
        elif dtoothnumber == "Upper Molar 2 - TN 18":
            self.molar8 = self.molarx
        elif dtoothnumber == "Upper Molar 3 - TN 19":
            self.molar9 = self.molarx
        elif dtoothnumber == "Upper Premolar 1 - TN 20":
            self.premolar1 = self.premolarx
        elif dtoothnumber == "Upper Premolar 2 - TN 21":
            self.premolar2 = self.premolarx
        elif dtoothnumber == "Upper Canine 1 - TN 22":
            self.canine1 = self.caninex
        elif dtoothnumber == "Upper Incisor 1- TN 23":
            self.incisor1 = self.incisorx
        elif dtoothnumber == "Upper Incisor 2 - TN 24":
            self.incisor2 = self.incisorx
        elif dtoothnumber == "Upper Incisor 3 - TN 25":
            self.incisor3 = self.incisorx
        elif dtoothnumber == "Upper Incisor 4 - TN 26":
            self.incisor4 = self.incisorx
        elif dtoothnumber == "Upper Canine 2 - TN 27":
            self.canine2 = self.caninex
        elif dtoothnumber == "Upper Premolar 3 - TN 28":
            self.premolar3 = self.premolarx
        elif dtoothnumber == "Upper Premolar 4 - TN 29":
            self.premolar4 = self.premolarx
        elif dtoothnumber == "Upper Molar 4 - TN 30":
            self.molar10 = self.molarx
        elif dtoothnumber == "Upper Molar 5 - TN 31":
            self.molar11 = self.molarx
        elif dtoothnumber == "Upper Molar 6 - TN 32":
            self.molar12 = self.molarx
        else:
            print("Invalid missing tooth name")   
    pass
    def cleartooth(self):
        dtoothnumber = self.dtoothnumber.text
        if dtoothnumber == "Lower Molar 1 - TN 1":
            self.molar1 = self.molarc
        elif dtoothnumber == "Lower Molar 2 - TN 2":
            self.molar2 = self.molarc
        elif dtoothnumber == "Lower Molar 3 - TN 3":
            self.molar3 = self.molarc
        elif dtoothnumber == "Lower Premolar 1 - TN 4":
            self.premolarl1 = self.premolarlc
        elif dtoothnumber == "Lower Premolar 2 - TN 5":
            self.premolarl2 = self.premolarc
        elif dtoothnumber == "Lower Canine 1 - TN 6":
            self.caninel1 = self.caninec
        elif dtoothnumber == "Lower Incisor 1 - TN 7":
            self.incisorl1 = self.incisorlc
        elif dtoothnumber == "Lower Incisor 2 - TN 8":
            self.incisorl2 = self.incisorlc
        elif dtoothnumber == "Lower Incisor 3 - TN 9":
            self.incisorl3 = self.incisorlc
        elif dtoothnumber == "Lower Incisor 4 - TN 10":
            self.incisorl4 = self.incisorlc
        elif dtoothnumber == "Lower Canine 2 - TN 11":
            self.caninel2 = self.caninelc
        elif dtoothnumber == "Lower Premolar 3 - TN 12":
            self.premolarl3 = self.premolarlc
        elif dtoothnumber == "Lower Premolar 4 - TN 13":
            self.premolarl4 = self.premolarlc
        elif dtoothnumber == "Lower Molar 4 - TN 14":
            self.molar4 = self.molarc
        elif dtoothnumber == "Lower Molar 5 - TN 15":
            self.molar5 = self.molarc
        elif dtoothnumber == "Lower Molar 6 - TN 16":
            self.molar6 = self.molarc
        elif dtoothnumber == "Upper Molar 1 - TN 17":
            self.molar7 = self.molarc
        elif dtoothnumber == "Upper Molar 2 - TN 18":
            self.molar8 = self.molarc
        elif dtoothnumber == "Upper Molar 3 - TN 19":
            self.molar9 = self.molarc
        elif dtoothnumber == "Upper Premolar 1 - TN 20":
            self.premolar1 = self.premolarc
        elif dtoothnumber == "Upper Premolar 2 - TN 21":
            self.premolar2 = self.premolarc
        elif dtoothnumber == "Upper Canine 1 - TN 22":
            self.canine1 = self.caninec
        elif dtoothnumber == "Upper Incisor 1- TN 23":
            self.incisor1 = self.incisorc
        elif dtoothnumber == "Upper Incisor 2 - TN 24":
            self.incisor2 = self.incisorc
        elif dtoothnumber == "Upper Incisor 3 - TN 25":
            self.incisor3 = self.incisorc
        elif dtoothnumber == "Upper Incisor 4 - TN 26":
            self.incisor4 = self.incisorc
        elif dtoothnumber == "Upper Canine 2 - TN 27":
            self.canine2 = self.caninec
        elif dtoothnumber == "Upper Premolar 3 - TN 28":
            self.premolar3 = self.premolarc
        elif dtoothnumber == "Upper Premolar 4 - TN 29":
            self.premolar4 = self.premolarc
        elif dtoothnumber == "Upper Molar 4 - TN 30":
            self.molar10 = self.molarc
        elif dtoothnumber == "Upper Molar 5 - TN 31":
            self.molar11 = self.molarc
        elif dtoothnumber == "Upper Molar 6 - TN 32":
            self.molar12 = self.molarc
        else:
            print("Invalid missing tooth name")   
    pass          
class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps=30):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
        return_value, frame = self.capture.read()
        if return_value:
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()
capture = None
class CameraScreen(Screen):
    def init_qrtest(self):
        pass
    def dostart(self, *largs):
        global capture
        capture = cv2.VideoCapture(0)
        self.camera_kivy.start(capture)
    def doexit(self):
        global capture
        global g
        return_value, frame = capture.read()
        cv2.imwrite('toothimages/tooth.png',frame)
        if capture != None:
            capture.release()
            capture = None
            self.manager.current = 'diagnosescreen'
            Cache.remove('kv.image')
            Cache.remove('kv.texture')
class MainScreen(Screen) :
    pass
class AdminRecordScreen(Screen):
    def displayDiagRecordAdmin(self): 
        query.execute("SELECT toothnumber,patientUsername,toothDiagnosis,currentDate FROM `patientrecord`")
        results = query.fetchall()
        db.commit()
        self.scrollview3.content_layout3.clear_widgets()
        for row in results:
            l3 = Label(text= '                                ' + str(row[1]) + '                   '+ str(row[0]) + '                ' + row[2]+ '                    '+row[3],font_size='15sp',color=[0.2627, 0.290, 0.3294, 1])
            self.scrollview3.content_layout3.add_widget(l3)
    def searchDiagnosisRecord(self,searchpatientdiagnosisrecord):
        query.execute("SELECT toothnumber,patientUsername,toothDiagnosis,currentDate FROM `patientrecord` WHERE toothDiagnosis LIKE '%"+searchpatientdiagnosisrecord+"%'")
        results = query.fetchall()
        self.scrollview3.content_layout3.clear_widgets()
        for row in results:
            l3 = Label(text= '                            ' + str(row[1]) + '                   '+ str(row[0]) + '                ' + row[2]+ '                    '+row[3],font_size='15sp',color=[0.2627, 0.290, 0.3294, 1])
            self.scrollview3.content_layout3.add_widget(l3)
    def countnormal(self):
        query.execute("SELECT COUNT(toothDiagnosis) FROM `patientrecord` WHERE toothDiagnosis LIKE 'Normal'")
        results = query.fetchall()
        db.commit()
        for row in results:
            pop8 = Popup(title='Normal Cases', content=Label(text='Total record number of normal cases:'+str(row[0])),size_hint=(None,None),size=(280,100))
            pop8.open()
            print(pop8)
    def countmoderate(self):
        query.execute("SELECT COUNT(toothDiagnosis) FROM `patientrecord` WHERE toothDiagnosis LIKE 'Moderate'")
        results = query.fetchall()
        db.commit()
        for row in results:
            pop9 = Popup(title='Moderate Cases', content=Label(text='Total record number of moderate cases:'+str(row[0])),size_hint=(None,None),size=(280,100))
            pop9.open()

    def countsevere(self):
        query.execute("SELECT COUNT(toothDiagnosis) FROM `patientrecord` WHERE toothDiagnosis LIKE 'Severe'")
        results = query.fetchall()
        db.commit()
        for row in results:
            pop10 = Popup(title='Severe Cases', content=Label(text='Total record number of severe cases:'+str(row[0])),size_hint=(None,None),size=(280,100))
            pop10.open()
class AdminPatientRecordScreen(Screen):
    def displayRecordAdmin(self): 
        query.execute("SELECT firstName,lastName,age,username,contactNum FROM `registeredpatient`")
        results = query.fetchall()
        db.commit()
        self.scrollview2.content_layout2.clear_widgets()
        for row in results:
            l2 = Label(text= '        ' + str(row[3]) + '                     '+ row[0] + '                              ' + row[1]+ '                        '+row[2]+'                           '+row[4],font_size='15sp',color=[0.2627, 0.290, 0.3294, 1])
            self.scrollview2.content_layout2.add_widget(l2)
    def searchPatientInfoRecord(self,searchpatientinforecord):
        query.execute("SELECT firstName,lastName,age,username,contactNum FROM `registeredpatient` WHERE firstName LIKE '%"+searchpatientinforecord+"%' OR lastName LIKE '%"+searchpatientinforecord+"%' OR username LIKE '%"+searchpatientinforecord+"%' ")
        results = query.fetchall()
        self.scrollview2.content_layout2.clear_widgets()
        for row in results:
            l2 = Label(text= '        ' + str(row[3]) + '                     '+ row[0] + '                              ' + row[1]+ '                        '+row[2]+'                           '+row[4],font_size='15sp',color=[0.2627, 0.290, 0.3294, 1])
            self.scrollview2.content_layout2.add_widget(l2)
class Chooser(Screen):
    fileName = StringProperty("/")
    def selected(self,fileName):
        global f
        print (fileName[0])
        self.image = str(fileName[0])
        f = self.image
    pass
class PatientRecordScreen(Screen):
    global patientUser
    patientname1 = StringProperty()
    lastcheckup1 = StringProperty()
    def displayRecord(self): 
        query.execute("SELECT * FROM `patientrecord` WHERE `patientUsername`='"+patientUser+"'")
        results = query.fetchall()
        db.commit()
        self.scrollview1.content_layout1.clear_widgets()
        for row in results:
            l = Label(text= '                                     ' + str(row[2]) + '                             '+ row[3] + '                                 ' + row[4],font_size='15sp',color=[0.2627, 0.290, 0.3294, 1])
            self.scrollview1.content_layout1.add_widget(l)
    def searchDentalRecord(self,searchdentalrecord):
        query.execute("SELECT * FROM `patientrecord` WHERE toothnumber LIKE '%"+searchdentalrecord+"%' OR toothDiagnosis LIKE '%"+searchdentalrecord+"%' OR currentDate LIKE '%"+searchdentalrecord+"%' ")
        results = query.fetchall()
        self.scrollview1.content_layout1.clear_widgets()
        for row in results:
            l = Label(text= '                                     ' + str(row[2]) + '                             '+ row[3] + '                                 ' + row[4],font_size='15sp',color=[0.2627, 0.290, 0.3294, 1])
            self.scrollview1.content_layout1.add_widget(l)
    def displayInfo(self,username):
        query.execute("SELECT * FROM `registeredpatient` WHERE `username`='"+username+"'")
        results = query.fetchall()
        db.commit()
        for row in results:
            self.patientname1 = row[1]
            self.lastcheckup1 = row[9]
class AboutUsScreen(Screen):
    pass
class GuidelineScreen(Screen):
    pass
class ScreenManagement(ScreenManager):
	pass
class mainApp(App):
    def build(self):
        config = self.config
        self.title = "iSMILE- v1.1.0"
        self.root = Builder.load_file('mainApp.kv')
        return self.root
if __name__=='__main__':
    db = MySQLdb.connect(host="localhost",user="root",passwd="admin",db="ismile")
    query = db.cursor()
    mainApp().run()