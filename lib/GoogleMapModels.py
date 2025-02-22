from typing import Union, List


class LocationModel:
    country: Union[str, None] = None
    city: Union[str, None] = None
    district: Union[str, None] = None
    neighbourhood: Union[str, None] = None
    fullAddress: Union[str, None] = None
    lat: Union[float, None] = None
    lng: Union[float, None] = None
    
    
    def __str__(self):
        return f'"country:" {self.country}, "city:" {self.city}, "district:" {self.district}, "neighbourhood:" {self.neighbourhood}, "fullAddress:" {self.fullAddress}, "lat:" {self.lat}, "lng:", {self.lng}'
    
class CompanyModel:
    location: Union[LocationModel, None] = None
    title: Union[str, None] = None
    rate: Union[float, None] = None
    category: Union[str, None] = None
    website: Union[str, None] = None
    phoneNumber: Union[str, None] = None
    
    def __str__(self):
        return f'"location:" {self.location}, "title:" {self.title}, "rate:" {self.rate}, "category:" {self.category}, "website:" {self.website}, "phoneNumber:" {self.phoneNumber}'