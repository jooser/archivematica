#!/usr/bin/python

# author: jhs
# created: 2013-01-28
# project: Rockefeller Archivematica - Archivists Toolkit Integration

# notes: this script creates a sql script, that can be run against an AT database
#        it will insert digital object records into AT for existing Archival Descriptions objects
#
# inputs:  requires information about the AT database, and the location of the DIP, plus some metadata supplied by the user
#
# first version of this script gets the input from prompts, next version will get it from MCP db.
# 
# example usage:
#
# python at_import.py --host=localhost --port=3306 --dbname="ATTEST" --dbuser=ATuser --dbpass=hello --dip_location="/home/jhs/dip" --dip_name=mydip --atuser=myuser --use_statement="Image-Service" --uri_prefix="http://www.rockarch.org/" 
#

import os
import sys
import MySQLdb
from time import localtime, strftime
import argparse

#global variables
db = None
cursor = None
testMode = 0

def recursive_file_gen(mydir):
    for root, dirs, files in os.walk(mydir):
        for file in files:
            yield os.path.join(root, file)

def connect_db(atdbhost, atdbport, atdbuser, atpass, atdb):
    try:
        db = MySQLdb.connect(atdbhost,atdbuser,atpass,atdb)
        cursor = db.cursor()
        return True
    except Exception:
        raise

def process_sql(str):
    if testMode:
        print str
    else:
        cursor.execute(str)            

def get_user_input():
    print "Archivematica import to AT script"
    print "Welcome\n"
    atdbhost = raw_input("AT database hostname:")
    atdbport = raw_input("AT database port:")
    atdbuser = raw_input("AT database user name:")
    atpass = raw_input("AT database user password:")
    atuser = raw_input("AT username:")
    atdb = raw_input("AT database name:")

    dip_location = raw_input("Location of DIP:")
    dip_name = raw_input("Name of DIP:")

    object_type = raw_input("Object Type:")
    ead_actuate = raw_input("EAD Actuate:")
    ead_show = raw_input("EAD Show:")
    use_statement = raw_input("Use Statement:")

    uri_prefix = raw_input("prefix for uri:")
    #aip = raw_input("Name of mets file:")
    #fileName = raw_input("File name:")
    return atdbhost, atdbport, atdbuser, atpass, atdb, dip_location, dip_name, atuser, object_type, ead_actuate, ead_show, use_statement, uri_prefix


def get_files_from_dip(dip_location, dip_name):
    #need to find files in objects dir of dip:
    # go to dipLocation/dipName/objects
    # get a directory listing
    # for each item, set fileName and go
    try:
        mydir = dip_location + "/" + dip_name + "/objects/"
        mylist = list(recursive_file_gen(mydir))
        
        if len(mylist) > 0:
            return mylist
        else:
            raise ValueError("cannot find dip")
    except Exception:
        raise

