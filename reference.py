import csv
import statistics
from collections import defaultdict as dd

def parse_data(filename):
    
    #initialize list of valid years and months to use for checking
    valid_years = ["2010", "2011", "2012", "2013", "2014"]
    valid_months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", 
                    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    valid_records = 0
    invalid_records = 0
    
    #opening and reading of the file of records
    with open(filename) as fp:
        data = csv.reader(fp)
        #skipping over the header row
        next(data)
        data = list(data)
        raw_data = dd(int)
        output_list = []
        
        #iterating through each row in the file
        for row in data:
            #checking for validity of year and month
            #increments corresponding count and value in raw_data (dd)
            if row[0] in valid_years and row[1] in valid_months:
                    valid_records +=1
                    raw_data[(row[0], row[1])] +=1
            else:
                invalid_records +=1
        
        #appending records in order into output list by year    
        for year in valid_years:
            yearlist = []
            month_records = 0
            #appending records in order into a list by month 
            for month in valid_months:
                month_records = raw_data[(year, month)]
                yearlist.append(month_records)
            output_list.append(yearlist)
                    
    return(output_list, valid_records, invalid_records)

def align_counts(raw_counts):
    output = []
    align_list = []
    
    #compiles the index at which the peak value occurs for each year
    for i in range(len(raw_counts)):
        align_max = max(raw_counts[i])
        align = raw_counts[i].index(align_max)
        align_list.append(align)
    #compiled list is sorted and the alignment index is found by taking median
    align_list.sort()
    align_index = align_list[2] 
    
    #iterate through each year and align peak to the earlier index set
    for year_list in raw_counts:
        max_val = max(year_list)
        curr_pos = year_list.index(max_val)
        #loop with conditions to ensure that the first occuring peak will be
        #aligned to the earlier set index
        while year_list[align_index] != max_val:
            if curr_pos > align_index :
                year_list.insert(len(year_list),year_list.pop(0))
            else:
                year_list.insert(0,year_list.pop())

        #appending the cycled lists into the output by year        
        output.append(year_list)
    return output

def calculate_alert_levels(aligned_counts):
    total = 0
    mean = 0
    sd = 0
    alert = 0
    mean_case = []
    alert_threshold = []
    
    #cycle by element index in list
    for i in range(12):
        month_list = []
        #extracting all the case counts for the month in all the years
        for year_list in aligned_counts:
            month_list.append(year_list[i])
        mean = statistics.mean(month_list)
        sd = statistics.stdev(month_list)
        alert = mean + 1.645 * sd
        #appending mean and alert values into respective lists by month
        mean_case.append(mean)
        alert_threshold.append(alert)
    
    return (mean_case, alert_threshold)
