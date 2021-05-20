'''
Time complexity is O(n). n - number of students.
Since the inner loop runs a constant number of times(6 in this case) everytime running time is 6*n which is O(n).

Space complexity is O(n).
Since the dictionary always consists of 6 items space complexity is n - dictionary to store the students.
'''

import csv
import sys

dictMax={'Maths':{'name':"",'mark':0},      #Stores the maximum in each subject
            'Biology':{'name':"",'mark':0},
            'English':{'name':"",'mark':0},
            'Physics':{'name':"",'mark':0},
            'Chemistry':{'name':"",'mark':0},
            'Hindi':{'name':"",'mark':0}}

first={'Name':"","total":0}     # first>=second>=thrid
second={'Name':"","total":0}
third={'Name':"","total":0}

with open(sys.argv[1]) as csvfile:

    for student in csv.DictReader(csvfile):             #Each row is a dictionary fo student data
        for subject,topper in dictMax.items():
            if(int(student[subject])>topper['mark']):               #If student's mark in subject is greater than topper mark then change topper
                    dictMax[subject]['name']=student['Name']        
                    dictMax[subject]['mark']=int(student[subject])
        total=0
        for key in student:
            if(key!="Name"):
                total+=int(student[key])

        if(total>=first['total']):              #total> first - third=second, second=first, first=student
            third.update(second)
            second.update(first)
            first['Name'], first['total']=student['Name'],total

        elif(total>=second['total']):           #total>second - third=second, second=student
            third.update(second)
            second['Name'], second['total']=student['Name'],total

        elif(total>=third['total']):            #total>third - third=student
            third['Name'], third['total']=student['Name'],total

    for subject,topper in dictMax.items():
        print("Topper in {0} is {1}\n".format(subject,topper['name']))

    print("Best students in the class are {0}, {1}, {2}".format(first['Name'],second['Name'],third['Name']))