def upload_to_atk(mylist, atuser, ead_actuate, ead_show, object_type, use_statement, uri_prefix):
    for f in mylist:
        print 'using ' + f
        file_name = os.path.basename(f)
        uuid = file_name[0:36]
        #aipUUID = aip[5:41]
        container1 = int(file_name[44:47])
        container2 = int(file_name[48:52])
        short_file_name = file_name[37:]
        time_now = strftime("%Y-%m-%d %H:%M:%S", localtime())
        file_uri = uri_prefix + "/" + file_name

        sql1 = "select a.archDescriptionInstancesId, a.resourceComponentId, b.dateBegin, b.dateEnd, b.dateExpression from ArchDescriptionInstances a join ResourcesComponents b on a.resourceComponentId = b.resourceComponentId where (container1numericIndicator = %d and container2NumericIndicator = %d)" % ( container1, container2);

        cursor.execute(sql1)
        data = cursor.fetchone()
        archDID = data[0]
        rcid = data[1]
        dateBegin = data[2]
        dateEnd = data[3]
        dateExpression = data[4]
 
        print "found archDescriptionInstancesId " + str(archDID) + ", rcid " + str(rcid)

        sql2 = "select repositoryId from Repositories" 

        cursor.execute(sql2)
        data = cursor.fetchone()
        repoId = data[0]

        sql3 = " select max(archDescriptionInstancesId) from ArchDescriptionInstances"
        cursor.execute(sql3)
        data = cursor.fetchone()
        newaDID = int(data[0]) + 1

        sql3a = "select max(fileVersionId) from FileVersions"
        cursor.execute(sql3a)
        data = cursor.fetchone()
        if not data[0]:
            newfVID = 1
        else:
            newfVID = int(data[0]) +1 

        sql4 = "insert into ArchDescriptionInstances (archDescriptionInstancesId, instanceDescriminator, instanceType, resourceComponentId, parentResourceId) values (%d, 'digital','Digital object',%d,1)" % (newaDID, rcid)

        process_sql(sql4)

        sql5 = """INSERT INTO DigitalObjects                  
           (`version`,`lastUpdated`,`created`,`lastUpdatedBy`,`createdBy`,`title`,
            `dateExpression`,`dateBegin`,`dateEnd`,`languageCode`,`restrictionsApply`,
            `eadDaoActuate`,`eadDaoShow`,`metsIdentifier`,`objectType`,`objectOrder`,
            `archDescriptionInstancesId`,`repositoryId`)
           VALUES (1,'%s', '%s','%s','%s','%s','%s',%d, %d,'English',%d,'%s','%s','%s','%s',0,%d,1)""" % (timeNow, timeNow, atuser, atuser, short_file_name,dateExpression, dateBegin, dateEnd, 0, ead_actuate, ead_show,uuid, object_type, newaDID)

        process_sql(sql5)

        sql6 = """insert into FileVersions (fileVersionId, version, lastUpdated, created, lastUpdatedBy, createdBy, uri, useStatement, sequenceNumber, eadDaoActuate, 
              eadDaoShow)
              values 
           (%d, 1, '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s','%s')""" % (newfVID,timeNow, timeNow,atuser,atuser,file_uri,use_statement,0, ead_actuate,ead_show)

        process_sql(sql6)
    
    print "done all files"
    processSql("commit")

if __name__ == '__main__':
    
    RESTRICTIONS_CHOICES=[ 'yes', 'no', 'premis' ]
    EAD_SHOW_CHOICES=['embed', 'new', 'none', 'other', 'replace']
    EAD_ACTUATE_CHOICES=['none','onLoad','other', 'onRequest']

    parser = argparse.ArgumentParser(description="A program to take digital objects from a DIP and upload them to an archivists toolkit db")
    parser.add_argument('--host', default="localhost", dest="atdbhost", 
        metavar="host", help="hostname or ip of archivists toolkit db")
    parser.add_argument('--port', type=int, default=3306, dest='atdbport', 
        metavar="port", help="port used by archivists toolkit mysql db")
    parser.add_argument('--dbname', dest='atdb', metavar="db",
        help="name of mysql database used by archivists toolkit")
    parser.add_argument('--dbuser', dest='atdbuser', metavar="db user")
    parser.add_argument('--dbpass', dest='atdbpass', metavar="db password")
    parser.add_argument('--dip_location', metavar="dip location")
    parser.add_argument('--dip_name', metavar="dip name")
    parser.add_argument('--atuser', metavar="at user")
    parser.add_argument('--restrictions', metavar="restrictions apply", default="premis", choices=RESTRICTIONS_CHOICES)
    parser.add_argument('--object_type', metavar="object type", default="")
    parser.add_argument('--ead_actuate', metavar="ead actuate", default="onRequest", choices=EAD_ACTUATE_CHOICES) 
    parser.add_argument('--ead_show', metavar="ead show", default="new", choices=EAD_SHOW_CHOICES )
    parser.add_argument('--use_statement', metavar="use statement")
    parser.add_argument('--uri_prefix', metavar="uri prefix")
    parser.add_argument('--access_conditions', metavar="conditions governing access", default="")
    parser.add_argument('--use_conditions', metavar="conditions governing use", default="")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    args =  parser.parse_args()
    if not (args.atdb):
        get_user_input()
    
    #print len(sys.argv)
    
    try:
        connect_db(args.atdbhost, args.atdbport, args.atdbuser, args.atdbpass, args.atdb)
        mylist = get_files_from_dip(args.dip_location, args.dip_name)
        upload_to_atk(mylist, args.atuser, args.ead_actuate, args.ead_show, args.object_type, args.use_statement, args.uri_prefix)
    except Exception as exc:
        print exc
    

