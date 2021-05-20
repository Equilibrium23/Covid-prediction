from reader.csvReader import readVaccinations, readTests, Vaccination, CovidTest, CovidGrow, readCovidGrow

if __name__ == "__main__":
    vaccinations = readVaccinations()
    # for date, vaccinationsData in vaccinations.items():
    #     print(date)
    #     print(vaccinationsData[Vaccination.ALL])
    #     print(vaccinationsData[Vaccination.DAILY])
    #     print(vaccinationsData[Vaccination.COMPLETED])
    #     print(vaccinationsData[Vaccination.COMPLETED_PERCENT])
    #     print() 
    # example print to show you how output looks like
    
    tests = readTests()
    # for date, vaccinationsData in tests.items():
    #     print(date)
    #     print(vaccinationsData[CovidTest.DAILY_NUMBER_OF_TESTS])
    #     print(vaccinationsData[CovidTest.DAILY_POSITIVE_TESTS])
    #     print(vaccinationsData[CovidTest.DAILY_AVERAGE_NUMBER_OF_TESTS])
    #     print(vaccinationsData[CovidTest.DAILY_AVERAGE_PERCENT_OF_POSITIVE_TESTS])
    #     print() 
    # example print to show you how output looks like

    covidDetails = readCovidGrow()
    # for date, covidData in covidDetails.items():
    #     print(date)
    #     print(covidData[CovidGrow.NEW_DAILY_CASES])
    #     print(covidData[CovidGrow.NEW_DAILY_DEATHS])
    #     print(covidData[CovidGrow.NEW_DAILY_RECOVERIES])
    #     print(covidData[CovidGrow.INACTIVE_CASES_SHIFT])
    #     print(covidData[CovidGrow.ACTIVE_CASES_SHIFT])
    #     print(covidData[CovidGrow.SUMMED_CASES])
    #     print(covidData[CovidGrow.SUMMED_DEATHS])
    #     print(covidData[CovidGrow.SUMMED_RECOVERIES])
    #     print(covidData[CovidGrow.TEMPORARY_INACTIVE_CASES_NUMBER])
    #     print(covidData[CovidGrow.TEMPORARY_ACTIVE_CASES_NUMBER])
    #     print() 
    # example print to show you how output looks like

