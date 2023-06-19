import os
import csv

class EmployeeDetails:

    def __init__(self):
        self.storeEmployeeDetails={
        "salaryList":[],
        "nameList":[],
        "ageList":[],
        "jobTitleList":[],
        "deptNameList":[]
        }

    def enter_details(self):
        while True:
            self.name=input("Enter the name: ").capitalize()
            boolean=True
            for i in range(len(self.name)):
                aa=self.name[i]
                if aa.isalpha() or aa==" ":
                    boolean=True
                else:
                    boolean=False
                    break
            if boolean:
                self.storeEmployeeDetails["nameList"].append(self.name)
                break
                
            else:
                print("Enter the correct name")
                
        while True:        
            self.age=input("Enter the age: ")
            if self.age.isdigit():
                self.age=int(self.age)
                if self.age>=18 and self.age<=60:
                    self.storeEmployeeDetails["ageList"].append(self.age)                    
                    break
                else:
                    print("Enter correct age between 20 to 60")
            else:
                print("Enter correct age")
        while True:   
            self.jobTitle=input("Enter your job title: ").capitalize()
            boolean=True
            for i in range(len(self.jobTitle)):
                aa=self.jobTitle[i]
                if aa.isalpha() or aa==" ":
                    boolean=True
                else:
                    boolean=False
                    break
            if boolean:
                self.storeEmployeeDetails["jobTitleList"].append(self.jobTitle)
                break

            else:
                print("Enter the job title correctly")
                
        while True:      
            self.deptName=input("Enter your department: ").capitalize()
            boolean=True
            for i in range(len(self.deptName)):
                aa=self.deptName[i]
                if aa==" " or aa.isalpha():
                    boolean=True
                else:
                    boolean=False
            if boolean:
                self.storeEmployeeDetails["deptNameList"].append(self.deptName)
                break
                
            else:
                print("Enter correct job title")
               
        while True:
            self.salary=input("Enter your salary in rs: ")
            if self.salary.isdigit():
                self.salary=int(self.salary)
                if self.salary>=20000 and self.salary<=200000:
                    self.storeEmployeeDetails["salaryList"].append(self.salary)
                    break
                else:
                    print("Enter the salary in between 20000 to 200000")
            else:
                print("Enter correct salary")        



    def data_file(self,fileName): 
        if fileName[-4:] == ".csv":

            try:
                with open(fileName, 'a+') as f:
                    writer=csv.writer(f)
                    #writer.writerow(["Name","Age","Job Title","Department Name","Salary"])
                    for i in range(len(self.storeEmployeeDetails["salaryList"])):
                        a=self.storeEmployeeDetails["nameList"][i]
                        b=self.storeEmployeeDetails["ageList"][i]
                        c=self.storeEmployeeDetails["jobTitleList"][i]
                        d=self.storeEmployeeDetails["deptNameList"][i]
                        e=self.storeEmployeeDetails["salaryList"][i]
                        writer.writerow([a,b,c,d,e])
                    f.close()

            except IOError:
                print("Error: could not create file " + fileName)

        else:        
            try:
                with open(fileName, 'a+') as f:
                    for i in range(len(self.storeEmployeeDetails["salaryList"])): 
                        a=self.storeEmployeeDetails["nameList"][i]
                        b=self.storeEmployeeDetails["ageList"][i]
                        c=self.storeEmployeeDetails["jobTitleList"][i]
                        d=self.storeEmployeeDetails["deptNameList"][i]
                        e=self.storeEmployeeDetails["salaryList"][i]
                        f.write(f"\nName={a}\nAge={b}\nJob Title={c}\nDepartment Name={d}\nSalary={e}")

            except IOError:
                print("Error: could not create file " + fileName)

    def get_second_highest_salary(self):
        self.sortedSalaryList=self.storeEmployeeDetails["salaryList"].copy()
        self.sortedSalaryList.sort()
        return f"The second highest salary of the Employee is:{self.sortedSalaryList[-2]}rs"
    
    def get_details_by_name(self,name):
        self.name=name
        self.detailsByName=[]
        for i in range(len(self.storeEmployeeDetails["nameList"])):
            if name==self.storeEmployeeDetails["nameList"][i]:
                a=self.storeEmployeeDetails["nameList"][i]
                b=self.storeEmployeeDetails["ageList"][i]
                c=self.storeEmployeeDetails["jobTitleList"][i]
                d=self.storeEmployeeDetails["deptNameList"][i]
                e=self.storeEmployeeDetails["salaryList"][i]
                self.returnList=(f"Name={a} Age={b} Job Title={c} Department Name={d} Salary={e}")
                self.detailsByName.append(self.returnList)
            else:
                pass
        return self.detailsByName
    

if __name__=="__main__":

    obj=EmployeeDetails()

    while True:
        n=input("Enter the number of employee details you want to enter: ")
        if n.isdigit():
            n=int(n)
            if n>0:
                break
            else:
                print("Enter the number greater than zero")
        
        else:
            print("You have entered string please enter the number greater than zero")
        
    for i in range(n):
        print(f"Enter the details of employee{i+1}")
        obj.enter_details()
        
    while True:    
        fileName=input("Enter the file name where you want to store data: ")
        if ".csv" == fileName[-4:] or ".txt" == fileName[-4:]:
            obj.data_file(fileName)
            break
        else:
            ("Please enter the filname ending with .txt for text file or with .csv for csv file")

    if n>1:
        print(obj.get_second_highest_salary())
    else:
        pass

    while True:
        a=obj.storeEmployeeDetails["nameList"]
        name=input(f"Enter the name of the employee from this list: {a}, to get the details of that person:\n").capitalize()
        if name in a:
            print(obj.get_details_by_name(name))
            break
        else:
            print("Please enter the correct name from the list given above")