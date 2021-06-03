import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from sklearn.neural_network import MLPClassifier
from reader.csvReader import  CovidTest, CovidGrow, Vaccination
from datetime import datetime
from sklearn.preprocessing import StandardScaler




def predict(data, vac, tests):
    a = [ info[CovidGrow.NEW_DAILY_CASES] for info in data.values() ]

    b = [ info[Vaccination.ALL] for info in vac.values() ]
    c = [ info[CovidTest.DAILY_NUMBER_OF_TESTS] for info in tests.values() ] 
    test_a =  a[-14:]

    test_c = c[-14:] 
    test_b = b[-14:]

    testing = [[test_b[i],test_c[i]] for i in range(len(test_b)) ]
    sc3 = StandardScaler()
    testing = sc3.fit_transform(testing)

    a = a[-60:-14]
    b = b[-60:-14]
    c = c[-60:-14]

    X = [ [b[i],c[i]] for i in range(len(b)) ]

    sc = StandardScaler()
    X = sc.fit_transform(X)

    Y = a 
    # sc2 = StandardScaler()
    # Y = sc2.fit_transform(Y)

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(15, 2), random_state=1, max_iter = 10000)  
    clf.fit(X, Y)
        
    print(clf.predict( testing ))
    print(test_a)


    