import requests
import unicodecsv
from bs4 import BeautifulSoup

f = open('weather_data.csv', 'wb')
writer = unicodecsv.writer(f)

# Column headers
writer.writerow(['Year','Month','Day','Max Temp (C)','Min Temp (C)','Mean Temp (C)',
                'Heat Deg Days (C)','Cool Deg Days (C)','Total Rain (mm)','Total Snow (cm)',
                'Total Precip (mm)','Snow on Grnd (cm)','Dir of Max Gust (10s deg)','Spd of Max Gust (km/h)'])

start_url = "http://climate.weather.gc.ca/climateData/dailydata_e.html?timeframe=2&Prov=QC&StationID=5415&dlyRange=1941-09-01%7C2014-07-31&cmdB1=Go&Year="
mid_url = '&Month='
end_url = "&cmdB1=Go#"

for year in range(1955, 2015):  # This will include all of 2014 so far
    for month in range (1,13):
        print "Processing data for %s / %s" % (month, year)
        r = requests.get(start_url + str(year) + mid_url + str(month) + end_url)
        data = r.text
        soup = BeautifulSoup(data)
        table = soup.find("table", attrs={"class","wet-boew-zebra"})
        for tr in table.find_all('tr')[2:]:
            #skip header and summary rows                        
            if tr.findChildren('th'):
                continue
            tds = tr.find_all('td')
            values = [td.text for td in tds]
            values.insert(0,month)
            values.insert(0,year)
            writer.writerow(values)

f.close()
