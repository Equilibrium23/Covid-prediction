import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from datetime import datetime
from reader.csvReader import readVaccinations, readTests, readCovidGrow, Vaccination, CovidTest, CovidGrow
from autocorrelation.correlationMatrix import correlate
import plotly
import plotly.graph_objects as go
from plotly.graph_objs import Scatter, Layout
import plotly.express as px

class CovidVisualisation:
    def __init__(self):
        self.covid_vaccinations = readVaccinations()
        self.covid_tests = readTests()
        self.covid_details = readCovidGrow()
    
    def validate_data_type(self, data_type):
        plot_data = dict()
        data_type_is_proper = False
        if isinstance(data_type, Vaccination):
            plot_data = self.covid_vaccinations
            data_type_is_proper = True
        elif isinstance(data_type, CovidTest):
            plot_data = self.covid_tests
            data_type_is_proper = True
        elif isinstance(data_type, CovidGrow):
            plot_data = self.covid_details
            data_type_is_proper = True

        return (data_type_is_proper, plot_data)

    def linear_plot(self, data_type, from_date : datetime, to_date : datetime):
        validation = self.validate_data_type(data_type)
        if validation[0]:
            plot_data = validation[1]
            x_data = [ x for x in plot_data.keys() if from_date.date() <= x <= to_date.date()  ]
            y_data = [ y[data_type] for x,y in plot_data.items() if from_date.date() <= x <= to_date.date() ]
            fig = go.Figure(data=go.Scatter(x = x_data,y = y_data))
            fig.show()
        
    def bar_plot(self, data_type, from_date : datetime, to_date : datetime):
        validation = self.validate_data_type(data_type)
        if validation[0]:
            plot_data = validation[1]
            covid_data = dict()
            covid_data["x"] = [ x for x in plot_data.keys() if from_date.date() <= x <= to_date.date()  ]
            covid_data["y"] = [ y[data_type] for x,y in plot_data.items() if from_date.date() <= x <= to_date.date() ]

            fig = px.bar( covid_data, x = 'x', y = 'y', color = 'y')
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title = str(data_type) ,
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="RebeccaPurple"
                )
            )
            fig.show()