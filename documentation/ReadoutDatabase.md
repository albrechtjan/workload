How to extract the data from the database and analyse it
------------

 * Log onto the server. At the moment, the server is `survey.zqa.tu-dresden.de`
 * Dump the databse: `mysqldump -u WORKLOAD_USER --password='<db-password-here>'  WORKLOAD_DB > dump.db` You can find the database password via the `settings.py` of the django project. There the password is being loaded from a file, so go to the file, and there you find the password.
 * Copy the dump.db file to your local machine.
 * On your local machine, import the database dump back into a database. On Debian, this means you have to:
    * Install MySQL `sudo apt install mysql-server mysql-client`
    * Start the MySQL console `mysql -u root -p`
    * Create a database `create database <database-name>;`
    * Exit the MySQL shell with Ctrl+D
    * Load the database dump into the database: `mysql <database-name> -u root -p < pfad/zum/databasedump.sql`
  * Now, you can view the tables in the database with graphical interfaces such as [`MySQL Workbench`](https://www.mysql.com/products/workbench/). MySQL Workbench also supports CSV export, so you can export the tables to `.csv` and then re-import them to any spreadsheet software such as Google Sheets or Microsoft Excel.

To understand the meaning of the data in the database, read [TableStructure.md](TableStructure.md)

  
