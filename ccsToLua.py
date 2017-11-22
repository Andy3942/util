#!/usr/bin/env python3
# coding=utf-8

import os
import math
import string
from xmltodict import parse
from xmltodict import unparse
import pprint

destRoot = "/Users/apple/Documents/workspace/sg/FknSango/CardSango/Resources/"
ccsRoot = "/Users/apple/Documents/workspace/sg/cocostudio/CocosProject/cocosstudio/"

#destDir = destRoot + "script/ui/athena/"
#destDir = "/Users/bzx/Documents/sango/FknSango/CardSango/Resources/script/ui/purgatorychallenge/"
#destDir = destRoot + "script/ui/moon/"
destDir = destRoot + "script/ui/formation/"
#destDir = "/Users/bzx/Documents/sango/FknSango/CardSango/Resources/script/ui/rechargeActive/worldGroupBuy/"
#file_path = ccsRoot + "MoonLayer.csd"
#file_path = "/Users/bzx/Documents/CocosProjects/CocosProject/cocosstudio/MoonShopLayer.csd"
#file_path = "/Users/bzx/Documents/CocosProjects/CocosProject/cocosstudio/MoonFightResultLayer.csd"
#file_path = "/Users/bzx/Documents/CocosProjects/CocosProject/cocosstudio/BatchComprehendLayer.csd"
#file_path = "/Users/bzx/Documents/CocosProjects/CocosProject/cocosstudio/MoonShopPreviewLayer.csd"
#file_path = ccsRoot + "AthenaPreviewLayer.csd"
#file_path = "/Users/bzx/Documents/CocosProjects/CocosProject/cocosstudio/PurgatoryRankLayer.csd"
#file_path = "/Users/bzx/Documents/CocosProjects/CocosProject/cocosstudio/PurgatoryRewardPreviewLayer.csd"
file_path = ccsRoot + "FormationLayer.csd"
#file_path = "/Users/bzx/Documents/CocosProjects/CocosProject/cocosstudio/WorldGroupBuyRecordLayer.csd"
#file_path = "/Users/bzx/Documents/CocosProjects/CocosProject/cocosstudio/WorldGroupPointRewardLayer.csd"

