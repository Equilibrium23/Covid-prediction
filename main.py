from datetime import datetime, timedelta
from reader.csvReader import readVaccinations, readTests, readCovidGrow, Vaccination, CovidTest, CovidGrow
from autocorrelation.Correlations import Correlations, autocorrelation_shift_day
from prediction.prediction import predict

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

if __name__ == "__main__":
    START_DATE = "2021-04-1"
    MIN_AUTOCORRELATION_FACTOR = 0.4
    DAYS_TO_PREDICT = 7

    corr_data = correlation_data("2021-1-1", START_DATE)
    TRAIN_SHIFT_DAY = autocorrelation_shift_day(MIN_AUTOCORRELATION_FACTOR, CovidGrow.NEW_DAILY_CASES, corr_data )

    vaccinations = readVaccinations()
    covidDetails = readCovidGrow()
    tests = readTests()

    start_date = datetime.strptime(START_DATE, '%Y-%m-%d').date()
    train_start_day = start_date - timedelta(days = TRAIN_SHIFT_DAY)
    predict(vaccinations, covidDetails, tests, corr_data, train_start_day ,start_date, DAYS_TO_PREDICT)
    
