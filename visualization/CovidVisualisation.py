import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from reader.csvReader import readVaccinations, readTests, readCovidGrow, Vaccination, CovidTest, CovidGrow

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

    def linear_covid_data_plots(self, data_types: list, from_date: datetime, to_date: datetime):
        fig = make_subplots(
            rows=len(data_types), cols=1,
            subplot_titles=(tuple([str(x) for x in data_types]))
            )

        for index, data_type in enumerate(data_types):
            validation = self.validate_data_type(data_type)

            if validation[0]:
                plot_data = validation[1]
                x_data = [ x for x in plot_data.keys() if from_date.date() <= x <= to_date.date()  ]
                y_data = [ y[data_type] for x,y in plot_data.items() if from_date.date() <= x <= to_date.date() ]

                fig.append_trace(go.Scatter
                (
                    x=x_data,
                    y=y_data,
                    name=str(data_type)
                ), row=index+1, col=1)

        fig.update_layout(height=len(data_types)*400, width=1300, title_text="Covid Data Subplots", showlegend=False)
        fig.show()
    
    def linear_autocorrelation_plots(self, data: dict):
        fig = make_subplots(
            rows=len(data.keys()), cols=1,
            subplot_titles=(tuple([str(x) + ' AUTOCORRELATION' for x in data.keys()]))
            )
        
        for index, key in enumerate(data.keys()):
            fig.append_trace(go.Scatter
                (
                    x=list(data[key].keys()),
                    y=list(data[key].values()),
                    name=key + ' AUTOCORRELATION'
                ), row=index+1, col=1)
        
        fig.update_layout(height=len(data.keys())*400, width=1300, title_text="Covid Autocorrelation Subplots", showlegend=False)
        fig.show()
    
    def correlation_matrix_plot(self, data: pd.DataFrame):
        fig = px.imshow(data, color_continuous_scale=px.colors.sequential.RdBu)
        fig.update_layout(title_text="Correlation Matrix")
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