"""
Collect council tax data from Valuation Office Agency website
=============================================================
Code accesses a list of postcodes, and sequentially enters
them into the website, collecting the URLs of each property
within each postcode. The code then iterates through each property
in that postcode to collect the relevant council tax information:
- address
- council tax band
- an improvement indicator
- the date from which the band is effective from
- a mixed use indicator

Requirements
:requires: requests
:requires: bs4
:requires: selenium
:requires: time
:requires: pandas
"""

# Import packages
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


def get_council_tax_info_property(url):
    """
    Function to extract the relevant council tax information for a given
    url / property
    :param url: URL representing an individual property
    :type url: string
    :return my_dict: A dictionary containing relevant information from that url
    :rtype my_dict: dictionary
    """

    # Get information from the page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Address
    address_tag = soup.find("h2")
    address = address_tag.get_text().title()

    # Other data
    other_tag = soup.find_all("dd")

    # Council tax band
    council_band = other_tag[2].get_text().title()
    council_band = council_band.strip("\n").strip(" ").strip("\n")

    # Improvement indictor
    improvement_indicator = other_tag[3].get_text().title()
    improvement_indicator = improvement_indicator.strip("\n").strip(" ").strip("\n")

    # With effect from
    effect_from = other_tag[4].get_text().title()
    effect_from = effect_from.strip("\n").strip(" ").strip("\n")

    # Mixed-use property
    mixed_use = other_tag[5].get_text().title()
    mixed_use = mixed_use.strip("\n").strip(" ").strip("\n")

    # Create a dictionary for each address
    my_dict = {
        "Address": address,
        "Council_tax_band": council_band,
        "Improvement_indicator": improvement_indicator,
        "Effect_from": effect_from,
        "Mixed_use": mixed_use
    }

    return my_dict


def get_property_urls(postcode):
    """
    Function to extract the property urls for all properties in a given postcode
    :param postcode: Postcode
    :type postcode: string
    :return links: A list containing all the urls of properties in that postcode
    :rtype links: list
    """

    # Launch web driver and go to website
    driver = webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe")
    driver.get("https://www.tax.service.gov.uk/check-council-tax-band/properties?searchBy=Postcode")

    # Enter selected postcode into postcode search, waiting one second until click
    time.sleep(2)
    driver.find_element_by_id('postcode').send_keys(postcode)
    driver.find_element_by_id('submitsearch3').click()

    # Find the urls for each property
    elems = driver.find_elements_by_css_selector("td [href]")
    links = [elem.get_attribute('href') for elem in elems]

    while True:
        try:
            driver.find_element_by_id('next_page_link').click()
            elems = driver.find_elements_by_css_selector("td [href]")
            links2 = [elem.get_attribute('href') for elem in elems]
            links.extend(links2)
            time.sleep(2)
        except:
            print(postcode, "successfully completed")
            break

    driver.quit()

    # Remove 'http://www.havant.gov.uk/' from the list
    links = list(filter(lambda a: a != 'http://www.havant.gov.uk/', links))

    return links


def get_council_tax_info_postcode(postcode):
    """
    Function to extract the relevant council tax information for a given
    postcode
    :param postcode: Postcode
    :type postcode: string
    :return property_info: list of dictionaries containing council tax
    information for each property in the postcode
    :rtype property_info: list of dictionaries
    """
    property_urls = get_property_urls(postcode)

    # Empty list
    property_info = []

    # Get council tax information for a list of property urls
    for i in property_urls:
        property_dict = get_council_tax_info_property(i)
        # Create list of dictionaries
        property_info.append(property_dict)

    return property_info


def save_all_postcodes_council_tax_info(csv_name):
    """
    Function to extract the relevant council tax information for all postcodes
    and save to CSV
    :param csv_name: CSV name containing a list of postcodes
    :type csv_name: string
    """

    # Import list of postcodes
    postcode_df = pd.read_csv(csv_name)

    # Convert to list
    postcode_list = postcode_df['pcds'].to_list()

    # Create empty list for all council tax info
    all_pcds_info = []

    # Iterate over postcodes to get council tax information
    for i in postcode_list:
        postcode_info = get_council_tax_info_postcode(i)
        all_pcds_info.extend(postcode_info)

    # Convert list of dictionaries to pandas dataframe
    postcode_df = pd.DataFrame(all_pcds_info)

    # Save to CSV
    postcode_df.to_csv('Council_tax_bands.csv', encoding='utf-8', index=False)


save_all_postcodes_council_tax_info('My_postcodes.csv')
