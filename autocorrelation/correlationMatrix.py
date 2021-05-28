import os
import sys
import pandas as pd
from pandas.core.frame import DataFrame

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from reader.csvReader import readVaccinations, readTests, readCovidGrow
from datetime import datetime

def correlate(paramsVaccinations: list, paramsTests: list, paramsCovidGrow: list, start_date: str, end_date: str) -> dict:
    """
    Parameters:
        paramsVaccinations: list of columns' names (see: Vaccination enum class) 
        paramsTests: list of columns' names (see: CovidTests enum class) 
        paramsCovidGrow: list of columns' names (see: CovidGrow enum class)
        start_date: data starting from this date is take into account
        end_date: data to this date is take into account

    Output:
        Dictionary containing correlation matrix
        Correlation matrix is also printed to text file to increase results clarity
    
    Note:
        Range from start_date to end_date must cover data in ALL columns given as parameters!
        Let's note that data in vaccinations cover shorter period that in other files
    """
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
    

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 0)

    try:
        df = pd.DataFrame(data, columns=[str(x) for x in data.keys()])
        corrMatrix = df.corr()

        with open('autocorrelation/correlation_matrix.txt', 'w') as f:
            print(corrMatrix, file=f)
        
        return corrMatrix.to_dict()

    except ValueError:
        print('Columns lengths are different\nNote: Earliest day in vaccination data is 2020-12-28')
        return []



    
