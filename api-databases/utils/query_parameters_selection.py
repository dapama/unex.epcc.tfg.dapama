

import sys


# https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response



def ask_for_a_query_date( ):

    dates_array = []

    op = True
    while op != False:
        print 'Insert the year which you want to add into the Temporal Query Array: '
        year1 = raw_input( 'Year (e.g.: 2018): ' )
        day1 = raw_input( 'Day (between 001 and 365): ' )

        dates_array.append( int( year1 + day1 ) )

        op = query_yes_no('Do you want to add another year?')

    return dates_array


def ask_for_a_query_box():
    print 'Insert the coordinates to describe the Query Box: '
    print 'Point 1: '
    lat1 = raw_input( 'Latitude (between -90 and 90): ' )
    long1 = raw_input( 'Longitude (between -180 and 180): ' )
    print 'Point 2: '
    lat2 = raw_input( 'Latitude (between -90 and 90): ' )
    long2 = raw_input( 'Longitude (between -180 and 180): ' )

    return lat1, long1, lat2, long2


def query_yes_no( question, default="yes" ):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError( "invalid default answer: '%s'" % default )

    while True:
        sys.stdout.write( question + prompt )
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")