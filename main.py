import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

from datetime import datetime

# Klasy i funkcje przeznaczone do parsowania plików CSV
from reader.csvReader import readVaccinations, readTests, readCovidGrow, Vaccination, CovidTest, CovidGrow

# Klasy i funkcje przeznaczone do predykcji
from prediction.covidClf import CovidClf
from prediction.prepareData import correlation_data, prepare_learning_and_testing_data
from prediction.prediction import predict

# Klasa przeznaczona do obsługi korelacji
from autocorrelation.Correlations import Correlations

# Klasa przeznaczona do wizualizacji
from visualization.CovidVisualisation import CovidVisualisation
import plotly.graph_objects as go
import plotly.express as px

if __name__ == "__main__":
    covid_charts = CovidVisualisation()

    # 1. Przedstawienie sparsowanych danych na wykresach
    ###################################################


    # covid_charts.linear_covid_data_plots(
    # [*[
    #     #Chosen Vaccinations data columns
    #     Vaccination.ALL, 
    #     Vaccination.DAILY,
    #     Vaccination.COMPLETED,
    #     Vaccination.COMPLETED_PERCENT
    # ],
    # *[
    #     #Chosen CovidTests data columns
    #     CovidTest.DAILY_NUMBER_OF_TESTS, 
    #     CovidTest.DAILY_POSITIVE_TESTS, 
    #     CovidTest.DAILY_AVERAGE_NUMBER_OF_TESTS,
    #     CovidTest.DAILY_AVERAGE_PERCENT_OF_POSITIVE_TESTS
    # ],
    # *[
    #     #Chosen CovidGrow data columns
    #     CovidGrow.SUMMED_CASES,
    #     CovidGrow.NEW_DAILY_CASES,
    #     CovidGrow.SUMMED_DEATHS,
    #     CovidGrow.NEW_DAILY_DEATHS,
    #     CovidGrow.NEW_DAILY_RECOVERIES,
    #     CovidGrow.INACTIVE_CASES_SHIFT,
    #     CovidGrow.ACTIVE_CASES_SHIFT,
    #     CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER,
    #     CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER,
    #     CovidGrow.TEMPORARY_ACTIVE_CASES_NUMBER,
    #     CovidGrow.SUMMED_RECOVERIES
    # ]], 
    # datetime(2020, 3, 3), 
    # datetime(2021, 5, 17))


    # 2. Przedstawienie wykresów autokorelacji oraz macierzy korelacji na skalę wszystkich danych
    # (okres czasu mozna zmienić w argumentach funkcji, z tych danych korzystamy na mniejszych przedziałach)
    #########################################################################################################


    # Correlations.correlate(
    # [
    #     #Chosen Vaccinations data columns
    #     Vaccination.ALL, 
    #     Vaccination.DAILY,
    #     Vaccination.COMPLETED,
    #     Vaccination.COMPLETED_PERCENT
    # ],
    # [
    #     #Chosen CovidTests data columns
    #     CovidTest.DAILY_NUMBER_OF_TESTS, 
    #     CovidTest.DAILY_POSITIVE_TESTS, 
    #     CovidTest.DAILY_AVERAGE_NUMBER_OF_TESTS,
    #     CovidTest.DAILY_AVERAGE_PERCENT_OF_POSITIVE_TESTS
    # ],
    # [
    #     #Chosen CovidGrow data columns
    #     CovidGrow.SUMMED_CASES,
    #     CovidGrow.NEW_DAILY_CASES,
    #     CovidGrow.SUMMED_DEATHS,
    #     CovidGrow.NEW_DAILY_DEATHS,
    #     CovidGrow.NEW_DAILY_RECOVERIES,
    #     CovidGrow.INACTIVE_CASES_SHIFT,
    #     CovidGrow.ACTIVE_CASES_SHIFT,
    #     CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER,
    #     CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER,
    #     CovidGrow.TEMPORARY_ACTIVE_CASES_NUMBER,
    #     CovidGrow.SUMMED_RECOVERIES
    # ], 
    # start_date = "2020-03-03", end_date = "2021-05-17", plot=True)


    # 3. Przygotowanie danych do predykcji i predykcja najblizszych dni (ilość wg. uznania)
    # (wraz z danymi, wyświetlony zostaje wykres porównujący dane z predykcji z danymi testowymi)
    ##############################################################################################


    START_DATE = "2021-04-1"
    DAYS_TO_PREDICT = 7

    corr_data = correlation_data("2021-3-1", START_DATE)

    vaccinations = readVaccinations()
    covidDetails = readCovidGrow()
    tests = readTests()

    start_date = datetime.strptime(START_DATE, '%Y-%m-%d').date()
    predict(vaccinations, covidDetails, tests, corr_data, start_date ,start_date, DAYS_TO_PREDICT)


    # 4. Przygotowanie danych do predykcji i predykcja średnich z trzech następnych tygodni
    #########################################################################################################


    # clf = CovidClf()
    # data = prepare_learning_and_testing_data()
    
    # clf.fit_clf(data[0], data[1])
    # prediction = clf.predict_clf(data[2])

    # covid_charts.week_avg_prediction(prediction, data[3])
    
    
    