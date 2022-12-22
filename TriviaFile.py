from mysql.connector import connect
import pandas as pd
import pymysql as ps
from sqlalchemy import create_engine

connection = {
    "host": "****",
    "port": ***,
    "user": "***",
    "passwd": "***",
    "database": "****"
}
db = ps.connect(**connection)
#sqlEngine = create_engine('mysql+pymysql://pbhat2:kDDMKw45@10.196.143.9/gac_dev4_ods')
#dbConnection = sqlEngine.connect()
dataFrame = pd.DataFrame()
query = "SELECT * FROM GAC_BOREHOLE_DETAILS;";
limit = 10000
offset = 0
cursor = db.cursor()
try:
    chunks = []
    for chunk in pd.read_sql(query, db, chunksize=10000):
        chunks.append(chunk)
    result = pd.concat(chunks,ignore_index=True)
    dataFrame = result.copy(deep=True)
except Exception as e:
    pass
finally:
    print("Done!")
    db.close()

pd.set_option('display.expand_frame_repr', False)
print(dataFrame.head())


dataFrameDF = dataFrame[dataFrame.duplicated(['SIEBEL_BOREHOLE_UID', 'SAPITT_BOREHOLE_UID', 'COUNTRY_CODE', 'MDM_BOREHOLE_ID'])]
#pd.set_option('display.expand_frame_repr', False)
print(dataFrameDF[['SIEBEL_BOREHOLE_UID', 'SAPITT_BOREHOLE_UID', 'COUNTRY_CODE', 'MDM_BOREHOLE_ID']])
dataFrameDF.to_csv('D:\\Projects\\AnalysisQueries\\Stories\\2022\\SprintB-10\\DBJImprove\\Duplicate.csv', index=False)

#pd.set_option('display.expand_frame_repr', False)



dataFrameDFAll = dataFrame[dataFrame.duplicated(['SIEBEL_BOREHOLE_UID', 'SAPITT_BOREHOLE_UID', 'COUNTRY_CODE', 'MDM_BOREHOLE_ID'], keep=False)]
dataFrameDFAll.to_csv('D:\\Projects\\AnalysisQueries\\Stories\\2022\\SprintB-10\\DBJImprove\\DuplicateAll.csv', index=False)

# Group By Method
dataFrame_1 = pd.concat(g for _, g in dataFrame.groupby(['SIEBEL_BOREHOLE_UID', 'SAPITT_BOREHOLE_UID', 'COUNTRY_CODE', 'MDM_BOREHOLE_ID']) if len(g) > 1)
