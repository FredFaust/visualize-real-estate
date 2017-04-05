import sys
import math
import requests
import traceback
from lxml import html
from cssselect import HTMLTranslator


class DuProprioScraper:
    def __init__(self):
        self.data_scraped_houses = []
        self.errors = []

    def scrap_all_mtl(self):
        self.data_scraped_houses = []
        self.errors = []
        id_region_mtl = 6
        # Initial request to fetch number of houses
        url_list_mtl = self.build_list_url(id_region_mtl, 1)
        page_list_mtl = requests.get(url_list_mtl)
        doc_list_mtl = html.fromstring(page_list_mtl.content)

        # Get the total number of pages
        houses_per_page = 11
        css_span = "span.search-results-listings-header__properties-found__number"
        results = self.scrap_value(doc_list_mtl, css_span)
        span_properties_found = results[0]
        total_house_count = int(span_properties_found.text)
        total_nbr_pages = math.ceil(total_house_count / houses_per_page)

        urls_houses = []
        # Collect the url for every houses
        # for i in range(1, total_nbr_pages + 1):
        for i in range(1, 2):
            print("Scraping page #{}".format(i))
            url_list = self.build_list_url(id_region_mtl, i)
            page_list = requests.get(url_list)
            doc_list = html.fromstring(page_list.content)
            prop_link = "a[property=significantLink]"
            links = self.scrap_value(doc_list, prop_link)
            for link in links:
                urls_houses.append(link.get('href'))

        # Collect info about individual houses
        for i, url in enumerate(urls_houses):
            print("Scraping house #{}".format(i))
            page_single_house = requests.get(url)
            doc_single_house = html.fromstring(page_single_house.content)
            css_price = 'meta[property="price"]'
            css_lat = 'meta[property="latitude"]'
            css_long = 'meta[property="longitude"]'
            css_street = 'meta[property="streetAddress"]'
            css_locality = 'meta[property="addressLocality"]'
            try:
                elem_price = self.scrap_value(doc_single_house, css_price)[0]
                elem_geo_lat = self.scrap_value(doc_single_house, css_lat)[0]
                elem_geo_long = self.scrap_value(doc_single_house, css_long)[0]
                elem_street = self.scrap_value(doc_single_house, css_street)[0]
                elem_locality = \
                self.scrap_value(doc_single_house, css_locality)[0]
                val_price = elem_price.get('content')
                val_lat = elem_geo_lat.get('content')
                val_long = elem_geo_long.get('content')
                val_street = elem_street.get('content')
                val_locality = elem_locality.get('content')
                self.data_scraped_houses.append({
                    'price': val_price,
                    'street': val_street,
                    'locality': val_locality,
                    'latitude': val_lat,
                    'longitude': val_long,
                })
            except Exception as ex:
                traceback.print_exc(limit=3, file=sys.stdout)
                self.errors.append((url, ex))

        print("Total number of houses scraped : {}".format(
            len(self.data_scraped_houses)))
        print("Total number of errors encountered : {}".format(
            len(self.errors)))

        return self.data_scraped_houses, self.errors

    @staticmethod
    def scrap_value(doc, selector):
        xpath_selector = HTMLTranslator().css_to_xpath(selector)
        elems = doc.xpath(xpath_selector)
        return elems

    @staticmethod
    def build_list_url(region_id, page_num):
        # For archiving purposes
        # "https://duproprio.com/en/search/list?search=true&regions%5B0%5D=6&type%5B0%5D=house&type%5B1%5D=condo&type%5B2%5D=cottage&is_for_sale=1&with_builders=1&parent=1&pageNumber=2&sort=-published_at"
        p_regions = "&regions%5B0%5D={}".format(region_id)
        # TODO Loop for house types
        p_types = "&type%5B0%5D=house&type%5B1%5D=condo&type%5B2%5D=cottage"
        p_others = "&is_for_sale=1&with_builders=1&parent=1"
        p_page_num = "&pageNumber={}".format(page_num)
        p_sort = "&sort=-published_at"
        base_url = "https://duproprio.com/en/search/list?search=true"
        final_url = "{}{}{}{}{}{}".format(base_url, p_regions, p_types,
                                          p_others, p_sort, p_page_num)
        return final_url
