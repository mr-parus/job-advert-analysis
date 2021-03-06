import logging
from typing import Union

import bs4
from lib.normalise import (
    WOF_AUS,
    WOF_NZ,
    Geocoder,
    datetime_from_iso_utc,
    html2plain,
)
from lib.salary import get_salary_data
from sources.abstract_datasource import module_name
from sources.commoncrawl_datasource import CommonCrawlDatasource

AU_GEOCODER = Geocoder(lang="en", filter_country_ids=(WOF_AUS, WOF_NZ))


def fixup_iworkfornsw_loc(loc):
    # Normally multiple lines is statewide; take the broad location
    loc = loc.split("\n")[0]
    # Reverse the location; heuristic but generally gets something close to right (the locations are often ambiguous)
    return (
        ", ".join(reversed(loc.replace("-", "/").replace("&", "/").split("/")))
        + ", NSW, AU"
    )


# IWORKFORNSW_MAPPINGS = {
#     'Organisation/Entity:': 'hiringOrganization',
#     'Job Category:': 'industry',
#     'Job Location:': 'jobLocation',
#     'Job Reference Number:': 'identifier',
#     'Work Type:': 'employmentType',
#     'Number of Positions:': 'totalJobOpenings',
#     'Total Remuneration Package:': 'baseSalary', # A little abuse
#     'Contact:': 'applicationContact',
#     'Closing Date:': 'validThrough',
# }


class Datasource(CommonCrawlDatasource):
    name = module_name(__name__)
    query = "iworkfor.nsw.gov.au/job/*"

    def extract(self, html: Union[bytes, str], uri, view_date):
        soup = bs4.BeautifulSoup(html, "html5lib")
        body = soup.select_one("tbody")
        # Some pages are missing a body; e.g. CC-MAIN-2018-17
        if not body:
            return []
        infos = body.select("tr")
        data = {}
        for info in infos:
            key = info.select_one("th")
            value = info.select_one("td")
            if key and value:
                data[key.get_text().strip()] = value.get_text().strip()
        title_tag = soup.select_one(".job-detail-title")
        if not title_tag:
            logging.warning("Missing title tag in %s, %s", uri, view_date)
            title = None
        else:
            title = title_tag.get_text().strip()
        description = str(soup.select_one(".job-detail-des") or "")
        return [
            {
                "title": title,
                "description": description,
                "metadata": data,
                "uri": uri,
                "view_date": view_date,
            }
        ]

    def normalise(self, title, description, metadata, uri, view_date):
        salary = get_salary_data(metadata.get("Total Remuneration Package:") or "")
        location_raw = metadata["Job Location:"]
        return {
            "title": title,
            "description": html2plain(description),
            "uri": uri,
            "view_date": datetime_from_iso_utc(view_date),
            "org": metadata["Organisation/Entity:"],
            **salary,
            "location_raw": location_raw,
            **AU_GEOCODER.geocode(fixup_iworkfornsw_loc(location_raw)),
        }
