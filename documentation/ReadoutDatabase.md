How to extract the data from the database and analyse it
------------

The data entered


  
  
Also, zuerst musst du mysql-client und mysql-server bei dir installieren. Auf Ubuntu geht das zum Beispiel mit 
sudo apt install mysql-server mysql-client

Dann startest du mysql als root user, auf Ubuntu geht das mit

mysql -u root -p

Dann erstellst du eine Datenbank mit dem folgenden Kommando:

create database workloaddata;

Du kannst natürlich der Datenbank auch einen andern Namen geben.

Dann beendest du mysql mit Ctrl+D

Dann benutzt du das Kommando

mysql dbcopy -u root -p < pfad/zum/databasedump.sql

  
