#coding=utf-8

class Major:
    def __init__(self,majorId,majorName):
        self.majorId = majorId
        self.majorName = majorName
        self.comments = []
        self.salary = 0;
        self.ISTJ=0;
        self.INFJ=0;
        self.ISTP=0;
        self.INFP=0;
        self.ESTJ=0;
        self.ENFJ=0;
        self.ESTP=0;
        self.ENFP=0;
        self.ISFJ=0;
        self.INTJ=0;
        self.ISFP=0;
        self.INTP=0;
        self.ESFJ=0;
        self.ENTJ=0;
        self.ESFP=0;
        self.ENTP=0;

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