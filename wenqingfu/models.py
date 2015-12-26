#coding=utf-8

class Major:
    def __init__(self,majorId,majorName):
        self.majorId = majorId
        self.majorName = majorName
        self.comments = []

class Comment:

    def __init__(self,commentId,comprehensiveScore,teachingScore,dealScore,workScore):
        self.commentId = commentId
        self.comprehensiveScore = comprehensiveScore
        self.teachingScore = teachingScore
        self.dealScore = dealScore
        self.workScore = workScore

class School:
    def __init__(self,Id,schoolName):
        self.majors = []
        self.score = 0
        self.schoolId = Id
        self.schoolName= schoolName