class TOLua(object):
    _file_path = ""
    _class_name = ""
    _class_file_path = ""
    _data = {}
    _text = ""
    _head = ""
    _create_function = ""
    _body = ""
    def __init__(self, file_path):
        self._file_path = file_path
        self._class_name = "ST" + os.path.splitext(os.path.basename(self._file_path))[0]
        self._class_file_path = "%s%s.lua"%(destDir, self._class_name)

    def toCode(self):
        data = self._data["GameFile"]["Content"]["Content"]["ObjectData"]
        className = "STLayer"
        self._text = "%s = class(\"%s\", function()\n\treturn %s:create()\nend)\n\n"%(self._class_name, self._class_name, className)
        self.nodeToCode(data, None)
        self._text += self._head + "\n"
        #self._text += self._create_function + "\n"
        self._text += self._body
        self._text += self.appendCode(0, "function %s:getMemberNodeByName(name)"%(self._class_name))
        self._text += self.appendCode(1, "return self[\"_\" .. name]")
        self._text += self.appendCode(0, "end")
        self._text = self._text.expandtabs(4)
    def nodeToCode(self, data, parent):
        name = data["Name"]
        indent = 0
        if parent is None:
            self._body += self.appendCode(indent, "function %s:create()"%(self._class_name))
            indent += 1
            self._body += self.appendCode(indent, "local ret = %s:new()"%(self._class_name))
        else:
            self._body += self.appendCode(indent, "function %s:create%s(isRootLayer)"%(self._class_name, name[0].upper() + name[1:]))
            indent += 1
            #self._create_function += self.appendCode(indent, "ret:load%s()"%(name.capitalize()))
            customClassName = data.get("CustomClassName", None)
            className = data["ctype"]
            if customClassName is None:
                if className == "SingleNodeObjectData":
                    self._body += self.appendCode(indent, "local ret = STNode:create()")
                elif className == "SpriteObjectData":
                    self._body += self.appendCode(indent, "local ret = STSprite:create(\"%s\")"%(data["FileData"]["Path"]))
                #STButton
                elif className == "ButtonObjectData":
                    normalImage = data["NormalFileData"]["Path"]
                    selectedImage = data["PressedFileData"]["Path"]
                    disabledImage = data["DisabledFileData"]["Path"]
                    Scale9Enable = data.get("Scale9Enable", "false")
                    if Scale9Enable == "True":
                        Scale9Enable = "true"
                    normalImage = "\"%s\""%(normalImage)
                    if selectedImage == "Default/Button_Press.png":
                        selectedImage = "nil"
                    else:
                        selectedImage = "\"%s\""%(selectedImage)

                    if disabledImage == "Default/Button_Disable.png":
                        disabledImage = "nil"
                    else:
                        disabledImage = "\"%s\""%(disabledImage)
                    self._body += self.appendCode(indent, "local ret = STButton:createWithImage(%s, %s, %s, %s)"%(normalImage, selectedImage, disabledImage, Scale9Enable))
                    if Scale9Enable == "true":
                        Scale9OriginX = float(data.get("Scale9OriginX", 0))
                        Scale9OriginY = float(data.get("Scale9OriginY", 0))
                        Scale9Width = float(data.get("Scale9Width"))
                        Scale9Height = float(data.get("Scale9Height"))
                        self._body += self.appendCode(indent, "ret:setCapInsets(CCRectMake(%s, %s, %s, %s))"%(Scale9OriginX, Scale9OriginY, Scale9Width, Scale9Height))
                    #ButtonText
                    ButtonText = data.get("ButtonText", None)
                    if ButtonText is not None:
                        FontSize = data["FontSize"]
                        TextColor = data["TextColor"]
                        a = float(TextColor.get("A", 0))
                        r = float(TextColor.get("R", 0))
                        g = float(TextColor.get("G", 0))
                        b = float(TextColor.get("B", 0))
                        FontName = "g_sFontName"
                        FontResource = data.get("FontResource", None)
                        if FontResource is not None:
                            FontNamePath = FontResource["Path"]
                            if FontNamePath == "py.ttf":
                                FontName = "g_sFontPangWa"
                        self._body += self.appendCode(indent, "ret:setLabel(\"%s\", %s, %s, ccc3(%s, %s, %s), 1, ccc3(0, 0, 0), type_stroke)"%(ButtonText, FontName, FontSize, r, g, b))
                elif className == "TextObjectData":
                    LabelText = data["LabelText"]
                    FontName = "g_sFontName"
                    FontResource = data.get("FontResource", None)
                    if FontResource is not None:
                        FontNamePath = FontResource["Path"]
                        if FontNamePath == "py.ttf":
                            FontName = "g_sFontPangWa"
                    FontSize = data["FontSize"]
                    #ShadowEnabled
                    ShadowEnabled = data.get("ShadowEnabled", None)
                    if ShadowEnabled is not None:
                        shadowColor = "ccc3(0, 0, 0)"
                        ShadowColor = data.get("ShadowColor", None)
                        if ShadowColor is not None:
                            shadowColor = "ccc3(%s, %s, %s)"%(ShadowColor["R"], ShadowColor["G"], ShadowColor["B"])
                        self._body += self.appendCode(indent, "local ret = STLabel:create(\"%s\", %s, %s, 1, %s, type_shadow)"%(LabelText, FontName, FontSize, shadowColor))
                    else:
                        self._body += self.appendCode(indent, "local ret = STLabel:create(\"%s\", %s, %s)"%(LabelText, FontName, FontSize))
                    Alpha = data.get("Alpha", None)
                    if Alpha is not None:
                        data["CColor"]["A"] = Alpha
                    data["Size"] = None
                    # todo
                elif className == "TextFieldObjectData":
                    self._body += self.appendCode(indent, "local ret = STSprite:create()")
                    # todo
                elif className == "LoadingBarObjectData":
                    self._body += self.appendCode(indent, "local ret = STSprite:create()")
                    # todo
                elif className == "ImageViewObjectData":
                    Scale9OriginX = float(data.get("Scale9OriginX", 0))
                    Scale9OriginY = float(data.get("Scale9OriginY", 0))
                    Scale9Width = float(data.get("Scale9Width"))
                    Scale9Height = float(data.get("Scale9Height"))
                    capInset = "CCRectMake(%s, %s, %s, %s)"%(Scale9OriginX, Scale9OriginY, Scale9Width, Scale9Height)
                    self._body += self.appendCode(indent, "local ret = STScale9Sprite:create(\"%s\", %s)"%(data["FileData"]["Path"], capInset))
                elif className == "CheckBoxObjectData":
                    self._body += self.appendCode(indent, "local ret = STSprite:create()")
                    # todo
                elif className == "PageViewObjectData":
                    self._body += self.appendCode(indent, "local ret = STSprite:create()")
                    # todo
                elif className == "PanelObjectData":
                    self._body += self.appendCode(indent, "local ret = STLayout:create()")
                    if data.get("Size", None) is None:
                        data["Size"] = {"X":0, "Y":0}
                    # todo 
                elif className == "ScrollViewObjectData" or className == "ListViewObjectData":
                    if className == "ScrollViewObjectData":
                        self._body += self.appendCode(indent, "local ret = STScrollView:create()")
                    elif className == "ListViewObjectData":
                        self._body += self.appendCode(indent, "local ret = STTableView:create()")
                        data.setdefault("DirectionType", "Horizontal")
                        data["ScrollDirectionType"] = data["DirectionType"]
                    #direction
                    ScrollDirectionType = data["ScrollDirectionType"]
                    if ScrollDirectionType == "Vertical":
                        self._body += self.appendCode(indent, "ret:setDirection(kCCScrollViewDirectionVertical)")
                    elif ScrollDirectionType == "Horizontal":
                        self._body += self.appendCode(indent, "ret:setDirection(kCCScrollViewDirectionHorizontal)")
                    #clipAble
                    ClipAble = data.get("ClipAble", "false")
                    if ClipAble == "false":
                        self._body += self.appendCode(indent, "ret:setClippingToBounds(false)")
                    IsBounceEnabled = data.get("IsBounceEnabled", "false")
                    if IsBounceEnabled == "false":
                        self._body += self.appendCode(indent, "ret:setBounceable(false)")
                    # todo
            #if customClassName == "":
            # #addChild
            # if parent == self._data["GameProjectFile"]["Content"]["Content"]["ObjectData"]["Name"]:
            #     self._body += self.appendCode(indent, "self:addNode(self._%s)"%(name))
            # else:
            #     self._body += self.appendCode(indent, "self._%s:addNode(self._%s)"%(parent, name))
            #name
            self._body += self.appendCode(indent, "ret:setName(\"%s\")"%(name))
            #contentSize
            if (className != "SpriteObjectData" and className != "ButtonObjectData") or (className == "ButtonObjectData" and Scale9Enable == "true"):
                content_size = data.get("Size", None)
                if content_size is not None:
                    width = float(content_size.get("X", 0))
                    height = float(content_size.get("Y", 0))
                    size = "CCSizeMake(%s, %s)"%(width, height)
                    self._body += self.appendCode(indent, "ret:setContentSize(%s)"%(size))
                    if className == "ListViewObjectData":
                        self._body += self.appendCode(indent, "ret:setInnerSize(%s)"%(size))
            #innerNodeSize
            if className == "ScrollViewObjectData":
                InnerNodeSize = data["InnerNodeSize"]
                width = InnerNodeSize.get("Width")
                height = InnerNodeSize.get("Height")
                self._body += self.appendCode(indent, "ret:setInnerSize(CCSizeMake(%s, %s))"%(width, height))
            #tag
            # tag = data.get("Tag", None)
            # if tag is not None:
            #     self._body += self.appendCode(indent, "ret:setTag(%s)"%(float(tag)))
            #position
            position = data.get("Position", None)
            if position is not None:
                position_x = float(position.get("X", 0))
                position_y = float(position.get("Y", 0))
                if position_x != 0 or position_y != 0:
                    self._body += self.appendCode(indent, "ret:setPosition(ccp(%s, %s))"%(position_x, position_y))
            #PercentPosition
            PositionPercentXEnabled = data.get("PositionPercentXEnabled", None)
            if PositionPercentXEnabled is not None:
                PercentPositionX = float(data["PrePosition"].get("X", 0))
                self._body += self.appendCode(indent, "ret:setPercentPositionXEnabled(true)")
                self._body += self.appendCode(indent, "ret:setPercentPositionX(%s)"%(PercentPositionX))
            PositionPercentYEnabled = data.get("PositionPercentYEnabled", None)
            if PositionPercentYEnabled is not None:
                PrePosition = data.get("PrePosition", None)
                if PrePosition:
                    PrePosition.setdefault("Y", 0)
                    PercentPositionY = float(data["PrePosition"].get("Y", 0))
                    self._body += self.appendCode(indent, "ret:setPercentPositionYEnabled(true)")
                    self._body += self.appendCode(indent, "ret:setPercentPositionY(%s)"%(PercentPositionY))
            #scale
            scale = data.get("Scale", None)
            if scale is not None:
                scale_x = float(scale.get("ScaleX", 1))
                scale_y = float(scale.get("ScaleY", 1))
                if scale_x != 1:
                    self._body += self.appendCode(indent, "ret:setScaleX(%s)"%(scale_x))
                if scale_y != 1:
                    self._body += self.appendCode(indent, "ret:setScaleY(%s)"%(scale_y))
            #anchorPoint
            anchor_point = data.get("AnchorPoint", None)
            if anchor_point is not None:
                anchor_point_x = float(anchor_point.get("ScaleX", 0))
                anchor_point_y = float(anchor_point.get("ScaleY", 0))
                self._body += self.appendCode(indent, "ret:setAnchorPoint(ccp(%s, %s))"%(anchor_point_x, anchor_point_y))
            #color
            color = data.get("CColor", None)
            if color is not None:
                a = float(color.get("A", 0))
                r = float(color.get("R", 0))
                g = float(color.get("G", 0))
                b = float(color.get("B", 0))
                if r != 255 or g != 255 or b != 255:
                    self._body += self.appendCode(indent, "ret:setColor(ccc3(%s, %s, %s))"%(r, g, b))
                if a != 255:
                    self._body += self.appendCode(indent, "ret:setOpacity(%s)"%(a))
            #bgColor
            bgColor = data.get("SingleColor", None)
            if bgColor is not None:
                r = float(bgColor.get("R", 0))
                g = float(bgColor.get("G", 0))
                b = float(bgColor.get("B", 0))
                a = float(data.get("BackColorAlpha", 255))
                if a != 0:
                    self._body += self.appendCode(indent, "ret:setBgColor(ccc3(%s, %s, %s))"%(r, g, b))
                    if a != 255:
                        self._body += self.appendCode(indent, "ret:setBgOpacity(%s)"%(a))
            TouchEnable = data.get("TouchEnable", None)
            if TouchEnable is not None:
                if className != "ButtonObjectData":
                    self._body += self.appendCode(indent, "ret:setTouchEnabled(true)")
        #loadChildren
        children = data.get("Children", None)
        if children is not None:
            nodesData = children["AbstractNodeData"]
            if isinstance(nodesData, dict):
                nodesData = [nodesData]
            for nodeData in nodesData:
                nodeName = nodeData["Name"]
                VisibleForFrame = nodeData.get("VisibleForFrame", None)
                if VisibleForFrame is not None:
                    continue
                if parent is None:
                    self._body += self.appendCode(indent, "local %s = ret:create%s(true)"%(nodeName, nodeName[0].upper() + nodeName[1:]))
                else:
                    self._body += self.appendCode(indent, "local %s = self:create%s(isRootLayer)"%(nodeName, nodeName[0].upper() + nodeName[1:]))
                self._body += self.appendCode(indent, "ret:addChild(%s)"%(nodeName))
        #成员变量
        if parent is not None:
            self._body += self.appendCode(indent, "if isRootLayer then")
            indent += 1
            self._body += self.appendCode(indent, "self._%s = ret"%(name))
            indent -= 1
            self._body += self.appendCode(indent, "end")
        else:
            self._body += self.appendCode(indent, "ret._layer = ret")
        #return 
        self._body += self.appendCode(indent, "return ret")
        #end
        indent -= 1
        self._body += self.appendCode(indent, "end\n")

        children = data.get("Children", None)
        if children is not None:
            nodeData = children["AbstractNodeData"]
            if isinstance(nodeData, dict):
                self.nodeToCode(nodeData, name)
            else:
                for child in nodeData:
                    self.nodeToCode(child, name)
        if parent is None:
            self._create_function += self.appendCode(1, "return ret")
            self._create_function += self.appendCode(0, "end")
    def appendCode(self, indent, statement):
        return "%s%s\n"%(self.getIndentStr(indent), statement)

    def writeToLua(self):
        print(self._class_name)
        print(self._class_file_path)
        print(self._file_path)
        fp = open(self._class_file_path, "w")
        fp.write(self._text)
        fp.close()
    
    def parseXml(self):
        fp = open(self._file_path, 'r')
        self._data = parse(fp.read())
        fp.close()

    def getIndentStr(self, indent):
        return " " * 4 * indent

print("\n\n\n\n\n\n\n\n\n")
toLua = TOLua(file_path)
toLua.parseXml()
toLua.toCode()
toLua.writeToLua()