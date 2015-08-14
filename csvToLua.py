#!/usr/bin/env python3
# coding=utf-8

import codecs
import re
import csv
import os

to_folder = "/Users/bzx/Documents/sango/"
cfg_folder = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出XML表/"
csv_folder = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出CSV表/"

def findCsv(path):
    if os.path.isdir(path):
            for sub_dir in os.listdir(path):
                findCsv(path)
    elif path.endswith(".csv"):
        parse()
    pass
def parse(filename):
    lua_path = "%sDB_%s.lua"%(to_folder, filename)
    db_path = "%s%s_db.lua"%(to_folder, filename)
    cfg_path = "%s%s.cfg"%(cfg_folder, filename)
    csv_path = "%s%s.csv"%(csv_folder, filename)
    #cfg
    cfg_data = {}
    cfg_fp = open(cfg_path)
    cfg_lines = cfg_fp.readlines()
    for line in cfg_lines:
        pattern = re.compile(r"[a-zA-Z0-9_=]*")
        line = pattern.search(line).group(0)
        if line != "":
            line_data = line.split("=")
            cfg_data[line_data[0]] = line_data[1]
        pass
    #keys
    lua_fp = open(lua_path, 'w')
    lua_fp.write("module(\"DB_Stronghold2\", package.seeall)\n")
    lua_fp.write("local db_path = \"%s\"\n"%(db_path))
    lua_fp.write("local keys={")

    db_fp = open(db_path, 'w')
    db_fp.write("local data = {\n")
    csv_reader = csv.reader(codecs.open(csv_path, 'r', "gbk"))
    keys = {}
    key_max_num = None
    fp_position = 0
    for line_fields in csv_reader:
        if csv_reader.line_num == 1:
            continue
        elif csv_reader.line_num == 2:
            key_max_num = len(line_fields) - 1
            for i in range(0, key_max_num):
                field = line_fields[i]
                if cfg_data.get(field) != None:
                    keys[i] = field
            key_index = 0
            for i in range(0, key_max_num):
                key = keys.get(i)
                if key != None:
                    key_index = key_index + 1
                    lua_fp.write("[\"%s\"]=%s,"%(key, key_index))
                pass
            lua_fp.write("}\n")
            lua_fp.write("local id_datas = {\n")
        else:
            data_id = None
            fp_position = db_fp.tell()
            db_fp.write("{")
            for i in range(0, len(line_fields) - 1):
                field = line_fields[i]
                field_type = cfg_data.get(keys.get(i))
                if field_type != None:
                    if field == "":
                        db_fp.write("nil")
                    else:
                        if field_type == "number":
                            db_fp.write(field)
                            if data_id == None:
                                data_id = field
                        elif field_type == "string":
                            db_fp.write("\"" + field + "\"")
                    db_fp.write(",")
            db_fp.write("},\n")
            lua_fp.write("[%s]=%s,\n"%(data_id, fp_position))
    db_fp.write("}\n")
    db_fp.write("return data")
    lua_fp.write("}\n")
    lua_fp.write("""
    local mt = {}
    mt.__index = function (t,key)
        local value = t[keys[key]]
        t[key] = value
        return value
    end
    local fp = nil
    local datas = {}
    local count = nil
    function getDataById(id)
        local data = datas[id]
        if data == nil then
            if fp == nil then
                fp = io.open(db_path)
            end
            local id_data = id_datas[id]
            fp:seek("set", id_data)
            local data_line = fp:read()
            local statement = string.format("return %s", string.sub(data_line, 1, -2))
            data = loadstring(statement)()
            datas[id] = data
        end
        setmetatable(data, mt)
        return data
    end
    function getArrDataByField(fieldName, fieldValue)
        local arrData = {}
        local fieldNo = 1
        for i=1, #keys do
            if keys[i] == fieldName then
                fieldNo = i
                break
            end
        end
        for k, v in pairs(Stronghold2) do
            if v[fieldNo] == fieldValue then
                setmetatable (v, mt)
                arrData[#arrData+1] = v
            end
        end
        return arrData
    end
    function getDatas()
        datas = require(db_path)
        return datas
    end
    function getDataCount()
        count = count or table.count(id_datas)
    end
    """)
    lua_fp.close()
    db_fp.close()