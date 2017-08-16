import urllib2
import click
import xmltodict
from termcolor import colored

@click.command()
@click.option('--location', prompt='Your location:', help='Are you currently in work (Tara) or at home (Howth Junction)?')
def cli(location):
    """
    Docstring here yo...
    """
    times = retrieveDartTimes(retrieveXML(location), location)

def retrieveXML(source):
    """
    Retreive the raw XML from the Irish Rail API
    """
    return xmltodict.parse(
        urllib2.urlopen('{}/{}?{}'.format(
            'http://api.irishrail.ie/realtime/realtime.asmx'
            , 'getStationDataByCodeXML_WithNumMins'
            , 'StationCode={}&NumMins=60'.format('TARA' if source == 'w' else 'HWTHJ')
        )
    ).read())

def retrieveDartTimes(xmlroot, source):
    """
    Retrieve train times, print colour coded response
    """
    # Loop through all incoming trains
    for train in xmlroot['ArrayOfObjStationData']['objStationData']:
        # We only want Southbound trains if heading from home, Northbound if from work
        if (train['Direction'] == ('Northbound' if source == 'work' else 'Southbound')):
            print colored(
                '{} to {} arriving at {} ({} minutes)'.format(
                    train['Traintype']
                    , train['Destination']
                    , train['Exparrival']
                    , train['Duein']
                )
                , definePrintColour(int(train['Duein']))
            )

def definePrintColour(duein):
    """
    Using the provided duetime value, define a colour to be used when printing to output
    """
    # Color code based arrival time
    if duein > 45:
        return 'cyan'
    elif duein > 20:
        return 'green'
    elif duein > 15:
        return 'yellow'
    else:
        return 'red'
