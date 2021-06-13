**Metody Inteligencji Obliczeniowej**


# Predykcja nowych przypadków COVID-19 

Jan Zajda, Wojciech Jędraski, Tomasz Gajda 


  - [1. Temat projektu](#1-temat-projektu)
  - [2. Założenia technologiczne](#2-założenia-technologiczne)
  - [3. Źródło danych wejściowych](#3-źródło-danych-wejściowych)
  - [4. Parsowanie danych](#4-parsowanie-danych)
  - [5. Wizualizacja danych](#5-wizualizacja-danych)
  - [6. Macierz korelacji i wykresy autokorelacji](#6-macierz-korelacji-i-wykresy-autokorelacji)
  - [7. Dobór danych wejściowych](#7-dobór-danych-wejściowych)
  - [8. Predykcja - uczenie SSN](#8-predykcja---uczenie-ssn)
  - [9. Przykładowe wyniki predykcji](#9-przykładowe-wyniki-predykcji)
    - [Predykcja następnego tygodnia](#predykcja-następnego-tygodnia)
    - [Predykcja średniej ilości dziennych zakażeń następnych tygodni](#predykcja-średniej-ilości-dziennych-zakażeń-następnych-tygodni)
  - [10. Dokumentacja użytkownika](#10-dokumentacja-użytkownika)

## 1. Temat projektu

Projekt polega na stworzeniu narzędzia, pozwalającego na predykcję nowych przypadków **COVID-19**. Do tworzenia predykcji wykorzystane zostaną **Sztuczne Sieci Neuronowe**. Z racji szeregu czasowego dane zostaną podzielone na **uczące** i **testujące** zgodnie z osią czasu. Jako dane wejściowe użyte zostaną niektóre wartości szeregu czasowego z przeszłości - do ich ustalenia przeprowadzona zostanie **analiza autokorelacji**, z której wyłoniony powinien zostać kluczowy input.


## 2. Założenia technologiczne

Do stworzenia narzędzia korzystającego ze **Sztucznej Sieci Neuronowej** wykorzystany został **Python** w najnowszej wersji. Główne biblioteki, z których korzystaliśmy to **pandas**, **plotly** i **scikit-learn.** 


## 3. Źródło danych wejściowych

Do wytworzenia predykcji korzystamy z danych przygotowanych przez Pana **Michała Rogalskiego**. Dane są w postaci plików CSV, umieszczone są w folderze o nazwie **data**. Wszystkie dane oraz pliki zawarte są publicznym arkuszu pod tym linkiem:

[http://bit.ly/covid19-poland](http://bit.ly/covid19-poland)

Dane dla większej przejrzystości zostały podzielone na trzy główne pliki - **wzrost, testy i szczepienia.** Dla wygody, korzystaliśmy z pobranych arkuszy, dlatego w projekcie zawarte są dane w zakresie od **2 marca 2020**, do **17 maja 2021**.

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/input_data.png" height="400px" width="660px">

Rys. 1 - Plik **Google Spreadsheets** stworzony przez Michała Rogalskiego,  zawierający wszystkie dostępne dane na temat przebiegu COVID-19 w Polsce

## 4. Parsowanie danych

Dane z plików CSV wymagają parsowania - w folderze **reader** znajduje się plik o nazwie **csvReader.py**, który służy do przetworzenia danych z plików CSV na struktury danych dostępne w Pythonie. 

W pliku utworzone zostały **trzy klasy** - po jednej na rodzaj (**CovidGrow, CovidTest i Vaccination**)  -  w których dostępne są metody czytające dane z plików CSV. Metody te przetwarzają dane na słowniki, które poszczególnym datom przypisują wszystkie dane dotyczące specyficznego rodzaju. Przykładowo wyciągając ostatni element z obiektu klasy CovidGrow, otrzymujemy: 

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/parsed_data.png" height="400px" width="600px">

Rys. 2 - Graficzne przedstawienie **formatu danych** stosowanych w projekcie

Taka struktura pozwala nam na łatwą manipulację danymi i przystępny dostęp do wszystkich informacji.


## 5. Wizualizacja danych

W folderze o nazwie **visualization**, możemy znaleźć klasę o nazwie **_CovidVisualization_** zawierającej pięć metod służących do wizualizacji danych:

*   **linear_covid_data_plots**- metoda służąca do tworzenia wykresu liniowego podanych wartości,
*   **bar_autocorrelation_plots** - metoda przedstawiająca wykresy autokorelacji dla różnych danych wejściowych,
*   **correlation_matrix_plot** - metoda przedstawiająca macierz korelacji zmiennych na wykresie,
*   **bar_plot**- metoda służąca do tworzenia wykresu słupkowego podanych wartości,
*   **week_avg_prediction**- metoda porównująca na wykresie wyniki przewidywań średniej ilości dziennych zachorowań w trzech kolejnych tygodniach z realnymi wartościami,
*   **plot_prediction**- metoda porównująca na wykresie wyniki przewidywań ilości dziennych zachorowań w określonym okresie czasu - metoda składa wykresy  przewidywań, danych testowych i treningowych w jeden wykres,

Po wywołaniu metody, lokalnie w przeglądarce zostaje włączony interaktywny wykres, na którym możemy zobaczyć dane przekazane do metod. Do stworzenia wizualizacji skorzystaliśmy z biblioteki_ **plotly.**

Po wywołaniu metody, lokalnie w przeglądarce zostaje włączony interaktywny wykres, na którym możemy zobaczyć dane przekazane do metod.

Przykłady działania wizualizacji przedstawione zostaną przy użyciu danych z dni **od 20 kwietnia 2021 roku** do **17 maja 2021 roku.**

Przedstawiają one odpowiednio:
*   Ilość dziennych przypadków zakażeń (w postaci liniowej i słupkowej),
*   Ilość dziennych dawek szczepionek (w postaci liniowej i słupkowej)


<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/daily_cases_bar_plot.png" height="350px" width="600px">

Rys. 3 - Wykres **słupkowy** przedstawiający ilość przypadków **(20.04 - 17.05.2021)**

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/daily_cases_linear_plot.png" height="350px" width="600px">

Rys. 4 - Wykres **liniowy** przedstawiający ilość przypadków **(20.04 - 17.05.2021)**

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/daily_vaccination_bar_plot.png" height="350px" width="600px">

Rys. 5 - Wykres **słupkowy** przedstawiający ilość podanych szczepionek **(20.04 - 17.05.2021)**

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/daily_vaccination_linear_plot.png" height="350px" width="600px">

Rys. 6 - Wykres **liniowy** przedstawiający ilość podanych szczepionek **(20.04 - 17.05.2021)**

Jeden z wykresów predykcji pokazuje również wyniki przedstawione na tle danych treningowych dostarczonych w procesie:

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/prediction_scaled_graph.png" height="200px" width="800px">

Rys. 7 - Wizualizacja predykcji na tle **danych treningowych**


## 6. Macierz korelacji i wykresy autokorelacji

By wybrać spośród dużej ilości potencjalnych danych te, które mają znaczenie w przypadku próby predykcji przypadków COVID-19, skorzystaliśmy z analizy **korelacji** między zmiennymi oraz analizy **autokorelacji**. Korelację między zmiennymi opisaliśmy na macierzy:

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/correlation_matrix.png" height="400px" width="650px">

Rys. 8 - Wizualizacja **macierzy korelacji** potencjalnych wartości wejściowych

**Autokorelacja** (korelacja sygnału z poprzednimi jego stanami), została przedstawiona na osobnym wykresie dla każdej ze zmiennych, na przykład:

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/vaccination_daily_autocorrelation.png" height="200px" width="800px">

Rys. 9 - Wizualizacja **autokorelacji** dla **dziennej ilości podanych szczepionek** (liniowy)

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/new_daily_cases_autocorrelation.png" height="200px" width="800px">

Rys. 10 - Wizualizacja **autokorelacji** dla **dziennej ilości przypadków** (liniowy)

Na początku wykresy autokorelacji przedstawione zostały na wykresach **liniowych**, ale zgodnie z zaleceniami zmienione zostały na wykresy **słupkowe**.

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/bar_graph_vaccines.png" height="200px" width="800px">

Rys. 11 - Wizualizacja **autokorelacji** dla **dziennej ilości podanych szczepionek** (słupkowy)

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/bar_graph_cases.png" height="200px" width="800px">

Rys. 12 - Wizualizacja **autokorelacji** dla **dziennej ilości przypadków** (słupkowy)


## 7. Dobór danych wejściowych

Po przejrzeniu wyników analizy autokorelacji przedstawionej w postaci wykresów, ustaliliśmy że nie dają nam one jasnych wyznaczników mówiących o tym, z jakiego okresu dane powinniśmy brać. Model niewiele różnić się będzie przy zmianie okresu (z np. 7 na 14 dni) - w tym przypadku liczy się **tendencja wzrostowa** i lepszej aproksymacji krzywej zachorowań nie otrzymamy stosując inny zakres dat.

Przy każdym włączeniu predykcji, **dynamicznie** obliczane są wartości korelacji zmiennych z poszukiwaną przez nas **dzienną liczbą nowych przypadków** - korelacja sprawdzana jest dla okresu czasu wyznaczonego przez podane w argumentach granice. W programie podać możemy minimalną wartość korelacji tych zmiennych - w ten sposób automatycznie wybierane są dane które weźmiemy pod uwagę w momencie uczenia sieci.


## 8. Predykcja - uczenie SSN

Do predykcji wykorzystaliśmy bibliotekę **scikit-learn.**
W programie znaleźć można dwa różne rodzaje predykcji:

**1. Przewidywanie ilości przypadków w wyznaczonym przez nas okresie, bazując na określonym zbiorze danych uczących**

Ten rodzaj predykcji pozwala na wybranie kilku **parametrów**, które definiują sposób i dane do trenowania naszej sieci. Parametry do ręcznego ustalenia:

*   **START_DATE** - data - definiuje dzień, od którego zaczynamy brać dane do trenowania sieci,
*   **DAYS_TO_PREDICT** - int - ilość dni, które chcemy przewidzieć (domyślnie 7),

Ta predykcja bazując na wybranej przez nas ilości danych i wybranych przez selekcję na podstawie korelacji typów zmiennych, umożliwia nam ustalenie przybliżonych ilości dziennych zakażeń w {DAYS_TO_PREDICT} kolejnych dniach.

**2. Przewidywanie tygodniowo średnich ilości dziennych przypadków zarażeń dla 3 kolejnych tygodni**

Ten rodzaj również pozwala na zmianę parametrów, lecz te zmieniamy w pliku **prepareData.py**.** **Ta predykcja bazując na tygodniowych średnich z przeszłości pozwala nam ustalić średnie dla trzech kolejnych tygodni.

## 9. Przykładowe wyniki predykcji

### Predykcja następnego tygodnia

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/output_graph_1.png" height="300px" width="650px">

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/output_graph_2.png" height="300px" width="650px">

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/output_graph_3.png" height="300px" width="650px">



Rys. 13 - Przykładowe wyniki **predykcji dziennej ilości zachorowań** następnego tygodnia


### Predykcja średniej ilości dziennych zakażeń następnych tygodni

<img src="https://github.com/Equilibrium23/MIO-Project/blob/docs/documentation-and-pictures/docs/Pictures/weeks_output_graph_1.png" height="450px" width="650px">

Rys. 14 - Przykładowy wynik **predykcji tygodniowej średniej ilości dziennych zachorowań** trzech kolejnych tygodni


## 10. Dokumentacja użytkownika

By skorzystać ze stworzonego przez nas narzędzia, wystarczy postępować zgodnie z instrukcją umieszczoną poniżej.


1. **Pobierz repozytorium**

Wszystkie pliki źródłowe znajdują się w repozytorium na platformie GitHub - [https://github.com/Equilibrium23/MIO-Project](https://github.com/Equilibrium23/MIO-Project)  


2. **Pobierz najnowszą wersję Python’a**

Wszystkie informacje i potrzebne pliki można znaleźć na oficjalnej stronie Python’a - [https://www.python.org/downloads/](https://www.python.org/downloads/)


3. **Pobierz wszystkie zależności z pliku requirements.txt**

Korzystając z komendy poniżej pobierz wszystkie zewnętrzne biblioteki

`python3 -m pip install -r requirements.txt`

<em>(komenda może się różnić w zależności od wersji Pythona)</em>

4. **Z poziomu folderu ze wszystkimi plikami, uruchom main.py**

Plik **main.py** zawiera prezentację większości funkcji, które dostępne są w naszym programie. Wewnątrz znajdują się wypunktowane opcje, które można **odkomentować** i uruchomić ponownie plik aby uzyskać opisany wyżej w komentarzu efekt.
