# IMPORTS
import csv
from collections import namedtuple
import re
import os
import logging
from operator import attrgetter
import requests
import argparse

# get root logger, set default to DEBUG
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# file handler
fh = logging.FileHandler('autompg2.log', 'w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
logger.addHandler(sh)

class AutoMPG:
    """
    Creates an automobile consisting of the make,
    model, year, and mpg of the vehicle.

    Attributes:
    ----------------------------------------
        make (str): make of car
        model (str): model of car
        year (int): model year
        mpg (float): miles per gallon car gets
        other (class object): AutoMPG class object.

    Methods:
    ----------------------------------------
        __init__: constructor. Creates automobile 
        with make, model, year, and mpg.
        __repr__: printable representation of object.
        __str__: informal representation of object.
        __eq__: compares equality of two class objects.
        __lt__: implements functionality of less than operator
                on the two class objects.
    """
    def __init__(self, make, model, year, mpg):
        """
        Construct AutoMPG 

        Args: 
        make (str): make of car
        model (str): model of car
        year (int): model year
        mpg (float): miles per gallon car gets

    """
        self.make = make.title()
        self.model = model.title()
        self.year = int(year)
        self.mpg = float(mpg)
    
    def __repr__(self):
        """
        Creates a printable representation of AutoMPG object.

        Return:
            (str): representation of AutoMPG in the form (AutoMPG('make', 'model', year, mpg))

        """
        return f"AutoMPG('{self.make}', '{self.model}', {self.year}, {self.mpg})"
    
    def __str__(self):
        """
        Creates informal representation of AutoMPG object,

        Return:
            (str): informal representation of AutoMPG in the form "year make model"
        """

        return f"{self.year} {self.make} {self.model}"
    
    def __eq__(self, other):
        """
        Allows for equality comparison between AutoMPG objects. Make/model are compared
        in typical Python comparison format. Year and mpg are compared in typical int comparison
        format.

        Args:
            other (class object): instance of AutoMPG class

        Return:
            equality comparison of AutoMPG class or NotImplemented
        """
        if type(self) == type(other):
            return (self.make == other.make) and (self.model == other.model) and \
            (self.year == other.year) and (self.mpg == other.mpg)
        else:
            return NotImplemented
    
    def __lt__(self, other):
        """
        Implements functionality of less than operator between AutoMPG objects. Make/model are compared
        in typical Python comparison format. Year and mpg are compared in typical int comparison
        format.

        Args:
            other (class object): instance of AutoMPG class

        Return:
            less than comparison of AutoMPG class or NotImplemented
        """
        if type(self) == type(other):
            return (self.make, self.model, self.year, self.mpg) < \
                (other.make, other.model, other.year, other.mpg)
        else: 
            return NotImplemented
    
    def __hash__(self):
        """
        Hashes AutoMPG attributes.

        Return:
            (tuple): hashable AutoMPG attributes
        """
        return hash((self.make, self.model, self.year, self.mpg))

class AutoMPGData:
    CLEANFILE = 'auto-mpg.clean.txt'
    ORIGINALFILE = 'auto-mpg.data.txt'

    def __init__(self):
        """
        Creates empty list to hold AutoMPG objects. Loads clean data.

        """
        self.data = []
        self._load_data()

    def __iter__(self):
        """
        Allows iteration over data list.

        Return:
            Iterator over list.
        """
        return iter(self.data)

    def _load_data(self):
        """
        Creates AutoMPG instances using cleaned auto data.

        Return:
            (list): data list containing all AutoMPG instances from auto data.
        """
        # check if original data file exists
        if not os.path.exists(self.ORIGINALFILE):
            # log absence of original file
            logging.debug("Original data file does not exist.")
            # if original data file doesn't exist, run _get_data() method
            self._get_data()

        # check if clean data file exists
        if not os.path.exists(self.CLEANFILE):
            # log absence of clean file
            logging.debug("Clean data file doesn't exist.")
            # if clean data file doesn't exist, run _clean_data method
            self._clean_data()
            # run _load_data method again
            self._load_data()

        else:
            # if clean data file does exists
            # create namedtuple "Record" that holds attributes corresponding to data column values 
            Record = namedtuple('Record', ['mpg', 'cylinders', 'displacement', 'horsepower',
                                'weight', 'acceleration', 'model_year', 'origin', 'car_name'])
            # open clean data file to read
            with open(self.CLEANFILE, "rt") as f:
                reader = csv.reader(f, delimiter=" ", skipinitialspace=True)
                for line in reader:

                    # # create Record objects for each line
                    records = Record(line[0], line[1], line[2], line[3], line[4], \
                        line[5], line[6], line[7], line[8:])
                    
                    # # instantiate AutoMPG objects and add them to data list
                    self.data.append(AutoMPG(records.__getattribute__('car_name')[0], " ".join(records.__getattribute__('car_name')[1:]),
                            '19'+str(records.__getattribute__('model_year')), records.__getattribute__('mpg')))
        return self.data
        
                
    def _clean_data(self):
        """
        Cleans auto-mpg.data.txt. Fields in .txt file are separated
        by spaces and tabs, which must be dealt with.
        """
        # self.file = file
        # open auto-mpg.data
        with open(self.ORIGINALFILE, "rt") as f:
            reader = csv.reader(f)
            # create auto-mpg.clean.txt
            with open(self.CLEANFILE, "w") as f:
                writer = csv.writer(f)
                for line in reader:
                    for string in line:
                        # turn tab in each row into 1 space
                        line = string.expandtabs(1)
                        # get rid of unnecessary quotations around each car make/model
                        line = re.sub('"', '', line)
                        writer.writerow([line])
        logging.info(f"{self.CLEANFILE} file created")
    
    def _get_data(self):
        """Receives automobile data from website and creates a .txt file"""
        get_data = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data')

        if get_data:
            logging.info("Data received from website")
        else:
            logging.error("Data not received from website.")

        open("auto-mpg.data.txt", "wb").write(get_data.content) 
        logging.info(f"{self.ORIGINALFILE} file created")


    def sort_by_default(self):
        """Sorts data list of all AutoMPG objects. List will be sorted by make, 
        model, year, and then mpg"""
        self.data.sort()
        return self.data
    
    def sort_by_year(self):
        """Sorts data list of all AutoMPG objects. List sorted by year, make, model,
         and then mpg """
        self.data.sort(key=attrgetter('year', 'make', 'model', 'mpg'))
        return self.data
    
    def sort_by_mpg(self):
        """Sorts data list of all AutoMPG objects. List sorted by mpg, make, model,
        and then year."""
        self.data.sort(key=attrgetter('mpg', 'make', 'model', 'year'))
        return self.data


def main(): 
    create_auto = AutoMPGData()
    parser = argparse.ArgumentParser(description='analyze Auto MPG data set')
    parser.add_argument('-s', '--sort', metavar='<sort order>', choices=['year', 'mpg', 'default'], 
                        help='choose a sorting option, must be: "year, "mpg", or "default"', type=str)
    parser.add_argument('command', metavar='<command>', help='type "print" to print sorted automobile list',
                        choices='print', type=str)
    args = parser.parse_args()

    # if year typed in command line after file
    if args.sort.lower() == 'year':
        create_auto.sort_by_year()
    # if mpg typed in command line after file
    elif args.sort.lower() == 'mpg':
        create_auto.sort_by_mpg()
    # if default typed in command line after file
    elif args.sort.lower() == 'default':
        create_auto.sort_by_default()

    # if print typed in command line affater year, mpg, or default
    if args.command == 'print':
        for auto in create_auto:
            print(auto)


if __name__ == '__main__':
    main()
