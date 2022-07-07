from guizero import App, Combo, Text, TextBox, PushButton, Picture, Window, info
from adafruit_servokit import ServoKit
from decimal import Decimal
import mysql.connector, time

#PCA 9685 Constructor for Adafruit Library
kit = ServoKit(channels=16)

#mysql connector for python
con = mysql.connector.connect(
    user="classdash",
    password="classdash",
    host="localhost",
    database="classdash")

#cursor constructor
cursor = con.cursor(buffered = True)

#Fix the physical locker number to the pins of PCA9685
def lockerFix(locker):
    if locker == 1:
        door = 0
        lock = 1
    elif locker == 2:
        door = 4
        lock = 5
    elif locker == 3:
        door = 8
        lock = 9
    elif locker == 4:
        door = 12
        lock = 13
    return [door,lock]

#Database Code Search
def searchCode(inputCode):#Below compares inputCode to DB code field
    queryCode = ('SELECT EXISTS(SELECT * from WebSite_meal WHERE code = %s)')
    find = cursor.execute(queryCode,(inputCode,))
    found = cursor.fetchone()
    if found == (0,):
        return 0
    else:
        return 1

#Database Name Search
def searchName(inputName):#Below compares inputName to DB code field
    queryCode = ('SELECT EXISTS(SELECT * from WebSite_meal WHERE name = %s)')
    find = cursor.execute(queryCode,(inputName,))
    found = cursor.fetchone()
    if found == (0,):
        return 0
    else:
        return 1
    
#App Start Window to start on and resets all
def apw():
    codeBox.clear()
    nameBox.clear()
    inputWindow.hide()
    lockerInfo.hide()
    app.show()
    
#OrderInfo Input Window Allows to input Name or Code
def oiw():
    app.hide()
    inputWindow.show()
    
#CloseLocker Shut Door, Lock and Remove DB entry
def closeLocker(locker):
    queryClose = ('DELETE FROM WebSite_meal Where Locker = %s')
    makeClose = cursor.execute(queryClose,(locker,))
    con.commit()
    kit.servo[(lockerFix(locker)[0])].angle = 90#Close Door
    time.sleep(10)
    kit.servo[(lockerFix(locker)[1])].angle = 90#Lock Locker
    apw();
    
#LockerInfo Window Displays Order Information
def liw(locker):
    inputWindow.hide()
    lockerInfo.show() #Query for name from locker number
    queryName = ('SELECT name from WebSite_meal WHERE Locker = %s')
    findName = cursor.execute(queryName,(locker,))
    foundName = cursor.fetchone()
    name = str(''.join(foundName,))
    lockerName.value =('Buyer is:')+ name
                    #Query for price from locker number
    queryPrice = ('SELECT price from WebSite_meal WHERE Locker = %s')
    findPrice = cursor.execute(queryPrice,(locker,))
    foundPrice = cursor.fetchone()
    price = ''.join(map(str, foundPrice))
    lockerPrice.value = ('Price is: $')+price
                    #Query for food from locker number
    queryFood = ('SELECT food from WebSite_meal WHERE Locker = %s')
    findFood = cursor.execute(queryFood,(locker,))
    foundFood = cursor.fetchone()
    food = str(''.join(foundFood,))
    lockerFood.value = ('Meal Ordered:')+ food
                    #Locker already known
    number = str(locker)
    lockerNumber.value = ('Locker Location:')+number
    lockerInfo.after(8000,closeLocker,(locker,))
    

#Submit Code Field and Check against the DB and if it is not Empty
def submitCode(): #Below checks if empty and longer than 6 chars
    if codeBox.value is codeBox.value.strip() or len(codeBox.value) < 6:
        inputWindow.warn("No Code Entered","Please Enter a 6 Digit Code")
    else:
        inputCode = codeBox.value
        if searchCode(inputCode) == 0: #Checks against the DB
            inputWindow.warn("Invalid Code",
                             "There is no locker with the entered code")
        else:#If Code is in DB Find Locker number and Open after ok is hit
            queryLocker = ('SELECT Locker from WebSite_meal WHERE code = %s')
            find = cursor.execute(queryLocker,(inputCode,))
            found = cursor.fetchone()
            locker = int(''.join(found))
            inputWindow.info("Locker Number", "Your Locker is %d" %locker)
            kit.servo[(lockerFix(locker)[1])].angle = 0#Open Lock
            time.sleep(10)
            kit.servo[(lockerFix(locker)[0])].angle = 0#Open Door
            inputWindow.after(3000,liw,(locker,))
            return 1          

#Submit Name Field and check against the DB and if its not empty
def submitName(): #Below checks for empty field
    if nameBox.value is nameBox.value.strip():
        inputWindow.warn("No Name Entered","Please Enter a Name")
    else:
        inputName = nameBox.value
        if searchName(inputName) == 0: #Checks against the DB
            inputWindow.warn("No Name",
                             "There is no locker with the entered Name")
        else:#If name is in DB find locker number and open after ok is hit
            queryLocker = ('SELECT Locker from WebSite_meal WHERE name = %s')
            find = cursor.execute(queryLocker,(inputName,))
            found = cursor.fetchone()
            locker = int(''.join(found))
            inputWindow.info("Locker Number", "Your Locker is %d" %locker)
            kit.servo[(lockerFix(locker)[0])].angle = 0
            kit.servo[(lockerFix(locker)[1])].angle = 0
            inputWindow.after(3000,liw,(locker,))
            return 1            

#App Start 
app = App(title = "Class Dash", height = 400,
          width = 800, bg = 'white')
intro = Text(app, text = "Welcome to Class Dash", align = 'top')
utsaLogo = Picture(app, image = "/home/pi/ClassDash/static/WebSite/images/UTSAEELogo.png"
                   , width = 325, height = 50)
start = PushButton(app, text = "Start", width = 'fill', height = 'fill', command = oiw)

#Input Window Name or Code for Locker and Unlocking and Opening
inputWindow = Window(app, title = "Input Name or Code", height = 400,
                   width = 800, bg = 'white')
nameText = Text(inputWindow, text = "Enter the Name for the Order", align = 'top')
nameBox = TextBox(inputWindow)
nameSubmit = PushButton(inputWindow, text = "Submit Name", command = submitName)
codeText = Text(inputWindow, text = "Or Enter the Code for the Order", align = 'top')
codeBox = TextBox(inputWindow)
codeSubmit = PushButton(inputWindow, text = "Submit Code", command = submitCode)
cancelButton = PushButton(inputWindow, text = "Cancel", command = apw)

#Locker Info and Closing/Locking
lockerInfo = Window(app, title = "Here's Your Food", height = 400,
                       width = 800, bg = 'white')
lockerFood = Text(lockerInfo, text = "food", align = 'top')
lockerPrice = Text(lockerInfo, text = "price", align = 'top')
lockerName = Text(lockerInfo, text = "name", align = 'top')
lockerNumber = Text(lockerInfo, text = "number", align = 'top')
#Function Calls
lockerInfo.hide()
inputWindow.hide()
app.display()
cursor.close()
con.close()