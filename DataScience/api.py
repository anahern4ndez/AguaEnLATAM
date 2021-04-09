

import knoema
import pandas as pd
import numpy as np

apicfg = knoema.ApiConfig()
apicfg.host = 'knoema.com'
apicfg.app_id = "lWeHSds"
apicfg.app_secret = "V2IQCRjXL4T6TQ"

data = knoema.get('FAOAQST2019', Location='BRA;MEX;COL;ARG;PER;VEN;CHL;GTM;ECU;BOL;HTI;CUB;DOM;HND;PRY;NIC;SLV;CRI;PAN;URY;JAM;TTO;GUY;SUR;BLZ;BHS;BRB;LCA;GRD;VCT;ATG;DMA;KNA', Variable='4151;4150;4472;4155;4154;4185;4250;4252;4251;4253;4475;4260;4254;4256;4255;4257;4549;4550')


f = open("aquastat.txt", "w")
f.write(str(data))
f.close()

print(data)

pandas_dict = {}

for variable in data.columns.levels[1]:
    pandas_dict[variable] = np.array([])

pandas_dict['year'] = []
pandas_dict['country'] = []


years = []
for date in data.head(50).index.values:
    dt = pd.to_datetime(str(date))
    # pandas_dict['year'].append(dt.strftime('%d/%m/%Y'))
    # years.append(dt.strftime('%d/%m/%Y'))
    years.append(date)

for year in years:
    for location in data.columns.levels[0]:
        for variable in data.columns.levels[1]:
            try:
                col = data[location, variable]['A'].to_numpy()
                pandas_dict[variable] = np.hstack((pandas_dict[variable], col))
                # print(year, location)
                # print("lv", location, variable, type(col))
            except KeyError as e:
                pandas_dict[variable] = np.hstack((pandas_dict[variable], np.array([ None for i in range(len(data.index)) ])))
        for i in range(len(col)):
            pandas_dict['year'].append(year)
            pandas_dict['country'].append(location)

for col in pandas_dict.keys():
    print(col, len(pandas_dict[col]))

pd.DataFrame(pandas_dict).to_csv("aquastat.csv")
pd.DataFrame(pandas_dict).query('year >= "2000-01-01"').to_csv("aquastat2000.csv")


knoema.get('WHOWSS2018', timerange='2000-2017', Location='GT;AI;AG;AR;AW;BS;BB;BZ;BO;BR;VG;KN.R1;KY;CL;CO;CR;CU;CW;DM;DO;EC;SV;FK;GF;GD;GP;GY;HT;HN;JM;MQ;MX;MS;NI;PA;PY;PE;PR;KN;LC;VC;SX;SR;TT;TC;VI;UY;VE', Indicator='KN.T3;KN.T4;KN.T5;KN.T6;KN.T7;KN.T9;KN.T10;KN.T11;KN.T12;KN.T13;KN.T14;KN.T17;KN.T18;KN.T19;KN.T20', Area='KN.A1')

pandas_dict = {}

for variable in data.columns.levels[1]:
    pandas_dict[variable] = np.array([])

pandas_dict['year'] = []
pandas_dict['country'] = []

years = []
for date in data.head(50).index.values:
    dt = pd.to_datetime(str(date))
    years.append(date)

for year in years:
    for location in data.columns.levels[0]:
        for variable in data.columns.levels[1]:
            try:
                col = data[location, variable]['National']['A'].to_numpy()
                pandas_dict[variable] = np.hstack((pandas_dict[variable], col))
            except KeyError as e:
                pandas_dict[variable] = np.hstack((pandas_dict[variable], np.array([ None for i in range(len(data.index)) ])))
        for i in range(len(col)):
            pandas_dict['year'].append(year)
            pandas_dict['country'].append(location)

for col in pandas_dict.keys():
    print(col, len(pandas_dict[col]))

pd.DataFrame(pandas_dict).to_csv("who.csv")