from lib.normalise import WOF_AUS, WOF_NZ, Geocoder, location_jsonld
from lib.salary import get_salary_data
from sources.abstract_datasource import module_name
from sources.jsonld import Datasource as JSONLinkedDatasource

AU_GEOCODER = Geocoder(lang="en", filter_country_ids=(WOF_AUS, WOF_NZ))


class Datasource(JSONLinkedDatasource):
    name = module_name(__name__)
    query = "www.cgcrecruitment.com/job/*"

    def normalise(self, data, uri, view_date):
        ans = super().normalise(data, uri, view_date)
        salary_raw = data["baseSalary"]["value"].get("value")
        salary = get_salary_data(salary_raw)
        location_raw = location_jsonld(data)
        return {
            **ans,
            **salary,
            "location_raw": location_raw,
            **AU_GEOCODER.geocode(location_raw),
        }
