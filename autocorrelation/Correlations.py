import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from reader.csvReader import readVaccinations, readTests, readCovidGrow
from visualization.CovidVisualisation import CovidVisualisation




def autocorrelation_shift_day(MIN_AUTOCORRELATION_FACTOR: float, covid_type, autocorrelation ):
    result_day_numbers = 0
    for day_number, autocorr in autocorrelation["autoCorr"][str(covid_type)].items():
        if autocorr < MIN_AUTOCORRELATION_FACTOR:
            break
        result_day_numbers = day_number
    return result_day_numbers

class Correlations:

    @staticmethod
    def correlate(paramsVaccinations: list, paramsTests: list, paramsCovidGrow: list, start_date: str, end_date: str, plot: bool) -> dict:
        """
        Parameters:
            paramsVaccinations: list of columns' names (see: Vaccination enum class) 
            paramsTests: list of columns' names (see: CovidTests enum class) 
            paramsCovidGrow: list of columns' names (see: CovidGrow enum class)
            start_date: data starting from this date is take into account
            end_date: data to this date is take into account
            plot: bool indicationg if data should be plotted

        Output:
            Dictionary containing correlation matrix and autocorrelation data of given parameters
            Correlation matrix is also printed to text file to increase results clarity
            All linear graphs as well as correlation matrix are also printed using plotly
        
        Note:
            Range from start_date to end_date must cover data in ALL columns given as parameters!
            Let's note that data in vaccinations cover shorter period that in other files
        """
        data = Correlations.__prepare_data(paramsVaccinations, paramsTests, paramsCovidGrow, start_date, end_date)

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 0)

        try:
            corrMatrix = Correlations.__correlate(data)
            autoCorr = Correlations.__autocorr(data)

            with open('autocorrelation/correlations.txt', 'w') as f:
                print('---CORRELATION MATRIX---\n', file=f)
                print(corrMatrix, file=f)
                print('\n---AUTOCORRELATION DATA---\n', file=f)
                print(autoCorr, file=f)
            
            if plot:
                covid_charts = CovidVisualisation()
                start = start_date.split('-')
                end = end_date.split('-')

                covid_charts.linear_covid_data_plots([*paramsVaccinations, *paramsTests, *paramsCovidGrow], 
                                        datetime(int(start[0]), int(start[1]), int(start[2])), 
                                        datetime(int(end[0]), int(end[1]), int(end[2])))
                
                covid_charts.linear_autocorrelation_plots(autoCorr.to_dict())
                covid_charts.correlation_matrix_plot(corrMatrix)

            return {'autoCorr': autoCorr.to_dict(), 'corrMatrix': corrMatrix.to_dict()}

        except ValueError:
            print('Columns lengths are different\nNote: Earliest day in vaccination data is 2020-12-28')
            return []
    
    @staticmethod
    def __autocorr(data: dict) -> pd.DataFrame:
        corr_data = {}

        for key in data.keys():
            column = [float(x) for x in data[key]]
            result = np.correlate(column, column, mode='full')
            result = result[result.size // 2:]
            corr_data[key] = result / result.max()

        return pd.DataFrame(corr_data, columns=[str(x) for x in corr_data.keys()])
    
    @staticmethod
    def __correlate(data: dict) -> pd.DataFrame:
        df = pd.DataFrame(data, columns=[str(x) for x in data.keys()])
        return df.corr()

    @staticmethod
    def __prepare_data(paramsVaccinations: list, paramsTests: list, paramsCovidGrow: list, start_date: str, end_date: str) -> list:
        data = {}
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        vaccinations = readVaccinations()
        for parameter in paramsVaccinations: 
            column = []
            for date, vaccinationsData in vaccinations.items():
                if date >= start_date and date <= end_date:
                    column.append(vaccinationsData[parameter])
            
            data[str(parameter)] = column
        
        tests = readTests()
        for parameter in paramsTests: 
            column = []
            for date, testsData in tests.items():
                if date >= start_date and date <= end_date:
                    column.append(testsData[parameter])
            
            data[str(parameter)] = column
        
        covidDetails = readCovidGrow()
        for parameter in paramsCovidGrow: 
            column = []
            for date, covidData in covidDetails.items():
                if date >= start_date and date <= end_date:
                    column.append(covidData[parameter])
            
            data[str(parameter)] = column
        
        return data

    


        
