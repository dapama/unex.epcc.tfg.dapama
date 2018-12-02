from ftplib import FTP

# podaac-ftp.jpl.nasa.gov/allData/quikscat/L2B12/v4.0

ftp = FTP ( 'podaac-ftp.jpl.nasa.gov' )
print ( ftp.getwelcome () )
ftp.login ()
ftp.cwd ( '/allData/quikscat/L2B12/v4.0' )

files_by_years = list ( filter ( lambda dir: dir.isdigit (), ftp.nlst () ) )

try :
    print ( 'Year\'s data available:' )
    print ( files_by_years )

    year = int ( input ( 'Select the year of which you want to download the data: ' ) )
    if ( str ( year ) in files_by_years ) :
        print ( 'Year selected: , %s.' % year )  
        ftp.cwd ( str ( year ) )
        print ( ftp.nlst () ) 
    else :
        print ( 'Year selected not available.' )

except ( NameError, SyntaxError ) :
    print( 'This is not a whole number.' )

ftp.quit()