module("DBCommon", package.seeall)

function addDBFunction(db)
	db.mt = {}
	db.mt.__index = function (t,key)
		local index = db.keys[key]
		local value = rawget(t, index)
		rawset(t, key, value)
		return value
	end

	db.datas = {}
	db.getDataById = function(id)
		id = tonumber(id)
		local data = db.datas[id]
		if data == nil then
			if db.fp == nil then
				local path = CCFileUtils:sharedFileUtils():fullPathForFilename(db.data_path)
				db.fp = io.open(path)
			end
			local id_data = db.id_datas[id]
			if id_data == nil then
				return
			end
			db.fp:seek("set", id_data)
			local data_line = db.fp:read()
			local statement = string.format("return %s", string.sub(data_line, 1, -2))
			data = loadstring(statement)()
			db.datas[id] = data
		end
		if getmetatable(data) == nil then
			setmetatable(data, db.mt)
		end
		return data
	end

	db.getArrDataByField = function(fieldName, fieldValue)
		local arrData = {}
		local fieldNo = db.keys[fieldName]
		local datas = getDatas()
		for k, v in pairs(datas) do
			if v[fieldNo] == fieldValue then
				setmetatable (v, mt)
				arrData[#arrData+1] = v
			end
		end
		return arrData
	end

	db.getDatas = function()
		db.datas = require(db.data_path)
		return db.datas
	end

	db.getDataCount = function()
		return db.data_count
	end
end
