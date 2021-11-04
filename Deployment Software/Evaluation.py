from LoadRealData import loadinRealData
from LoadData import loadInTrainingData
from LoadModels import loadModels
import time


from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

xOrder =['Lux',
'Infrared',
'Visible',
'Full_Spectrum',
'Temperature',
'Humidity',
'Pressure',
'Accelerometer_x_axis',
'Accelerometer_y_axis',
'Accelerometer_z_axis',
'All_Cores']

def evaluateBehaviourClassificationProgram(xOrder):
    models01, models11, attackClassificationModel = loadModels()

    #XTest, yTest = loadInTrainingData("data/testdata/", xOrder)
    XTest, yTest = loadinRealData("/home/pi/Documents/Original/Deployment Software/data/realdata/", xOrder)

    # THESE LINES SHOULD BE UNCOMMENTED
    verifyAllModels(attackClassificationModel, models01, models11, XTest, yTest)
    classificationReportAll(attackClassificationModel , models01, models11, XTest, yTest)

    print("Starting Evaluation")
    no_potentials0, no_potentials1, no_potentials2 = 0, 0, 0
    correct_no_potentials0, correct_no_potentials1, correct_no_potentials2 = 0, 0, 0
    averageTime = 0
    for i, x in enumerate(XTest):
        start_time = time.time()
        answer, numberOfPotential = checkModels(models01, models11, attackClassificationModel, x)
        if (numberOfPotential == 0):
            no_potentials0 += 1
            if (answer == yTest[i]):
                correct_no_potentials0 += 1
        elif(numberOfPotential == 1):
            no_potentials1 += 1
            if (answer == yTest[i]):
                correct_no_potentials1 += 1
        else:
            no_potentials2 += 1
            if (answer == yTest[i]):
                correct_no_potentials2 += 1

        end_time = time.time()
        averageTime = averageTime + ((end_time - start_time - averageTime)/(i+1))
        time_convert(averageTime * (len(XTest)-i))
        

    correct = correct_no_potentials0 + correct_no_potentials1 + correct_no_potentials2
    print("Accuracy of system: " + str(correct*100/len(XTest)) + "%")
    print("Number of unknown attacks: " + str(no_potentials0) + " of which " + str(correct_no_potentials0) + " were correct")
    print("Number of single potential attacks: " + str(no_potentials1) + " of which " + str(correct_no_potentials1) + " were correct")
    print("Number of conflicting results: " + str(no_potentials2) + " of which " + str(correct_no_potentials2) + " were correct")

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    #print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

def checkModels(models01, models11, attackClassificationModel, x):
    x = x.reshape(1,-1)

    #model01 means 0 is in and 1 is out
    #model11 means 1 is in and -1 is out
    potentials = []
    for model in models01:
        # If inlier
        if (models01.get(model).predict(x) == 0):
            potentials.append(model)

    for model in models11:
        # If inlier
        if (models11.get(model).predict(x) == 1):
            potentials.append(model)

    #print(len(potentials))
    if (len(potentials) > 1):
        #Overlaps between multiple behaviours
        return attackClassificationModel.predict(x)[0], len(potentials)
    elif (len(potentials) ==  1):
        #Known behaviour
        return potentials[0], 1
    else:
        #Potentially unknown attack
        return "Unknown", 0

def verifyAllModels(attackClassificationModel, models01, models11, XTest, yTest):
    behaviours = list(set(yTest))
    print(behaviours)

    for model in models01:
        print(model)
        for behaviour in behaviours:
            if behaviour in model:
                verifyModels(models01.get(model), XTest, yTest, behaviour, 0)
                continue

    for model in models11:
        print(model)
        for behaviour in behaviours:
            if behaviour in model:
                verifyModels(models11.get(model), XTest, yTest, behaviour, 1)
                continue

    displayAnalytics(attackClassificationModel, XTest, yTest, "Attack Classification")

def verifyModels(model, X, y, behaviour, inline):
    y_pred = model.predict(X)
    i = 0
    correct = 0
    totalNormal = 0
    total1 = 0
    for yitem in y_pred:
        #print(yTest[i], yitem)
        if (y[i] == behaviour):
            totalNormal = totalNormal + 1
        if (inline == yitem):
            total1 = total1 + 1
        if (inline == yitem and y[i] == behaviour):
            correct = correct + 1
        i=i+1
    print("---" + behaviour + "----")
    print("False Negative", str((1-(correct/totalNormal))*100) + "%")
    print("False Positive", str((1-(correct/total1))*100) + "%")

def displayAnalytics(clf, X_test, y_test, name):
    print("Analytical Data For: " + name)
    y_pred = clf.predict(X_test) # store the prediction data
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))
    print(name + "'s Overall Accuracy: " + str(accuracy_score(y_test,y_pred))) # calculate the accuracys

def classificationReportAll(attackClassificationModel, models01, models11, X, y_test):
    for model in models01:
        print("-------" + model + "-------")
        y_pred = models01.get(model).predict(X)
        yTestFormatted = []
        for yval in y_test:
            if (yval == model):
                yTestFormatted.append(0)
            else:
                yTestFormatted.append(1)
        print(confusion_matrix(yTestFormatted,y_pred))
        #print(classification_report(yTestFormatted,y_pred))
        #print(str(accuracy_score(yTestFormatted,y_pred))) # calculate the accuracys

    for model in models11:
        print("-------" + model + "-------")
        y_pred = models11.get(model).predict(X)
        yTestFormatted = []
        for yval in y_test:
            if (yval == model):
                yTestFormatted.append(1)
            else:
                yTestFormatted.append(-1)
        print(confusion_matrix(yTestFormatted,y_pred))
        #print(classification_report(yTestFormatted,y_pred))
        #print(str(accuracy_score(yTestFormatted,y_pred))) # calculate the accuracys

# Not used anywhere
def XytoSingleClass(X, y):
    i = 0
    returnDataX = []
    returnDatay = []
    for x in X:
        if (y[i] == 0):
            returnDataX.append(x)
            returnDatay.append(y)
        i = i + 1
    return returnDataX, returnDatay

if __name__ == "__main__":
    evaluateBehaviourClassificationProgram(xOrder)
