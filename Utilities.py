__author__ = 'Bhuvanesh3'
from enum import Enum

class Transformation(Enum):
    Empty = 0
    RepetitionByExpansion = 1 #aka scaling or expansion
    RepetitionByTranslation = 2
    RepetitionByCircularTranslation = 3
    TranslationOfOneObject = 4
    ScalingOfOneObject = 5
    ConstantAddition = 6
    Scaling = 10
    """
    ShapeChange = 0
    Translate = 1
    Scale = 2
    Rotate = 3
    Fill = 4
    Reflect = 5
    NoChange = 6
    Delete = 7
    """

class Blob:
    def __init__(self,i=0,r=0,c=0,w=0,h=0,f=0):
        self.id = i
        self.startRow = r
        self.startCol = c
        self.endRow = r + h
        self.endCol = c + w
        self.width = w
        self.height = h
        self.fill = f


class Attribute(Enum):
    inside = 1
    above = 2
    alignment = 3
    fill = 4
    angle = 5
    size = 6
    shape = 7

class Conversion:
    def __init__(self,type,initial,final):
        self.TransformationType = type
        self.InitialState = initial
        self.FinalState = final

    def getConvertedValue(self,sourceValue = "none"):
        if self.TransformationType == Transformation.Translate:
            destValue = sourceValue
            topBottom = "none"
            leftRight = "none"
            if "bottom" in self.InitialState and "top" in self.FinalState:
                topBottom = "switch"
            elif "top" in self.InitialState and "bottom" in self.FinalState:
                topBottom = "switch"
            if "left" in self.InitialState and "right" in self.FinalState:
                leftRight = "switch"
            elif "right" in self.InitialState and "left" in self.FinalState:
                leftRight = "switch"
            if topBottom == "switch":
                if "bottom" in sourceValue:
                    destValue = destValue.replace("bottom","top")
                elif "top" in sourceValue:
                    destValue = destValue.replace("top","bottom")
            if leftRight == "switch":
                if "left" in sourceValue:
                    destValue = destValue.replace("left","right")
                elif "right" in sourceValue:
                    destValue = destValue.replace("right","left")
            return destValue
        elif self.TransformationType == Transformation.Reflect:
            aQuad = self.getQuadrant(int(self.InitialState))
            bQuad = self.getQuadrant(int(self.FinalState))
            srcQuad = self.getQuadrant(int(sourceValue))
            destQuad = 4
            destValue = 0
            if aQuad != bQuad and bQuad != srcQuad and srcQuad!= aQuad:
                destQuad = 10 - (aQuad + bQuad + srcQuad) #10 is sum of all quadrant numbers
                if self.getQuadrant(int(sourceValue) + 90 ) == destQuad:
                    destValue = int(sourceValue) + 90
                elif self.getQuadrant(int(sourceValue) - 90) == destQuad:
                    destValue = int(sourceValue) - 90
                else:
                    destValue = int(sourceValue) + 180 #ideally never executes
            elif aQuad == srcQuad:
                destQuad = bQuad
                destValue = int(self.FinalState)
            elif bQuad == srcQuad:
                destQuad = aQuad
                destValue = int(self.InitialState)
            return str(destValue % 360)
        elif self.TransformationType == Transformation.Rotate:
            degreeOfRotation = int(self.FinalState) - int(self.InitialState)
            destValue = int(sourceValue) + degreeOfRotation
            return str(destValue % 360)
        return self.FinalState

    def getQuadrant(self,degree):
        degree = degree % 360
        quadrant = 1
        if degree >= 0 and degree < 90:
            quadrant = 4
        elif degree >= 90 and degree < 180:
            quadrant = 3
        elif degree >= 180 and degree < 270:
            quadrant = 2
        else:
            quadrant = 1
        return quadrant

    def toString(self):
        return self.TransformationType.name+":"+self.InitialState+":"+self.FinalState
