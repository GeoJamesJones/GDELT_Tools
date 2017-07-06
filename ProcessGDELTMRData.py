#Importing System Modules
import shutil, os, traceback, sys, logging, time, zipfile, numpy
import csv
import arcpy
env = arcpy.env

#File Paths
topPath = r"D:\GDELT"
csvPath = os.path.join(topPath, "MasterReduced")
finalGDB = os.path.join(topPath, "GDELT.gdb")
finalFC = r'D:\GDELT\GDELT.gdb\GDELT_MR_1979_2013'
spatialRef = arcpy.Describe(finalFC).spatialReference
t = r'D:\GDELT\MasterReduced\GDELT.MASTERREDUCEDV2.TXT'

fields = ["SHAPE@", 'Date', 'Source', 'Target', 'CAMEOCode', 'NumEvents', 'NumArts', 'QuadClass', 'Goldstein', 'SourceGeoType', 'SourceGeoLat', 'SourceGeoLong', 'TargetGeoType', 'TargetGeoLat', 'TargetGeoLong', 'ActionGeoType', 'ActionGeoLat', 'ActionGeoLong']

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
    logging.info(pymsg)
    logging.info(msg)
    exit

if __name__ == '__main__':

    try:
        processStart = time.time()

        rowCount = 0
        validPointCount = 0
        startTime = time.time()
        cursor = arcpy.da.InsertCursor(finalFC, fields)
        arcpy.AddMessage("    Starting at " + time.ctime(startTime))

        with open(t, 'rb') as f:
            csvreader = csv.reader(f, delimiter='\t', quotechar='|')
            for row in csvreader:
                iRow = []
                rowCount += 1

##                print row

                if rowCount == 1:
                   arcpy.AddMessage("Passing Header Information..")

                elif len(row) == 17:

                    features = []
                    array = arcpy.Array()

                    if row[9] != '':
                        if row[10] != '':
                            point1 = arcpy.Point((float(row[10])), (float(row[9])))
                            array.add(point1)

                    if row[12] != '':
                        if row[13] != '':
                            point2 = arcpy.Point((float(row[13])), (float(row[12])))
                            array.add(point2)

                    if row[15] != '':
                        if row[16] != '':
                            point3 = arcpy.Point((float(row[16])), (float(row[15])))
                            array.add(point3)

                    if len(array) == 3:
                        ptGeo = arcpy.Multipoint(array)
                        validPointCount += 1


                        i = -1
                        for field in fields:
    ##                        print field
                            if i < 0:
                                iRow.append(ptGeo)
##                                print ptGeo
                                i+=1
                            else:
                                iRow.append(row[i])
##                                print row[i]
                                i+=1

                    if len(iRow) > 0:
                        cursor.insertRow(iRow)
##                        print iRow

        if rowCount % 100 == 0:
           arcpy.AddMessage("Processed %s rows of data" % str(rowCount))
        else:
            arcpy.AddMessage(".")

        endTime = time.time()
        arcpy.AddMessage("    Finished at " + time.ctime(endTime))
        arcpy.AddMessage("    Process took %d seconds" % int(endTime-startTime))

    except:
        exitScript()