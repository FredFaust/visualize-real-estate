import json
from visualization import charts as vzc

if __name__ == "__main__":
    with open('data/scraped_data_20170404_215821.txt') as json_file:
        data = json.load(json_file)
        vzc.mean_price_bar_chart(data)
