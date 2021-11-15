from SensorData import SensorData
from GraphClass import outputVerificationGraph
from LoadData import loadInTrainingData, getSensorData, sensorToXY, generateXOrder
from MachineLearning import generateModels
from LoadRealData import loadinRealData, removeUselessSensors, convertSensorArrayIntoXYFormat
from sklearn.model_selection import train_test_split
import joblib
import os

def displayAnalytics(clf, X_test, y_test, name):
    print("Analytical Data For: " + name)
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    y_pred = clf.predict(X_test) # store the prediction data
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))
    print(name + "'s Overall Accuracy: " + str(accuracy_score(y_test,y_pred))) # calculate the accuracys

def generateOneClassYData(entry, y_data):
    newYTest = []
    i = 0
    for yval in y_data:
        if (yval == entry):
            newYTest.append(1)
        else:
            newYTest.append(-1)
        i = i + 1
    return newYTest

def main():
    #Hardcoded xOrder
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

    #Load in other datasets
    X, y = loadInTrainingData("../data/workingdata/", xOrder)
    XTest, yTest = loadInTrainingData("../data/testdata/", xOrder)
    XReal, yReal = loadinRealData("../data/realdata/", xOrder)

    print("Data Sets Loaded")

    #Generate testing and training data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=9)

    #Generate Machine Learning Models
    models, oneClassModels = generateModels(X_train, y_train)

    # Save Generated Models in this directory
    save_directory = "Saved Models/"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for entry in oneClassModels:
        model = oneClassModels.get(entry)
        filename = save_directory + str(entry) + '.joblib11'
        joblib.dump(model, filename)
        print(entry + " saved")

    for entry in models:
        model = models.get(entry)
        filename = save_directory + str(entry) + '.joblib'
        joblib.dump(model, filename)
        print(entry + " saved")

    for entry in oneClassModels:
        model = oneClassModels.get(entry)
        print("______________________________________")
        print("-----------Training Data--------------")
        newYTest = generateOneClassYData(entry, y_test)
        displayAnalytics(model, X_test, newYTest, entry)
        print("-----------Real Data------------------")
        newYTest = generateOneClassYData(entry, yReal)
        displayAnalytics(model, XReal, newYTest, entry)
        print("-----------Simulation Data------------")
        newYTest = generateOneClassYData(entry, yTest)
        displayAnalytics(model, XTest, newYTest, entry)

    #Generate Analytics For Models
    for entry in models:
        model = models.get(entry)
        print("______________________________________")
        print("-----------Training Data--------------")
        displayAnalytics(model, X_test, y_test, entry)
        print("-----------Real Data------------------")
        displayAnalytics(model, XReal, yReal, entry)
        print("-----------Simulation Data------------")
        displayAnalytics(model, XTest, yTest, entry)

if __name__ == "__main__":
    main()
