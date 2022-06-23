import os

import requests as requests
from flask import Flask, request

from strategy.cloud.cloud_strategy import CloudStrategy
from strategy.console.console_strategy import ConsoleStrategy
from strategy.file.file_strategy import FileStrategy
from strategy.utils import Utils

app = Flask(__name__)


@app.route('/load-data/', methods=['POST'])
async def load_file():
    utils = ConsoleStrategy()
    option = os.getenv("OPTION")

    endpoint = request.form.get("url_data")
    if not endpoint:
        return "Please provide provide url to your dataset"

    data = requests.get(endpoint)
    print(len(data.json()))

    if option == "cloud":
        print("used cloud strategy")
        utils = CloudStrategy(file_url=endpoint)
    elif option == "file":
        print("used file strategy")
        utils = FileStrategy()
    else:
        print("used default strategy")
    strategy = Utils(utils)
    await strategy.start_realisation(data.json())

    return 'file loaded'


# docker run -p 5000:5000 -it --env-file .env  -e OPTION=file dotem-lab:latest
# incidentnum,servyr,servnumid,watch,signal,offincident,premise,objattack,incident_address,apt,ra,beat,division,sector,district,taag,community,date1,year1,month1,day1,time1,date1dayofyear,date2_of_occurrence_2,year2,month2,day2,time2,date2dayofyear,reporteddate,edate,eyear,emonth,eday,etime,edatedayofyear,cfs_number,callorgdate,callreceived,callcleared,calldispatched,splrpt,involvement,victimtype,comprace,compethnicity,compsex,ro1badge,ro1name,ro2badge,ro2name,reptoff,assoffbadge,reviewbadgenum,elenum,followup1,followup2,status,ucr_disp,mo,family,hate,hatecrimedescriptn,weaponused,gang,drug,offensecode,cjis,penalcode,ucr_offense,ucr_offdesc,ucrcode,type,nibrs_crime,nibrs_crime_category,nibrs_crimeagainst,nibrs_code,nibrs_group,nibrs_type,upzdate,x_coordinate,y_cordinate,zip_code,city,state,geocoded_column
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
