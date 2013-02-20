#!/bin/bash

# This file is part of Archivematica.
#
# Copyright 2010-2013 Artefactual Systems Inc. <http://artefactual.com>>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica. If not, see <http://www.gnu.org/licenses/>>.

# @package Archivematica
# @author Joseph Perry <joseph@artefactual.com>>
# @version svn: $Id$

origDir="`pwd`"
cd "`dirname $0`"
databaseName="MCP"
set -e
echo -n "Enter the DATABASE root password (Hit enter if blank):"
read dbpassword

if [ ! -z "$dbpassword" ] ; then
  dbpassword="-p${dbpassword}"
else
  dbpassword=""
fi


mysqldump="mysqldump -u root ${dbpassword} ${databaseName}"
dumpTables="--skip-triggers --skip-comments -d"
dumpData="--skip-triggers --skip-comments --no-create-info --extended-insert=FALSE --complete-insert=TRUE --order-by-primary"
# Quick load dump for testing
#dumpData="--skip-triggers --skip-comments --no-create-info --extended-insert=TRUE"
MCPDumpSQLLocation="../src/MCPServer/share/mysql"

#echo 'START TRANSACTION;' > $MCPDumpSQLLocation
echo 'SET foreign_key_checks = 0;' > $MCPDumpSQLLocation
#Transcoder
#Reset counters for commit
mysql -u root ${dbpassword} ${databaseName} --execute "UPDATE CommandRelationships SET countAttempts=0, countOK=0, countNotOK=0;"
$mysqldump CommandTypes CommandClassifications CommandsSupportedBy Commands FileIDTypes FileIDs CommandRelationships  Groups FileIDGroupMembers SubGroups DefaultCommandsForClassifications FileIDsBySingleID FilesIdentifiedIDs $dumpTables >> $MCPDumpSQLLocation
$mysqldump CommandTypes CommandClassifications CommandsSupportedBy Commands FileIDTypes FileIDs CommandRelationships  Groups FileIDGroupMembers SubGroups DefaultCommandsForClassifications FileIDsBySingleID $dumpData >> $MCPDumpSQLLocation #Source of FPR DATA


#Dashboard
#-- Dashboard dump tables --
$mysqldump auth_message auth_user auth_user_groups auth_user_user_permissions auth_group auth_group_permissions auth_permission django_content_type django_session SourceDirectories $dumpTables >> $MCPDumpSQLLocation
$mysqldump auth_message auth_user_groups auth_user_user_permissions auth_group auth_group_permissions auth_permission django_content_type $dumpData >> $MCPDumpSQLLocation



echo 'SET foreign_key_checks = 1;' >> $MCPDumpSQLLocation
#echo 'COMMIT;' >> $MCPDumpSQLLocation

sed -i -e 's/ AUTO_INCREMENT=[0-9]\+//' $MCPDumpSQLLocation

#VIEWS
#-- MCP-views --
##$mysqldump filesPreservationAccessFormatStatus jobDurationsView lastJobsInfo lastJobsTasks processingDurationInformation processingDurationInformation2 processingDurationInformationByClient taskDurationsView transfersAndSIPs $dumpTables >> $MCPDumpSQLLocation

#-- Transcoder-views --
##$mysqldump filesPreservationAccessFormatStatus  >> $MCPDumpSQLLocation

#-- Dashboard dump Dashboard-views --
##$mysqldump developmentAide_choicesDisplayed $dumpTables >> $MCPDumpSQLLocation

cd "$origDir"
