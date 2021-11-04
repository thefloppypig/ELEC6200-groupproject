def generateModels(X_train, y_train):
    models = []
    oneClassModels = []

    knn = generateKNeighbour(X_train, y_train)
    print("KNN Modelled")
    naive = generateNaiveBayesian(X_train, y_train)
    print("Naive Modelled")
    gradient = generateGradientDescent(X_train, y_train)
    print("Gradient Modelled")
    tree = generateDecisionTree(X_train, y_train)
    print("Tree Modelled")
    forest = generateDecisionTree(X_train, y_train)
    print("Forest Modelled")
    models = {"knn":knn, "naive":naive, "gradient":gradient, "tree":tree, "forest":forest}

    oneClassModels = generateOneClassModels(X_train, y_train)
    return models, oneClassModels

def generateOneClassModels(X_train, y_train):
    oneClassModels = {}
    behaviours = list(set(y_train))
    #behaviours = ["Normal"]
    for behaviour in behaviours:
        newYTrain = []
        newXTrain = []
        i = 0
        for yval in y_train:
            if (yval == behaviour):
                newYTrain.append(1)
                newXTrain.append(X_train[i])
            else:
                newYTrain.append(-1)
            i = i + 1
        #oneClassModels[behaviour] = generateKNeighbour(X_train, newYTrain)
        oneClassModels[behaviour] = generateOneClassSVM(X_train)
    print("OneClasses Modelled")
    return oneClassModels

def generateKNeighbourOneClass(X_train):
    from sklearn.neighbors import NearestNeighbors
    clf = NearestNeighbors(n_neighbors = 1, algorithm='ball_tree')
    clf.fit(X_train) # fitting the data
    return clf

def generateOneClassSVM(X_train):
    from sklearn.svm import NuSVC as supportvm
    from sklearn.svm import OneClassSVM
    clf = OneClassSVM(kernel='rbf', nu=0.1).fit(X_train)
    return clf

def generateKNeighbour(X_train, y_train):
    from sklearn.neighbors import KNeighborsClassifier
    clf = KNeighborsClassifier(n_neighbors = 1)
    clf.fit(X_train,y_train) # fitting the data
    return clf

def generateSVM(X_train, y_train):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf')
    clf = model.fit(X_train, y_train)
    return clf

def generateNaiveBayesian(X_train, y_train):
    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB() # create a classifier
    clf.fit(X_train,y_train) # fitting the data
    return clf

def generateGradientDescent(X_train, y_train):
    from sklearn.linear_model import SGDClassifier
    clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5000)
    clf.fit(X_train,y_train) # fitting the data
    return clf

def generateDecisionTree(X_train, y_train):
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    clf.fit(X_train,y_train) # fitting the data
    return clf

def generateRandomForesttClassifier(X_train, y_train):
    from sklearn.ensemble  import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators = 1000, random_state = 42)
    clf.fit(X_train,y_train) # fitting the data
    return clf
