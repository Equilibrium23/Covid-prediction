import re
import csv
import unicodedata
from enum import Enum
from datetime import datetime

class Vaccination(Enum):
    ALL = 0 # Summed Vaccinations From the Beginning
    DAILY = 1 # Number of vaccinations in example day
    COMPLETED = 2 # Number of vaccinations after 2 doses (or after 1 dose J&J)
    COMPLETED_PERCENT = 3 #Number of vaccinations after 2 doses (or after 1 dose J&J) in % relation to the whole Polish Population

def readVaccinations() -> dict:
    """ Parse szczepienia.csv file.
        Return
        ------
        dict (sorted by date ascending) in format :
            datetime.date() \:
            {
                {
                    Vaccination.ALL \: int,
                    Vaccination.DAILY \: int,
                    Vaccination.COMPLETED \: int, 
                    Vaccination.COMPLETEDPERCENT \: round(float, 5) (e.g 0,2345 means 23,45 %)
                }
            },
            ...
    """

    with open('data/szczepienia.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        next(reader, None) # to skip CSV headers

        result = dict()
        for row in reader:
            date = datetime.strptime(row[0], '%d.%m.%Y').date()
            all_vaccinations = int(unicodedata.normalize("NFKD", row[1]).replace(" ", ""))
            daily_vaccinations = int(unicodedata.normalize("NFKD", row[2]).replace(" ", ""))
            completed_vaccinations = int(unicodedata.normalize("NFKD", row[3]).replace(" ", ""))
            completed_vaccinations_percent = round( float ( row[4].replace("%", "").replace(",", ".") )/100 , 5)
            result[date] = {
                Vaccination.ALL : all_vaccinations,
                Vaccination.DAILY : daily_vaccinations,
                Vaccination.COMPLETED : completed_vaccinations, 
                Vaccination.COMPLETED_PERCENT : completed_vaccinations_percent
            } 

        result = dict(sorted(result.items())) # sort by Date
        return result
    
################################################################################################################
################################################################################################################

class CovidTest(Enum):
    DAILY_NUMBER_OF_TESTS = 0
    DAILY_POSITIVE_TESTS = 1
    DAILY_AVERAGE_NUMBER_OF_TESTS = 2 # DAILY AVERAGE NUMBER OF TESTS from last 7 days
    DAILY_AVERAGE_PERCENT_OF_POSITIVE_TESTS = 3 # DAILY AVERAGE PERCENT OF POSITIVE TESTS from last 7 days

def readTests() -> dict:
    """ Parse testy.csv file.
        Return
        ------
        dict (sorted by date ascending) in format :
            datetime.date() \:
            {
                {
                    CovidTest.DAILY_NUMBER_OF_TESTS \: int > 0 if data is available, -1 otherwise,
                    CovidTest.DAILY_POSITIVE_TESTS \: int > 0,
                    CovidTest.DAILY_AVERAGE_NUMBER_OF_TESTS \: int > 0 if data is available, -1 otherwise,
                    CovidTest.DAILY_AVERAGE_PERCENT_OF_POSITIVE_TESTS \: round(float, 5) > 0 (e.g 0,2345 means 23,45 %) if data is available -1 otherwise
                }
            },
            ...
    """

    with open('data/testy.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        next(reader, None) # to skip CSV headers

        result = dict()
        for row in reader:
            date = datetime.strptime(row[0], '%Y-%m-%d').date()
            try:
                dailyTests = int(unicodedata.normalize("NFKD", row[1]).replace(" ", ""))
            except:
                dailyTests = -1
            dailyPositiveTests = int(unicodedata.normalize("NFKD", row[2]).replace(" ", ""))

            try:
                averageDailyTests = int(unicodedata.normalize("NFKD", row[3]).replace(" ", ""))
            except:
                averageDailyTests = -1
            
            try:
                averageDailyPositiveCasesPerCent = round( float ( row[4].replace("%", "").replace(",", ".") )/100 , 5)
            except:
                averageDailyPositiveCasesPerCent = -1

            result[date] = {
                CovidTest.DAILY_NUMBER_OF_TESTS : dailyTests,
                CovidTest.DAILY_POSITIVE_TESTS : dailyPositiveTests,
                CovidTest.DAILY_AVERAGE_NUMBER_OF_TESTS : averageDailyTests, 
                CovidTest.DAILY_AVERAGE_PERCENT_OF_POSITIVE_TESTS : averageDailyPositiveCasesPerCent
            } 

        result = dict(sorted(result.items())) # sort by Date
        return result

################################################################################################################
################################################################################################################

class CovidGrow(Enum):
    NEW_DAILY_CASES = 0
    NEW_DAILY_DEATHS = 1
    NEW_DAILY_RECOVERIES = 2
    INACTIVE_CASES_SHIFT = 3
    ACTIVE_CASES_SHIFT = 4
    SUMMED_CASES = 5
    SUMMED_DEATHS = 6
    SUMMED_RECOVERIES = 7
    TEMPORARY_INACTIVE_CASES_NUMBER = 8
    TEMPORARY_ACTIVE_CASES_NUMBER = 9

def readCovidGrow() -> dict:
    """ Parse testy.csv file.
        Return
        ------
        dict (sorted by date ascending) in format :
            datetime.date() \:
            {
                {
                    CovidGrow.NEW_DAILY_CASES                 \: int,
                    CovidGrow.NEW_DAILY_DEATHS                \: int,
                    CovidGrow.NEW_DAILY_RECOVERIES            \: int,
                    CovidGrow.INACTIVE_CASES_SHIFT            \: int,
                    CovidGrow.ACTIVE_CASES_SHIFT              \: int,
                    CovidGrow.SUMMED_CASES                    \: int,
                    CovidGrow.SUMMED_DEATHS                   \: int,
                    CovidGrow.SUMMED_RECOVERIES               \: int,
                    CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER \: int,
                    CovidGrow.TEMPORARY_ACTIVE_CASES_NUMBER   \: int
                }
            },
            ...
    """

    with open('data/wzrost.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        next(reader, None) # to skip CSV headers

        result = dict()
        for row in reader:
            date = datetime.strptime(row[0], '%Y-%m-%d').date()
            new_daily_cases = int ( re.sub("\+| ","",unicodedata.normalize("NFKD", row[1])) )
            new_daily_deaths = int ( re.sub("\+| ","",unicodedata.normalize("NFKD", row[2])) )
            new_daily_recoveries = int ( re.sub("\+| ","",unicodedata.normalize("NFKD", row[3])) )
            inactive_cases_shift = int ( re.sub("\+| ","",unicodedata.normalize("NFKD", row[4])) )
            active_cases_shift = int ( re.sub("\+| ","",unicodedata.normalize("NFKD", row[5])) )
            summed_cases = int(row[6])
            summed_deaths = int (row[7])
            summed_recoveries = int (row[8])
            temporary_inactive_cases_number = int (row[9])
            temporary_active_cases_number = int (row[10])

            result[date] = {
                CovidGrow.NEW_DAILY_CASES                 : new_daily_cases,
                CovidGrow.NEW_DAILY_DEATHS                : new_daily_deaths,
                CovidGrow.NEW_DAILY_RECOVERIES            : new_daily_recoveries,
                CovidGrow.INACTIVE_CASES_SHIFT            : inactive_cases_shift,
                CovidGrow.ACTIVE_CASES_SHIFT              : active_cases_shift,
                CovidGrow.SUMMED_CASES                    : summed_cases,
                CovidGrow.SUMMED_DEATHS                   : summed_deaths,
                CovidGrow.SUMMED_RECOVERIES               : summed_recoveries,
                CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER : temporary_inactive_cases_number,
                CovidGrow.TEMPORARY_ACTIVE_CASES_NUMBER   : temporary_active_cases_number
            } 

        result = dict(sorted(result.items())) # sort by Date
        return result