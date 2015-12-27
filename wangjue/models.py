#coding=utf-8

class Major:
    def __init__(self,majorId,majorName):
        self.majorId = majorId
        self.majorName = majorName
        self.comments = []
        self.salary = 0;

class Comment:
    def __init__(self,majorId,comprehensiveScore,teachingScore,dealScore,workScore):
        self.majorId = majorId
        self.comprehensiveScore = comprehensiveScore
        self.teachingScore = teachingScore
        self.dealScore = dealScore
        self.workScore = workScore

class School:
    def __init__(self,Id,schoolName):
        self.majors = []
        self.score = 0.0
        self.schoolId = Id
        self.schoolAvgCommentScore = 0
        self.schoolAvgSalary = 0
        self.schoolName= schoolName