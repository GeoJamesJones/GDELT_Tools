import traceback
import sys
import time
import datetime
import os
import arcpy

outWS = arcpy.GetParameterAsText(0)
outGDB_name = arcpy.GetParameterAsText(1)
outFC_name = arcpy.GetParameterAsText(2)
sr = arcpy.GetParameterAsText(3)

if outGDB_name.split(".")[1] not in ['gdb']:
    arcpy.AddError("Please end File Geodatabse name with '.gdb'...")
    exit()

def exitScript():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg  = "PYTHON ERRORS:\n Traceback info:\n" + tbinfo + "Error info:\n" + str(sys.exc_info()[1])
    msg = "\nArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg)
    arcpy.AddError(msg)
    print pymsg
    print msg
    F.write(pymsg)
    F.write(msg)
    exit()

fields = [[u'String', u'GLOBALEVENTID'], [u'String', u'SQLDATE'], [u'String', u'MonthYear'], [u'String', u'Year'],
 [u'String', u'FractionDate'], [u'String', u'Actor1Code'], [u'String', u'Actor1Name'],
 [u'String', u'Actor1CountryCode'], [u'String', u'Actor1KnownGroupCode'], [u'String', u'Actor1EthnicCode'],
 [u'String', u'Actor1Religion1Code'], [u'String', u'Actor1Religion2Code'], [u'String', u'Actor1Type1Code'],
 [u'String', u'Actor1Type2Code'], [u'String', u'Actor1Type3Code'], [u'String', u'Actor2Code'],
 [u'String', u'Actor2Name'], [u'String', u'Actor2CountryCode'], [u'String', u'Actor2KnownGroupCode'],
 [u'String', u'Actor2EthnicCode'], [u'String', u'Actor2Religion1Code'], [u'String', u'Actor2Religion2Code'],
 [u'String', u'Actor2Type1Code'], [u'String', u'Actor2Type2Code'], [u'String', u'Actor2Type3Code'],
 [u'String', u'IsRootEvent'], [u'String', u'EventCode'], [u'String', u'EventBaseCode'], [u'String', u'EventRootCode'],
 [u'String', u'QuadClass'], [u'String', u'GoldsteinScale'], [u'String', u'NumMentions'], [u'String', u'NumSources'],
 [u'String', u'NumArticles'], [u'String', u'AvgTone'], [u'String', u'Actor1Geo_Type'], [u'String', u'Actor1Geo_FullName'],
 [u'String', u'Actor1Geo_CountryCode'], [u'String', u'Actor1Geo_ADM1Code'], [u'String', u'Actor1Geo_Lat'], [u'String', u'Actor1Geo_Long'],
 [u'String', u'Actor1Geo_FeatureID'], [u'String', u'Actor2Geo_Type'], [u'String', u'Actor2Geo_FullName'], [u'String', u'Actor2Geo_CountryCode'],
 [u'String', u'Actor2Geo_ADM1Code'], [u'String', u'Actor2Geo_Lat'], [u'String', u'Actor2Geo_Long'],
 [u'String', u'Actor2Geo_FeatureID'], [u'String', u'ActionGeo_Type'], [u'String', u'ActionGeo_FullName'],
 [u'String', u'ActionGeo_CountryCode'], [u'String', u'ActionGeo_ADM1Code'], [u'String', u'ActionGeo_Lat'],
 [u'String', u'ActionGeo_Long'], [u'String', u'ActionGeo_FeatureID'], [u'String', u'DATEADDED'], [u'String', u'SOURCEURL']]

outFile = 'Create_GDELT_Environment' + str(datetime.datetime.today()) + '.txt'
fileFixed = outFile.replace(':', '-')
outFilePath = os.path.join(outWS, fileFixed)

with open(outFilePath, 'w') as F:
    try:
        processStart = time.time()
        arcpy.AddMessage("Process Started at " + str(processStart))
        F.write("Process Started at " + str(processStart))

        # Create the output file geodatabase to hold the GDELT Data
        arcpy.CreateFileGDB_management(outWS, outGDB_name)
        outGDB = os.path.join(outWS, outGDB_name)
        arcpy.AddMessage('Successfully created file geodatabase!')
        F.write('Successfully created file geodatabase!')

        # Create the new feature class
        arcpy.CreateFeatureclass_management(outGDB, outFC_name, geometry_type="MULTIPOINT", spatial_reference=sr )
        outFC = os.path.join(outGDB, outFC_name)
        arcpy.AddMessage('Successfully created feature class!')
        F.write('Successfully created feature class!')

        # Add the necessary fields

        count = 0
        for field in fields:
            fType = field[0]
            fName = field[1]
            arcpy.AddField_management(outFC, field_name=fName, field_type=fType)
            count +=1
            arcpy.AddMessage('Successfully added field ' + str(count) + ' of ' + str(len(fields)) + "!")
            F.write('Successfully added field ' + str(count) + ' of ' + str(len(fields)) + "!")
    except:
        exitScript()
    finally:
        processEnd = time.time()
        processDuration = processEnd - processStart
        arcpy.AddMessage("Entire process took %d seconds" % int(processDuration))
        F.write("Entire process took %d seconds" % int(processDuration))
        F.close()