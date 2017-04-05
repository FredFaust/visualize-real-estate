import json
from datetime import datetime
from scraping.scraper_duproprio import DuProprioScraper


def ftime(val):
    """Format time values under 10 to include 0 as first char"""
    if val < 10:
        return "0{}".format(val)
    return val


if __name__ == "__main__":
    dp_scraper = DuProprioScraper()
    data_scraped_houses, errors = dp_scraper.scrap_all_mtl()

    dt = datetime.now()
    datetime_dt = "{}{}{}_{}{}{}.txt".format(dt.year,
                                             ftime(dt.month),
                                             ftime(dt.day),
                                             ftime(dt.hour),
                                             ftime(dt.minute),
                                             ftime(dt.second))
    filename_data = "scraped_data_dp_{}".format(datetime_dt)
    filename_errors = "errors_dp_{}".format(datetime_dt)

    with open("data/{}".format(filename_data), 'w') as f:
        json.dump(data_scraped_houses, f, indent=4, ensure_ascii=False)

    if len(errors) > 0:
        with open("errors/{}".format(filename_errors), 'w') as f:
            for e in errors:
                f.write("-----End of error-----\n")
                f.write(str(e[0]) + '\n')
                f.write(str(e[1]) + '\n')
                f.write("-----End of error-----\n")
