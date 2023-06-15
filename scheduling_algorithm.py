import calendar
import pandas as pd
import difflib
from operator import itemgetter

def createList(r1, r2):
    return list(range(r1, r2+1))

#This function will replace an assigned day, if requested.
def holiday(name, days):
    for i in range (0,len(workdf)):
        workers = workdf['Workers'][i]
        if workdf['Date'][i] in days:
            for s in range(0,len(workers)):
                temp = difflib.SequenceMatcher(None,name,workers[s])
                if temp.ratio() > 0.5:
                    workers[s] = 'Replace'
        workdf['Workers'][i] = workers
    return workdf

#This function identifies institutional holidays
def get_holidays(dates):
    for i in range (0,len(workdf)):
        if workdf['Date'][i] in dates:
            workdf['Workers'][i] = ["Collective day off"]
    return workdf

#This function allows input of individual holiday requests.
def get_dates(worker):
    days = input("Enter each day that "+ worker + " wants off separated by commas without spaces (eg. 1,4-7,23-31): ")
    d = days.split(",")
    listIndex=[]
    #Now, the ranges of numbers must become a list (eg. 1-5 must become 1,2,3,4,5)
    for item in range(0,len(d)):
        if '-' in d[item]:
            d[item]=d[item].split("-")
            d[item]=list(range(int(d[item][0]),int(d[item][1])+1,1))
        if type(d[item]) is not list:
            d[item]=int(d[item])
        else:
            listIndex.append(item)
    #Must make the input into a list and eliminate all of the integers as to not have duplicates
    if len(listIndex) >= 1:
        for item in range(0,len(d)):
            if item not in listIndex:
                d[listIndex[0]].append(d[item])
        no_integers = [x for x in d if not isinstance(x, int)]
    else:
        no_integers = d
    return no_integers

#This function will ensure balanced shifts / days amongst workers
def balance(schedule, workers, daysOff, prevResult):
    opertimes = {}
    #This for loop gets the amount of shifts that each person has and stores it in a list of tuples
    for i in range(0,len(schedule)):
        dailyAssigned = schedule['Workers'][i]
        for worker in workers:
            for name in dailyAssigned:
                temp = difflib.SequenceMatcher(None,worker,name)
                if temp.ratio() > 0.3:
                    if worker in opertimes:
                        number = opertimes.get(worker)
                        number += 1
                        opertimes[worker] = number
                    else:
                        opertimes[worker] = 1
    lowestTimes = sorted(opertimes.items(), key=lambda x:x[1])

    #In order to edit the tuples, they must be converted into lists and then converted back into a list of tuples
    for i in range(0,len(lowestTimes)):
        for x in range(0,len(prevResult)):
            if lowestTimes[i][0]== prevResult[x][0]:
                lowestTimes[i]=list(lowestTimes[i])
                lowestTimes[i][1]+=prevResult[x][1]
                lowestTimes[i]=tuple(lowestTimes[i])
    lowestTimes = dict(lowestTimes)
    lowestTimes = sorted(lowestTimes.items(), key=lambda x:x[1])
    result = [list(t) for t in lowestTimes]

    #This for- loop will iterate through the list of workers by lowest shifts, and check whether they are available to fill the next slot
    day = []
    for i in range(0,len(workdf)):
        result = sorted(result, key=itemgetter(1))
        date = workdf['Date'][i]
        for x in range(0,len(workdf['Workers'][i])):
            count = 0
            result = sorted(result, key=itemgetter(1))
            for l in range(0,len(workdf['Workers'][i])):
                replace = result[count][0]
                temp = difflib.SequenceMatcher(None,replace,workdf['Workers'][i][l])
                if temp.ratio() > 0.3:
                    count += 1
            while workdf['Workers'][i][x] == "Replace":
                replace = result[count][0]
                for d in daysOff:
                    if d[0] == replace:
                        day = d[1]
                if date not in day:
                    workdf['Workers'][i][x] = replace
                    result[count][1] = result[count][1] + 1
                else:
                    count += 1
    #This for loop will add the previous shift numbers on to this month's shift numbers in order to have a balanced schedule for multiple months
    for i in range(0,len(prevResult)):
        result[i][1]+=prevResult[i][1]
    return result
  
# Create a plain text calendar
c = calendar.TextCalendar(calendar.SUNDAY)
st = c.formatmonth(2023, 1, 0, 0)


# Create an HTML formatted calendar
hc = calendar.HTMLCalendar(calendar.THURSDAY)
st = hc.formatmonth(2025, 1)


"""for i in c.itermonthdays(2025, 4):
    print(i)

for name in calendar.month_name:
    print(name)

for day in calendar.day_name:
    print(day)"""

