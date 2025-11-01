#File: voter_analysis/models.py
#Author: Aaron Huang (ahuan@bu.edu), 10/28/2025
#Description: models.py defines the database schema and loads data from local csv for Voter.
from django.db import models
from datetime import datetime
# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data of newton voters 
    '''
    last_name = models.CharField(default="")
    first_name = models.CharField(default="")

    # residential address 
    street_number = models.CharField(default="")
    street_name =  models.CharField(default="")
    apartment_number = models.CharField(default="")
    zip_code = models.CharField(default="")

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.CharField(max_length=2, default="")
    precinct_number = models.CharField(max_length=2, default="")


    #booleans on whether or not vote participated in recent elections
    v20state = models.BooleanField(null=True, blank=True)
    v21town = models.BooleanField(null=True, blank=True)
    v21primary = models.BooleanField(null=True, blank=True)
    v22general = models.BooleanField(null=True, blank=True)
    v23town = models.BooleanField(null=True, blank=True)

    #numeric value indicating how many of the past 5 elections the voter participated in 
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """String representation"""
        return f'voter {self.last_name}, {self.first_name}:{self.street_number} {self.street_name} {self.zip_code}'
    
def parse_booleans (b):
    return b=="TRUE"

def load_data():
    '''function to load data records from CSV file into Django database'''

    Voter.objects.all().delete()
    
    filename="C:/Users/13477/Downloads/newton_voters.csv"
    f=open(filename,'r') # open the file for reading

    #read oast the categories:
    f.readline() #do nothing

    #read all rows 
    for line in f:
        fields = line.strip().split(',') #split comma seperated values
        try:
            voter = Voter(last_name = fields[1],
                    first_name = fields[2],
                    street_number = fields[3],
                    street_name =  fields[4],
                    apartment_number = fields[5],
                    zip_code = fields[6],

                    date_of_birth = (fields[7]),
                    date_of_registration = fields[8],
                    party_affiliation = fields[9],
                    precinct_number = fields[10],

                    v20state = parse_booleans(fields[11]),
                    v21town = parse_booleans(fields[12]),
                    v21primary = parse_booleans(fields[13]),
                    v22general = parse_booleans(fields[14]),
                    v23town = parse_booleans(fields[15]),

                    voter_score = fields[16],
                )
            voter.save()
        except:
            print(f'error creating voter on line : {line}')
    print("created ", len(Voter.objects.all()), "voters")