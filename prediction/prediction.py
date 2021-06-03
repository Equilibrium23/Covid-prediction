import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from sklearn.neural_network import MLPClassifier
from reader.csvReader import  CovidTest, CovidGrow, Vaccination
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from pandas.core.frame import DataFrame


def predict(covidDetails, vaccinations, tests):
    #data
    start = -35
    stop = -7
    delta = -stop
    data = list()
    results = [ info[CovidGrow.NEW_DAILY_CASES] for info in covidDetails.values() ]

    data.append([ info[Vaccination.ALL] for info in vaccinations.values() ])
    data.append([ info[Vaccination.DAILY] for info in vaccinations.values() ])
    data.append([ info[Vaccination.COMPLETED_PERCENT] for info in vaccinations.values() ])
    #data.append([ info[Vaccination.COMPLETED] for info in vaccinations.values() ])

    data.append([ info[CovidTest.DAILY_NUMBER_OF_TESTS] for info in tests.values() ])
    #data.append([ info[CovidTest.DAILY_POSITIVE_TESTS] for info in tests.values() ])

    data.append([ info[CovidGrow.NEW_DAILY_RECOVERIES] for info in covidDetails.values() ])
    data.append([ info[CovidGrow.SUMMED_DEATHS] for info in covidDetails.values() ])
    #data.append([ info[CovidGrow.TEMPORARY_ACTIVE_CASES_NUMBER] for info in covidDetails.values() ])
    #data.append([ info[CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER] for info in covidDetails.values() ])
    
    data.append(results)

    #test
    test_res =  results[stop:]
    test_data = [x[stop-delta:stop] for x in data]
    test_data = [[test_data[i][j] for i in range(len(test_data))] for j in range(len(test_data[0]))]
    sc3 = StandardScaler()
    test_data = sc3.fit_transform(test_data)

    #train
    train_res =  results[start+delta:stop]
    train_data = [x[start:stop-delta] for x in data]
    train_data = [[train_data[i][j] for i in range(len(train_data))] for j in range(len(train_data[0]))]

    #prepare
    sc = StandardScaler()
    X = train_data
    X = sc.fit_transform(X)
    Y = train_res

    #action
    clf = MLPClassifier(solver='lbfgs',
                        activation='logistic',
                        alpha=1e-3,
                        hidden_layer_sizes=(20,20,20),
                        max_iter = 100,
                        tol = 1e-8,
                        n_iter_no_change = 100
                        )
    clf.fit(X, Y)
        
    xd = clf.predict( test_data )

    #plot
    df = DataFrame([test_res, xd])
    print(df.T)
    fig = px.line(df.T)
    fig.show()


    