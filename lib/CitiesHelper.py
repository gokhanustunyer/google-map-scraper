import os
from typing import List
import pandas as pd

from lib.GoogleMapModels import LocationModel

class WorldCitiesHelper:
    
    CSV_PATH = "datas/worldcities.csv"
    
    def __init__(self) -> None:
        
        dir_name = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_name, "..", WorldCitiesHelper.CSV_PATH)
        self.worldCities = pd.read_csv(file_path)
        
    def getDistrictsByCity(self, city: str) -> List[LocationModel]:
        districts = self.worldCities.loc[self.worldCities['admin_name'] == city]
        locations = []
        for _, row in districts.iterrows():
            if row["admin_name"].replace('İ', 'I').lower() == row["city"].replace("İ", 'I').lower():
                continue
            location = LocationModel()
            location.city = city
            location.country = row["country"]
            location.district = row["city"]
            locations.append(location)

        return locations
    
    def getCitiesByCountry(self, country: str) -> List[LocationModel]:
        pass
    
    def getNeighbourhoodsByDitrict(self, district: str) -> List[LocationModel]:
        pass
    
def main():
    wch = WorldCitiesHelper()
    wch.getDistrictsByCity("İstanbul")
    
if __name__ == "__main__":
    main()