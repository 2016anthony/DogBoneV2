# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 09:46:30 2015

@author: lvanhulle
"""
import Point as p
import Line as l

from parameters import constants as c
class LineGroup(object):
    
    def __init__(self, inGroup):
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None        
        if(inGroup != None):
            if(type(inGroup) is list):
                self.lines = inGroup
            else:
                self.lines = [inGroup]
            for line in self.lines:
                self.updateMinMax(line)
        else:
            self.lines = []
            
    def addLine(self, line):
        self.lines.append(line)
        self.updateMinMax(line)
        
    def updateMinMax(self, line):
        if(line.upperLeft.getX() < self.minX or self.minX is None): self.minX = line.upperLeft.getX()
        if(line.upperLeft.getY() > self.maxY or self.maxY is None): self.maxY = line.upperLeft.getY()
        if(line.lowerRight.getX() > self.maxX or self.maxX is None): self.maxX = line.lowerRight.getX()
        if(line.lowerRight.getY() < self.minY or self.minY is None): self.minY = line.lowerRight.getY()

    def addLineGroup(self, inGroup):
        for line in inGroup.lines:
            self.addLine(line)
            
    def addLinesFromCoordinateList(self, coordList):
        pointList = []        
        for coord in coordList:
            pointList.append(p.Point(coord[c.X], coord[c.Y]))
        self.addLinesFromPoints(pointList)
    
    def addLinesFromPoints(self, pointList):
        for i in range(len(pointList)-1):
            self.addLine(l.Line(pointList[i], pointList[i+1]))
            
    def mirror(self, axis):
        tempLines = [line.mirror(axis) for line in self.lines]
        tempLines.reverse()
        tempLines2 = []
        for line in tempLines:
            tempLines2.append(l.Line(line.end, line.start))
        return LineGroup(tempLines2)
    
    def translate(self, xShift, yShift,zShift=0):
        return LineGroup([line.translate(xShift, yShift, zShift) for line in self.lines])        
        
    def rotate(self, angle, point):
        if(point is None): point = p.Point(0,0)        
        return LineGroup([line.rotate(angle, point) for line in self.lines])
        
    def getLines(self):
        outList = []
        for line in self.lines:
            outList.append(l.Line(line.getStart(), line.getEnd()))
        return outList
        
    def getMidPoint(self):
        x = (self.maxX - self.minX)/2.0 + self.minX
        y = (self.maxY - self.minY)/2.0 + self.minY
        return p.Point(x, y)
    
    def __str__(self):
        tempString = ''     
        for line in self.lines:
            tempString = tempString + str(line) + '\n'
        return tempString