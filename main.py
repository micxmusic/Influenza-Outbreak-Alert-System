from reference import parse_data, align_counts, calculate_alert_levels

def test_alert(thresholds, counts, num_months=2):
    months = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
              7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"}
    count = 0
    #flag is used to check if the previous month exceeded the threshold
    flag = 0 
    
    #for loop cycles the list to find consecutive months that exceed threshold
    for i in range(len(counts)):
        #adding to count if the previous month already exceeds threshold
        if counts[i] > thresholds[i] and flag:
            count += 1
            #return the month that the number of threshold exceeds 
            #hits the specified number of consecutive months
            if count == num_months:
                return months[i+1]
        #sets count and flag to 1 for the first time the threshold is exceeded
        elif counts[i] > thresholds[i]:
            count = 1
            flag = 1
        #sets flag to zero when the month does not exceed threshold
        else:
            flag = 0
    
    #return value set if no alert is triggered
    return -1