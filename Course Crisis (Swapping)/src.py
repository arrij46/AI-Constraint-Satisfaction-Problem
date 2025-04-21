# Arrij Fawwad
# I220755
# C 

FileName = "Data/data1.txt"

def ReadFile(Data):
    with open(FileName, 'r') as file:
        for line in file:
            word = line.strip().split()
            if len(word) < 4:
                continue  

            rollno = word[0]

            CurrCourseWord = []
            i = 1
            while i < len(word) and '-' not in word[i]:
                CurrCourseWord.append(word[i])
                i += 1

            if i >= len(word):
                continue  
            CurrCourseWord.append(word[i])
            CurrCourse = ' '.join(CurrCourseWord)

            i += 1
            if i >= len(word):
                continue

            CurrSec = word[i]

            i += 1
            if i >= len(word):
                DesiredSection = "replace"
                DesiredCourse = ""
            elif len(word[i]) == 1: 
                DesiredSection = word[i]
                i += 1
                DesiredCourse = ' '.join(word[i:]) if i < len(word) else ""
            else:
                DesiredSection = "replace"
                DesiredCourse = ' '.join(word[i:])

            if rollno not in Data:
                Data[rollno] = []

            Data[rollno].append([CurrCourse, CurrSec, DesiredSection, DesiredCourse])

def FixData(Data):
    for rollno, CourseAlloacation in Data.items():
        for i in range(len(CourseAlloacation)):
            if CourseAlloacation[i][2] == "replace":
                CourseAlloacation[i][2] = CourseAlloacation[i][3][-1]

class Student:
    def __init__(self, rollno, CurrCourse, CurrSec, DesiredSection, DesiredCourse):
        self.rollno = rollno
        self.CurrCourse = CurrCourse
        self.CurrSec = CurrSec
        self.DesiredSection = DesiredSection
        self.DesiredCourse = DesiredCourse
        self.done = False
        
        words = DesiredCourse.split('-')
        if len(words) > 1:
            self.DesiredCourseName = words[0]
        else:
            self.DesiredCourseName = DesiredCourse
            
        words = CurrCourse.split('-')
        if len(words) > 1:
            self.CurrCourseName = words[0]
        else:
            self.CurrCourseName = CurrCourse

class Swapper:
    def __init__(self):
        self.students = []
        self.CourseMap = {}  
        self.SwapPair = []
    
    def AddStudent(self, student):
        self.students.append(student)
        if student.CurrCourse not in self.CourseMap:
            self.CourseMap[student.CurrCourse] = {}
        if student.CurrSec not in self.CourseMap[student.CurrCourse]:
            self.CourseMap[student.CurrCourse][student.CurrSec] = []
        self.CourseMap[student.CurrCourse][student.CurrSec].append(student)
    
    def Process(self, Data):
        # Sort
        SortedRoll = sorted(Data.keys(), reverse=True)
        
        for rollno in SortedRoll:
            for request in Data[rollno]:
                CurrCourse, CurrSec, DesiredSection, DesiredCourse = request
                student = Student(rollno, CurrCourse, CurrSec, DesiredSection, DesiredCourse)
                self.AddStudent(student)
        
        #older first
        self.students.sort(key=lambda x: x.rollno, reverse=True)
    
    def SectionSwaping(self):
        for student in self.students:
            if student.done:
                continue
            CourseName = student.CurrCourse.split('-')[0]
            DesiredCourseName = CourseName
            DesiredSection = student.DesiredSection
            
            for candidate in self.students:
                if candidate.done or candidate == student:
                    continue
                
                CandiCourseName = candidate.CurrCourse.split('-')[0]
                
                if (CourseName == CandiCourseName and
                    candidate.CurrSec == DesiredSection and
                    candidate.DesiredSection == student.CurrSec):
                    
                    self.SwapPair.append((student, candidate))
                    student.done = True
                    candidate.done = True
                    break
    
    def CourseSwaps(self):
        for student in self.students:
            if student.done:
                continue
                
            DesiredCourse = student.DesiredCourse
            if not DesiredCourse: 
                continue
                
            for candidate in self.students:
                if candidate.done or candidate == student:
                    continue
                
                if (candidate.DesiredCourse == student.CurrCourse and
                    candidate.DesiredSection == student.CurrSec and
                    candidate.CurrCourse == student.DesiredCourse and
                    candidate.CurrSec == student.DesiredSection):
                    
                    self.SwapPair.append((student, candidate))
                    student.done = True
                    candidate.done = True
                    break
    
    def Results(self):
        DoneCount =0
        NotDone = 0 
        results = []
        for pair in self.SwapPair:
            student1, student2 = pair
            swap_str = (f"{student1.rollno} swaped from {student1.CurrCourse} {student1.CurrSec} to "
                        f"{student1.DesiredCourse} {student1.DesiredSection} with {student2.rollno} who swaps from "
                        f"{student2.CurrCourse} {student2.CurrSec} to {student2.DesiredCourse} {student2.DesiredSection}")
            results.append(swap_str)
            DoneCount += 2
        
        undone = [f"{s.rollno} could not swap {s.CurrCourse} {s.CurrSec} -> {s.DesiredCourse} {s.DesiredSection}" 
                    for s in self.students if not s.done]
        results.extend(undone)
        NotDone = len(undone)

        total = len(self.students)
        results.append(f"Total Requests: {total}")
        results.append(f"Done Requests: {DoneCount}")
        results.append(f"Not Done Requests: {NotDone}")
        return results

# Main
Data = {}
ReadFile(Data)
FixData(Data)

AcademicOffice = Swapper()
AcademicOffice.Process(Data)

AcademicOffice.SectionSwaping()

AcademicOffice.CourseSwaps()

results = AcademicOffice.Results()

print("\nSwap Results:")
for result in results:
    print(result)
