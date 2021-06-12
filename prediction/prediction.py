import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from reader.csvReader import  CovidTest, CovidGrow, Vaccination
from visualization.CovidVisualisation import CovidVisualisation

HIGH_CORR = 0.5

def choose_columns(vaccinations, covidDetails, tests, corr_data):
    goal = str(CovidGrow.NEW_DAILY_CASES)
    corr_type = 'corrMatrix'

    corr = corr_data[corr_type][goal]
    data = list()
    
    for key in Vaccination:
        if corr[str(key)] > HIGH_CORR or corr[str(key)] < HIGH_CORR:
            data.append([ info[key] for info in vaccinations.values() ])

    for key in CovidGrow:
        if corr[str(key)] > HIGH_CORR or corr[str(key)] < -HIGH_CORR:
            data.append([ info[key] for info in covidDetails.values() ])
    
    for key in CovidTest:
        if corr[str(key)] > HIGH_CORR or corr[str(key)] < -HIGH_CORR:
            data.append([ info[key] for info in tests.values() ])

    return data


def predict(vaccinations, covidDetails, tests, corr_data, train_start_day, prediction_start_date, days_to_predict = 7):
    covid_charts = CovidVisualisation()

    #data
    inputs = choose_columns(vaccinations, covidDetails, tests, corr_data)
    outputs = [ info[CovidGrow.NEW_DAILY_CASES] for info in covidDetails.values() ]

    start = -abs((prediction_start_date - train_start_day).days)
    stop = -days_to_predict
    delta = days_to_predict
    
    #test
    test_out =  outputs[stop:]
    test_in = [x[stop-delta:stop] for x in inputs]
    test_in= [[test_in[i][j] for i in range(len(test_in))] for j in range(len(test_in[0]))]
    sc3 = StandardScaler()
    test_in = sc3.fit_transform(test_in)

    #train
    train_out =  outputs[start+delta:stop]
    train_in = [x[start:stop-delta] for x in inputs]
    train_in = [[train_in[i][j] for i in range(len(train_in))] for j in range(len(train_in[0]))]

    #prepare
    sc = StandardScaler()
    X = train_in
    X = sc.fit_transform(X)
    Y = train_out

    #action
    clf = MLPClassifier(solver='lbfgs',
                        activation='relu',
                        alpha=1e-3,
                        hidden_layer_sizes=(30,30,30),
                        max_iter = 1000,
                        tol = 1e-8,
                        n_iter_no_change = 100
                        )
    clf.fit(X, Y)
        
    prediction = clf.predict( test_in )
    covid_charts.plot_prediction(prediction, test_out, train_out)