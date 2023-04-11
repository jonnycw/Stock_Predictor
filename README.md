# S&P500_Predictor
Use machine learning to try and predict stock market movement. 

---

## About The Project

This application is designed predict the price action of the SPDR S&P 500 ETF Trust (SPY). This application looks at economic indicators and performs sentiment analysis to help investors make informed decisions about their investment choices.
+ Pulls S&P Financials
+ Generates key market ratios
+ Pulls economic indicators
+ Performs news sentiment analysis

Using the above inputs, the model is used to predict future S&P 500 movement.

---

## Installation

One version of the code is run on a pc with Windows 10. Another version of the code is run on Mac using Google Colab.

This project leverages Python 3.9 with the following packages:

+ pandas
+ numpy
+ datetime
+ sklearn 
+ tensorflow
+ datetime 
+ matplotlib
+ yfinance
+ requests
+ os
+ scikit-learn
+ nltk
+ vaderSentiment

### Installation Guide(MacOS & Windows)

1.  Open a terminal or command prompt on your computer.
2.  Install all packages by running the commands: 

```bash
  pip install pandas
  pip install numpy
  pip install datetime
  pip install sklearn 
  pip install tensorflow
  pip install datetime 
  pip install matplotlib
  pip install yfinance
  pip install requests
  pip install os
  pip install scikit-learn
  pip install nltk
  pip install vaderSentiment
```
---

## Installation

This code was run on a pc with Windows 10

This project leverages python 3.9 with the following packages:

+ streamlit
+ pandas 
+ pandas-datareader 
+ requests
+ yfinance 
+ plotly
+ MCForecastTools
+ matplotlib
+ numpy

### Installation Guide(MacOS & Windows)

1.  Open a terminal or command prompt on your computer.
2.  Install all packages by running the commands: 

```bash
  pip install streamlit
  pip install pandas 
  pip install pandas-datareader 
  pip install requests
  pip install yfinance 
  pip install datetime 
  pip install Matplotlib
  pip install MCForecastTools
  pip install numpy
```
---

### Background
In the background the following python modules are running.

```bash
"vix_mod"
"spy_mod"
"econ_mod"
"sent_mod"
```

vix_mod
>This plugin pulls historical vix data and pricing. Uses kmeans to label vix data as "high," "medium," and "low" volatility.

spy_mod
>This plugin pulls historical SPDR S&P 500 ETF Trust (SPY) data and generates market indicators and financial ratios.

econ_mod
>This plugin pulls economic data from the Federal Reserve Economic Data.

sent_mod
>This plugin pulls news headlines for the SPY and groups them by day. It then performs sentiment analysis to give a sentiment score betweeo -1 and 1 (-1 being most negative and 1 being most positive)

---

## Summary



---

## Contributors

* Michael Roth
* Diego Favela
* Jonny Cruz

---

## License
This program is licensed under the MIT License.
