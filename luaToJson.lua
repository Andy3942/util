
function idIsFirstField( data )
	for k, v in pairs(data) do
		if tonumber(v[1]) == nil then
			return false
		end
	end
	return true
end


function getArrayDatas( ... )
	local array_datas = {}
	local datas = _G[datas_key]
	if idIsFirstField(datas) then
		for k, v in pairs(datas) do
			table.insert(array_datas, v)
		end
		local comparator = function ( data1, data2 )
			return data1[1] < data2[1]
		end
		table.sort(array_datas, comparator)
	else
		local data = nil
		local i = 1
		repeat
			data = datas["id_" .. i]
			if data ~= nil then
				table.insert(array_datas, data)
			end
			i = i + 1
		until data == nil
	end
	return array_datas
end

function string.split(str, delimiter)
	if str==nil or delimiter==nil then
		return nil
	end
	if str == '' then
		return ''
	end
	
    local result = {}
    for match in (str..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match)
    end
    return result
end


function parseNumberString(src_str, dest_str, split_chars, split_index)
	if split_index > #split_chars then
		return tostring(tonumber(src_str)) .. ","
	end
	local split_char = split_chars[split_index]
	local split_datas = string.split(src_str, split_char)
	if split_datas[#split_datas] == "" then
		table.remove(split_datas, #split_datas)
	end
	if #split_datas > 1 then
		dest_str = dest_str .. '['
		for i = 1, #split_datas do
			local split_data = split_datas[i]
			dest_str = dest_str .. parseNumberString(split_data, "", split_chars, split_index + 1)
		end
		dest_str = string.sub(dest_str, 1, #dest_str - 1)
		dest_str = dest_str .. '],'
	elseif #split_datas == 1 then
		dest_str = dest_str .. parseNumberString(split_datas[1], "", split_chars, split_index + 1)
	end
	return dest_str
end

function isNumber( str )
	local start_index, end_index = string.find(str, "[0-9]*")
	local match_value = string.sub(str, start_index, end_index)
	return match_value == str
end

local args = load("return " .. ...)()
package.path = package.path .. ";?.lua"

function parseNormal( ... )
	local module_name = string.sub(args.file_name, 1, string.find(args.file_name, '.lua') - 1)
	datas_key = string.sub(module_name, 4)
	module = function ( ... )
	end
	
	require(args.dir .. module_name)

	local save_file_path = args.dest_folder .. string.lower(datas_key) .. ".json"
	local fp = io.open(save_file_path, 'w')
	fp:write("{\n")

	-- keys
	local keys_str = "\"keys\":["
	for i = 1, #keys do
		keys_str = keys_str .. string.format("\"%s\",", keys[i])
	end
	keys_str = string.sub(keys_str, 1, #keys_str - 1) .. "],"
	fp:write(keys_str)

	-- datas
	local datas_str = "\n\"datas\":{\n"
	local array_datas = getArrayDatas()

	for i = 1, #array_datas do
		local id = nil
		local data = array_datas[i]
		if idIsFirstField(_G[datas_key]) then
			id = array_datas[i][1]
		else
			id = i
		end
		datas_str = datas_str .. string.format("\"%d\":[", id)
		for j = 1, #keys do
			local value = data[j]
			local new_value = value
			if value == nil then
				new_value = "null"
			else
				local value_type = type(value)
				if value_type == "string" then
					value = string.gsub(value, "\n", "\\n")
					value = string.gsub(value, "\t", "\\t")
					local start_index, end_index = string.find(value, "[0-9|,-]*")
					match_value = string.sub(value, start_index, end_index)
					if match_value == value then
						local split_chars = {',', '|'}
						dest_str = parseNumberString(value, "", split_chars, 1)
						dest_str = string.sub(dest_str, 1, #dest_str - 1)
						new_value = dest_str
					else
						local dest_str = ""
						local split_datas = string.split(value, '|')
						if split_datas[#split_datas] == "" then
							table.remove(split_datas, #split_datas)
						end
						if #split_datas > 1 then
							dest_str = dest_str .. "["
							for i = 1, #split_datas do
								local split_data = split_datas[i]
								local is_number = isNumber(split_data)
								if is_number then
									dest_str = dest_str .. string.format("%s,", split_data)
								else
									dest_str = dest_str .. string.format("\"%s\",", split_data)
								end
							end
							dest_str = string.sub(dest_str, 1, #dest_str - 1) .. "]"
							new_value = dest_str
						else
							new_value = string.format("\"%s\"", value)
						end
					end
				end
			end
			datas_str = datas_str .. new_value .. ","
		end
		datas_str = string.sub(datas_str, 1, #datas_str - 1) .. "],\n"
	end
	datas_str = string.sub(datas_str, 1, #datas_str - 2)
	fp:write(datas_str)
	fp:write("\n}}")
	fp:close()
end

function parseCxml( ... )
	require(args.dir .. args.file_name:sub(1, #args.file_name - 4))
	local json_file_path = args.dest_folder .. args.file_name:sub(1, #args.file_name-3) .. "json"
	fp = io.open(json_file_path, "w")
	fp:write(string.format("{\"%s\":", args.key))
	local data = _G[args.key]
	if args.key ~= "talk" then
		data.models = data.models.normal
		for i = 1, #data.models do
			local v = data.models[i]
			v.modelURL = v.looks.look.modelURL
			v.armyID = v.looks.look.armyID
			v.looks = nil
		end
	end

	local str = tableToJsonStr(data)
	fp:write(str)
	fp:write("}")
	fp:close()
end

function tableToJsonStr(data)
	local json_str = ""
	if isArray(data) then
		json_str = json_str .. "[\n"
	else
		json_str = json_str .. "{\n"
	end

	if isArray(data) then
		for i = 1, #data do
			local value = data[i]
			local new_value = value
			if new_value == "" then
				new_value = "\"\""
			end
			if type(value) == "table" then
				new_value = tableToJsonStr(value)
			else
				if not isNumber(value) then
					new_value = string.format("\"%s\"", value)
				end
			end
			json_str = json_str .. new_value .. ",\n"
		end
	else
		for k, v in pairs(data) do
			local value = v
			local new_value = value
			if new_value == "" then
				new_value = "\"\""
			end
			if type(value) == "table" then
				new_value = tableToJsonStr(value)
			else
				if not isNumber(value) then
					new_value = string.format("\"%s\"", value)
				end
			end
			json_str = json_str .. string.format("\"%s\":%s,", k, new_value) .. "\n"
		end
	end
	json_str = json_str:sub(1, #json_str - 2) .. "\n"
	if isArray(data) then
		json_str = json_str .. ']'
	else
		json_str = json_str .. '}'
	end
	return json_str
end

function isArray(data)
	return data[1] 
end

print(args.dir .. args.file_name)

if args.is_cxml then
	parseCxml()
else
	parseNormal()
end