from datetime import datetime, timedelta
from reader.csvReader import readVaccinations, readTests, readCovidGrow, Vaccination, CovidTest, CovidGrow
from prediction.covidClf import CovidClf
from prediction.prepareData import prepare_learning_and_testing_data

if __name__ == "__main__":
    a = CovidClf()
    data = prepare_learning_and_testing_data()
    a.fit_clf(data[0], data[1])
    a.predict_clf(data[2])
    print(data[3])


    # START_DATE = "2021-04-1"
    # MIN_AUTOCORRELATION_FACTOR = 0.4
    # DAYS_TO_PREDICT = 7

    # corr_data = correlation_data("2021-1-1", START_DATE)

    # start_date = datetime.strptime(START_DATE, '%Y-%m-%d').date()
    # train_start_day = start_date - timedelta(days = TRAIN_SHIFT_DAY)
    # predict(vaccinations, covidDetails, tests, corr_data, train_start_day ,start_date, DAYS_TO_PREDICT)
    
