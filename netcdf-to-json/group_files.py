

def group_json_files_by_days(files_list, dst_path):
    path = dst_path
    new_json_files = reduce(lambda x, y: x + [y] if not y in x else x,
                            map(lambda file_i: os.path.basename(os.path.dirname(file_i[:-2] + 'json')), files_list), [])

    new_json_files.sort()
    print(new_json_files)

    for json_file in new_json_files:
        with open(path + json_file + '.json', 'w') as outfile:
            outfile.write("{\n\t" + '"'"data"'"' + " : [\n")
            # Read all the data days
            files_by_day = filter(lambda json_d: '/'+json_file+'/' in json_d,
                                  map(lambda file_i: file_i[:-2] + 'json', files_list))

            files_by_day.sort()
            print(files_by_day)
            for file_by_day in files_by_day:
                print(file_by_day)
                with open(file_by_day, 'r') as infile:
                    for line in infile:
                        if line.startswith("\t\t{"):
                            outfile.write(line)
                outfile.seek(-2, os.SEEK_END)
                outfile.write("},\n")
                os.remove(file_by_day)

            print('------------')

            outfile.seek(-3, os.SEEK_END)
            outfile.truncate()

            outfile.write("}\n\t]\n}")