
# ---------------------------
# read and return global_attributes
# ---------------------------
def read_global_attr(nc_file):
    attr_list = []
    global_attr = []
    # print 'Global attributes:'
    for attr_name in nc_file.ncattrs():
        # print attr_name, '=', getattr(nc_file, attr_name)
        attr_list.append(attr_name)
        atts = getattr(nc_file, attr_name)
        global_attr.append(atts)
    return attr_list, global_attr


# --------------------------------------------------
# read and return variables and their attributes
# --------------------------------------------------
def read_vars(nc_file):
    var_attr_list = []
    var_data_list = []
    # print 'Variables:'
    # dictionary of variables:values
    vars = nc_file.variables.keys()
    for var_name in vars:
        attr = nc_file.variables[var_name]
        var_data = nc_file.variables[var_name][:]
        var_attr_list.append(attr)
        var_data_list.append(var_data)
    #      print var_name, ':', attr
    # if var_name=="lon":
    # print var_name, ' data sample[0:10]:', var_data[0]
    return vars, var_attr_list, var_data_list