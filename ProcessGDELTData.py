#Importing System Modules
import shutil, os, traceback, sys, time, datetime
import csv
import arcpy
env = arcpy.env

#File Paths
finalFC = arcpy.GetParameterAsText(0)
spatialRef = arcpy.Describe(finalFC).spatialReference
csvPath = arcpy.GetParameterAsText(1)
finalGDB = arcpy.GetParameterAsText(2)
logPath = arcpy.GetParameterAsText(3)

# Helper Functions
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
    exit


TempCSV = []


if __name__ == '__main__':

    outFile = 'Process_GDELT' + str(datetime.datetime.today()) + '.txt'
    fileFixed = outFile.replace(':', '-')
    outFilePath = os.path.join(logPath, fileFixed)

    with open(outFilePath, 'w') as F:
        try:
            for root, dirs, files in os.walk(csvPath):
                for file in files:
                    if file.endswith(".CSV"):
                        csvPath = os.path.join(root, file)
                        TempCSV.append(csvPath)
            print("There are %s CSV files to process." % str(len(TempCSV)))
            arcpy.AddMessage("There are %s CSV files to process." % str(len(TempCSV)))
            F.write("There are %s CSV files to process." % str(len(TempCSV)))

            processStart = time.time()

            out_Name = os.path.basename(finalFC)
            geometry_type = "MULTIPOINT"
            has_m = "DISABLED"
            has_z = "DISABLED"
            ws = finalGDB

            env.overwriteOutput = 1
            if not arcpy.Exists(finalFC):
                arcpy.CreateFeatureclass_management(ws, out_Name, geometry_type, template, has_m, has_z, spatialRef)

    
            fieldsToUpdate = ("SHAPE@", "GLOBALEVENTID", "SQLDATE", "MonthYear", "Year", "FractionDate", "Actor1Code", "Actor1Name", "Actor1CountryCode", "Actor1KnownGroupCode", "Actor1EthnicCode", "Actor1Religion1Code", "Actor1Religion2Code",
                "Actor1Type1Code", "Actor1Type2Code", "Actor1Type3Code", "Actor2Code", "Actor2Name", "Actor2CountryCode", "Actor2KnownGroupCode", "Actor2EthnicCode", "Actor2Religion1Code", "Actor2Religion2Code", "Actor2Type1Code", "Actor2Type2Code",
                "Actor2Type3Code", "IsRootEvent", "EventCode", "EventBaseCode", "EventRootCode", "QuadClass", "GoldsteinScale", "NumMentions", "NumSources", "NumArticles", "AvgTone", "Actor1Geo_Type", "Actor1Geo_FullName", "Actor1Geo_CountryCode",
                "Actor1Geo_ADM1Code", "Actor1Geo_Lat", "Actor1Geo_Long", "Actor1Geo_FeatureID", "Actor2Geo_Type", "Actor2Geo_FullName", "Actor2Geo_CountryCode", "Actor2Geo_ADM1Code", "Actor2Geo_Lat", "Actor2Geo_Long", "Actor2Geo_FeatureID",
                "ActionGeo_Type", "ActionGeo_FullName", "ActionGeo_CountryCode", "ActionGeo_ADM1Code", "ActionGeo_Lat", "ActionGeo_Long", "ActionGeo_FeatureID", "DATEADDED", "SOURCEURL")
            csvCount = 0
            for t in TempCSV:
                csvCount += 1
                rowCount = 0
                errorCount = 0
                validPointCount = 0
                print("  Processing CSV file %s ,  %d of %d..." % (t, csvCount, len(TempCSV)))
                arcpy.AddMessage("  Processing CSV file %s ,  %d of %d..." % (t, csvCount, len(TempCSV)))
                F.write("  Processing CSV file %s ,  %d of %d..." % (t, csvCount, len(TempCSV)))
                startTime = time.time()

                cursor = arcpy.da.InsertCursor(finalFC, fieldsToUpdate)

                print("    Starting at " + time.ctime(startTime))
                arcpy.AddMessage("    Starting at " + time.ctime(startTime))
                F.write("    Starting at " + time.ctime(startTime))
                with open(t, 'rb') as f:
                    csvreader = csv.reader(f, delimiter='\t', quotechar='|')
                    for row in csvreader:
                        arcpy.AddMessage("Completed " + str(rowCount) + " rows...")
                        iRow = []
                        rowCount += 1

                        features = []
                        array = arcpy.Array()

                        if row[39] != '':
                            if row[40] != '':
                                point1 = arcpy.Point((float(row[40])), (float(row[39])))
                                array.add(point1)

                        if row[46] != '':
                            if row[47] != '':
                                point2 = arcpy.Point((float(row[47])), (float(row[46])))
                                array.add(point2)

                        if row[53] != '':
                            if row[54] != '':
                                point3 = arcpy.Point((float(row[54])), (float(row[53])))
                                array.add(point3)

                        if len(array) > 0:
                            ptGeo = arcpy.Multipoint(array)
                            validPointCount += 1

                            i = -1
                            for field in fieldsToUpdate:
                                if i < 0:
                                    iRow.append(ptGeo)
                                    i+=1
                                else:
                                    iRow.append(row[i])
                                    i+=1

                        try:
                            cursor.insertRow(iRow)

                        except:
                            print("Error on " + str(rowCount) + " skipping")
                            arcpy.AddMessage("Error on " + str(rowCount) + " skipping")
                            errorCount += 1
                            F.write("Error on " + str(rowCount) + " skipping")



                dataPct = ((float(validPointCount) / float(rowCount)) * 100)

                endTime = time.time()
                print("    Finished at " + time.ctime(endTime))
                print("    Process took %d seconds" % int(endTime-startTime))


                arcpy.AddMessage("    Finished at " + time.ctime(endTime))
                arcpy.AddMessage("    Process took %d seconds" % int(endTime-startTime))

                F.write("    Finished at " + time.ctime(endTime))
                F.write("    Process took %d seconds" % int(endTime-startTime))


            processEnd = time.time()
            processDuration = processEnd - processStart

            print("There were a total of %s errors" % str(errorCount))
            print("Entire process took %d seconds" % int(processDuration))
            arcpy.AddMessage("Entire process took %d seconds" % int(processDuration))
            arcpy.AddMessage("There were a total of %s errors" % str(errorCount))

            F.write("Entire process took %d seconds" % int(processDuration))
            F.write("There were a total of %s errors" % str(errorCount))
            F.close()

        except:
            exitScript()