from lib.GoogleMapModels import LocationModel
from lib.GoogleMapScraper import GoogleMapScraper


def main():
    scraper = GoogleMapScraper()
    
    start_from = LocationModel()
    start_from.country = "Turkey"
    start_from.city = "İstanbul"
    start_from.lat = 41.049654
    start_from.lng = 28.991882

    scraper.start_scraping(start_from)



if __name__ == "__main__":
    main()