firstMonday=[]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#This initializes number of shifts as 0 for each worker
startResult = [['John', 0], ['Joe', 0], ['Bob', 0], ['Jane', 0], ['Tim', 0], ['James', 0], ['Robert', 0], ['Benjamin', 0]]
OR=[]
masterdf = pd.DataFrame(OR, columns = ['Date', 'Day of Week', 'Workers'])

#The lower bound on the range should be month number +1, and the upper bound must be month number +2. 
#For example this schedule is from September to December
for i in range(10,14):
    mo = months[i-2]
    for month in range(1, i):
        # It retrieves a list of weeks that represent the month
        mycal = calendar.monthcalendar(2023, month)
        # The first MONDAY has to be within the first two weeks
        week1 = mycal[0]
        week2 = mycal[1]
        if week1[calendar.MONDAY] != 0:
            auditday = week1[calendar.MONDAY]
        else:
            # if the first MONDAY isn't in the first week, it must be in the second week
            auditday = week2[calendar.MONDAY]
        firstMonday.append(auditday)


    #This is a sample schedule for a 5-day work week, with the empty lists being days with no one working
    #These can be edited to add or take away shifts, and people can be added or removed, but must be added or removed from all lists of workers
    firstWeek=[["John", "Joe", "Bob"],
            ["Jane", "Tim"],
            ["Robert"],
            ["John", "Bob"],
            ["Joe", "Robert"]]

    secondWeek=[["Joe", "Bob"],
                ["Jane", "Tim"],
                ["Robert"],
                ["John", "Bob"],
                ["James"]]

    thirdWeek=[["John", "Joe", "Benjamin"],
            ["Jane", "Tim"],
            ["Robert"],
            ["John", "James", "Benjamin"],
            []]

    fourthWeek=[["James", "Joe", "Benjamin"],
            ["Jane", "Tim"],
            ["Robert"],
            ["James", "Benjamin"],
            []]

    fifthWeek=[["James", "Joe", "Bob"],
            ["Jane", "Tim"],
            ["Robert"],
            ["John", "Benjamin"],
            []]

    OR=[]
    #This for- loop adds the monthly schedule to the calendar, so that it can be iterated through
    for week in mycal:
        del week[5:7]

        position=0
        for day in week:
            if day !=0 and position < 5:

                dayOfWeek=[day, position]

                if day <= 7:
                    dayOfWeek.append(firstWeek[position])
                elif 8<=day<=14:
                    dayOfWeek.append(secondWeek[position])
                elif 15<=day<=21:
                    dayOfWeek.append(thirdWeek[position])
                elif 22<=day<=28:
                    dayOfWeek.append(fourthWeek[position])
                else:
                    dayOfWeek.append(fifthWeek[position])

                OR.append(dayOfWeek)
            position+=1




    workdf = pd.DataFrame(OR, columns = ['Date', 'Day of Week', 'Workers'])

    #This for loop replaces numbers of days of the week with wording, making it easier to implement into a true schedule
    for day in workdf["Day of Week"]:
        if day==0:
            workdf['Day of Week'] = workdf['Day of Week'].replace([0], 'Monday')
        if day==1:
            workdf['Day of Week'] = workdf['Day of Week'].replace([1], 'Tuesday')
        if day==2:
            workdf['Day of Week'] = workdf['Day of Week'].replace([2], 'Wednesday')
        if day==3:
            workdf['Day of Week'] = workdf['Day of Week'].replace([3], 'Thursday')
        if day==4:
            workdf['Day of Week'] = workdf['Day of Week'].replace([4], 'Friday')

    
    workers = ['Benjamin', 'Bob', 'Tim', 'James', 'Jane', 'Robert', 'John', 'Joe']
    dct = {}

    #Get days off for everyone
    holidays = get_dates("Everyone")
    if type(holidays) is not list:
        workdf = get_holidays(holidays)
    else:
        workdf = get_holidays(holidays[0])
    
    #Get individual days off for each month and make them into a list
    print("For days in " + mo)
    for worker in workers:
        listOfDates = []
        dates = get_dates(worker)
        if type(dates) is list:
            dct[worker] = dates
        else:
            listOfDates.append(dates)
            dct[worker] = listOfDates

    datesList = list(map(list, dct.items()))

    for i in range(0,len(datesList)):
        if type(datesList[i][1][0]) is list:
            days = datesList[i][1][0]
            datesList[i][1]=days
        holiday(datesList[i][0], datesList[i][1])
    
    #All days must be balanced with the previous months days off
    startResult = balance(workdf, workers, datesList, startResult)
    masterdf = masterdf.append(workdf, ignore_index=False)

#The dataframe can now be printed and exported into an Excel file.
print(masterdf)
masterdf.to_excel(r'ORfall.xlsx', index = False)