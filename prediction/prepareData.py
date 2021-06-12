import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from statistics import mean
from datetime import datetime, timedelta 

from autocorrelation.Correlations import Correlations
from reader.csvReader import readVaccinations, readTests, readCovidGrow, Vaccination, CovidTest, CovidGrow

def correlation_data( START_DATE, END_DATE ):
    return Correlations.correlate(
    [
        #Chosen Vaccinations data columns
        Vaccination.ALL, 
        Vaccination.DAILY,
        Vaccination.COMPLETED,
        Vaccination.COMPLETED_PERCENT
    ],
    [
        #Chosen CovidTests data columns
        CovidTest.DAILY_NUMBER_OF_TESTS, 
        CovidTest.DAILY_POSITIVE_TESTS, 
        CovidTest.DAILY_AVERAGE_NUMBER_OF_TESTS,
        CovidTest.DAILY_AVERAGE_PERCENT_OF_POSITIVE_TESTS
    ],
    [
        #Chosen CovidGrow data columns
        CovidGrow.SUMMED_CASES,
        CovidGrow.NEW_DAILY_CASES,
        CovidGrow.SUMMED_DEATHS,
        CovidGrow.NEW_DAILY_DEATHS,
        CovidGrow.NEW_DAILY_RECOVERIES,
        CovidGrow.INACTIVE_CASES_SHIFT,
        CovidGrow.ACTIVE_CASES_SHIFT,
        CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER,
        CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER,
        CovidGrow.TEMPORARY_ACTIVE_CASES_NUMBER,
        CovidGrow.SUMMED_RECOVERIES
    ], 
    start_date = START_DATE, end_date = END_DATE, plot=False)


def weekly_average_of_covid_new_cases(covid_data):
    """
    result in format:
    {
       datetime.date(2020, 3, 2): avg from next week, 
       datetime.date(2020, 3, 9): avg from next week,
       ... 
    }
    """
    temp_train_date = datetime.strptime("2020-03-02", '%Y-%m-%d').date()
    train_end_date = datetime.strptime("2021-05-17", '%Y-%m-%d').date()
    result = dict()

    while (train_end_date - temp_train_date).days > 0:
        result[temp_train_date] = mean( [ y[CovidGrow.NEW_DAILY_CASES] for x,y in covid_data.items() if temp_train_date <= x <= temp_train_date + timedelta(days = 7) ] )
        temp_train_date += timedelta(days = 7)
    
    return result


HIGH_CORR = 0.75

def choose_columns(corr_data):
    goal = str(CovidGrow.NEW_DAILY_CASES)
    corr_type = 'corrMatrix'

    corr = corr_data[corr_type][goal]
    data = dict()

    data[Vaccination] = []
    data[CovidGrow] = []
    data[CovidTest] = []

    for key in Vaccination:
        if corr[str(key)] > HIGH_CORR or corr[str(key)] < -HIGH_CORR:
            data[Vaccination].append(key)

    for key in CovidGrow:
        if corr[str(key)] > HIGH_CORR or corr[str(key)] < -HIGH_CORR:
            data[CovidGrow].append(key)
    
    for key in CovidTest:
        if corr[str(key)] > HIGH_CORR or corr[str(key)] < -HIGH_CORR:
            data[CovidTest].append(key)

    return data


def prepare_learning_and_testing_data():

    ##### set up
    vaccinations = readVaccinations()
    covidDetails = readCovidGrow()
    tests = readTests()

    TRAIN_START_DAY = "2020-12-28"
    TRAIN_END_DAY = "2021-04-19"
    TRAIN_NUMBER_OF_WEEKS = 1
    corr_data = correlation_data( TRAIN_START_DAY, TRAIN_END_DAY )

    chosen_columns = choose_columns(corr_data)

    output = weekly_average_of_covid_new_cases(covidDetails)

    ##### train
    temp_train_date = datetime.strptime(TRAIN_START_DAY, '%Y-%m-%d').date()
    train_end_date = datetime.strptime(TRAIN_END_DAY, '%Y-%m-%d').date()
    train_input = [ [] for x in range( ( train_end_date - temp_train_date).days // (TRAIN_NUMBER_OF_WEEKS * 7)) ]

    period = 0
    while (train_end_date - temp_train_date).days > 0 and ( temp_train_date + timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS)) <= train_end_date:
        for column in chosen_columns[Vaccination]:
            train_input[period].append( mean( [ value[column] for date,value in vaccinations.items() if temp_train_date <= date <= temp_train_date + timedelta(days = TRAIN_NUMBER_OF_WEEKS * 7)  ]) )

        for column in chosen_columns[CovidGrow]:
            train_input[period].append( mean([ value[column] for date,value in covidDetails.items() if temp_train_date <= date <= temp_train_date + timedelta(days = TRAIN_NUMBER_OF_WEEKS * 7)  ]) )

        for column in chosen_columns[CovidTest]:
            train_input[period].append( mean([ value[column] for date,value in tests.items() if temp_train_date <= date <= temp_train_date + timedelta(days = TRAIN_NUMBER_OF_WEEKS * 7)  ] ))

        temp_train_date += timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS)

        period += 1


    temp_train_date = datetime.strptime(TRAIN_START_DAY, '%Y-%m-%d').date()
    temp_train_date += timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS)
    train_output = []
    for date, average_new_covid_cases in output.items():
        if date == temp_train_date :
            train_output.append(output[date])
            if temp_train_date + timedelta(days = 7 * ( TRAIN_NUMBER_OF_WEEKS )) <= train_end_date:
                temp_train_date += timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS)

    train_output =  [int(x) for x in train_output]
    ##### test
    temp_test_date = datetime.strptime(TRAIN_END_DAY, '%Y-%m-%d').date()
    test_end_date = datetime.strptime("2021-05-17", '%Y-%m-%d').date()
    test_input = [ [] for x in range( ( test_end_date - temp_test_date).days // (TRAIN_NUMBER_OF_WEEKS * 7)) ]

    period = 0
    while (test_end_date - temp_test_date).days > 0 and ( temp_test_date + timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS)) <= test_end_date:
        if temp_test_date + timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS) in output:
            for column in chosen_columns[Vaccination]:
                test_input[period].append( mean([ value[column] for date,value in vaccinations.items() if temp_test_date <= date <= temp_test_date + timedelta(days = TRAIN_NUMBER_OF_WEEKS * 7)  ]) )

            for column in chosen_columns[CovidGrow]:
                test_input[period].append( mean([ value[column] for date,value in covidDetails.items() if temp_test_date <= date <= temp_test_date + timedelta(days = TRAIN_NUMBER_OF_WEEKS * 7)  ]) )

            for column in chosen_columns[CovidTest]:
                test_input[period].append( mean([ value[column] for date,value in tests.items() if temp_test_date <= date <= temp_test_date + timedelta(days = TRAIN_NUMBER_OF_WEEKS * 7)  ]) )

        temp_test_date += timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS)

        period += 1

    test_input = [x for x in test_input if x != []]

    temp_test_date = datetime.strptime(TRAIN_END_DAY, '%Y-%m-%d').date()
    temp_test_date += timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS)
    test_output = []
    for date, _ in output.items():
        
        if date == temp_test_date:
            test_output.append(output[date])
            if temp_test_date + timedelta(days = 7 * ( TRAIN_NUMBER_OF_WEEKS )) <= test_end_date:
                temp_test_date += timedelta(days = 7 * TRAIN_NUMBER_OF_WEEKS)

    return (train_input, train_output, test_input, test_output)