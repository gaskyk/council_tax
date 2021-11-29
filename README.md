# Collecting council tax data

## Overview

This code collects council tax data for properties from a list of postcodes. The data comes from the [Valuation Office Agency website](https://www.tax.service.gov.uk/check-council-tax-band/search).

## How do I use this project?

The following Python packages are required:
- requests
- bs4
- selenium
- time
- pandas

In addition, the code requires:
- [ChromeDriver](https://chromedriver.chromium.org/home) to be downloaded and for the ChromeDriver file path to be specified in the code as this is required for selenium to drive Chrome
- A list of postcodes saved in a file called "My_postcodes.csv" with the column name "pcds". It is not included here as it may narrow down my location. A list of postcodes can be found on the [Open Geography Portal](https://geoportal.statistics.gov.uk/)
