# automobile_dev

The program downloads and cleans the AutoMPG data set from UCI Machine Learning Repository. The data set consists of 398 records each having nine attributes. In my program I create a class called AutoMPG which creates objects for each car in the AutoMPG data set. I then create a derived class called AutoMPGData which has multiple functionalities from loading and cleaning the AutoMPG data set, to downloading the data set using the request module if it doesn't exist in the working environment. Further, there are functions to sort the AutoMPG objects by different attributes and I've implemented the argparse module to enhance command-line parsing for the program.

## Code practicing a variety of Python skills, specifically:
###  Base and derived classes
    *Creation of AutoMPG base class
        -Creates automobiles with make, model, and year
        -Addition of various methods to allow for object comparison and hashing
    *Creation of AutoMPGData derived class
        -Loads and cleans data files
        -Retrieves original data files from the internet if it doesn't exist
        -Includes methods for sorting data by various attributes
### Logging Module
    *Tracking creation of various .txt files 
    *Tracking HTTPrequests
    *Practicing logging to files and to the command line
### Requests Module
    *Downloads data file from UCI Machine Learning Repository and writes content to local file
### Argparse Module
    *Implements enhanced command-line parsing for the program
    *Implements an argument to sort through all automobile objects by year, mpg, or the default sorting based on a user input 
    *A required "print" command iterates through and prints each object in the the sorted list of AutoMPG objects