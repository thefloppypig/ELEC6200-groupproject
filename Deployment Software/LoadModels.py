import os
from sklearn.svm import SVC
from sklearn import svm, datasets
import joblib
#from pyod.models.hbos import HBOS

# Returns all models
def loadModels():
    root_dir = "/home/pi/Documents/Original/Deployment Software/"
    models01, models11 = loadAnomalyModels(root_dir)
    attackClassificationModel = loadAttackClassifcation(root_dir)
    return models01, models11, attackClassificationModel

# Returns Attack Classifcation model
def loadAttackClassifcation(root_dir):
    return joblib.load(root_dir + "multiclass Algorithm.joblib")

# Returns Anomaly models
def loadAnomalyModels(root_dir):
    files01 = findFiles(root_dir + "Anomaly Models/", ".joblib01")
    files11 = findFiles(root_dir +"Anomaly Models/", ".joblib11")
    models01 = importModels(root_dir +"Anomaly Models/", files01)
    models11 = importModels(root_dir + "Anomaly Models/", files11)
    return models01, models11

# Return list of files names that match "extension" in "directory"
def findFiles(directory, extension):
    return [filename for filename in directory if filename.endswith(extension)]

# Load models
def importModels(directory, files):
    models = {}
    for file in files:
        name = file[:-9]
        models[name] = joblib.load(directory + file)
        print("Loaded " + file)
    return models
