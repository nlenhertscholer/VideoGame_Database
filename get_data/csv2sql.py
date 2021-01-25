import glob

PLATFORM_CATEGORY = ['console', 'arcade', 'platform',
                     'operating_system', 'portable_console', 'computer']

DATE_CATEGORY = ['YYYYMMMMDD', 'YYYYMMMM', 'YYYY', 'YYYYQ1',
                 'YYYYQ2', 'YYYYQ3', 'YYYYQ4', 'TBD']

DELIM = ';'


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def add_quote(mystring):
    idx = mystring.find("'")
    if idx == -1:
        return mystring
    else:
        mystring = mystring.split("'")
        new_str = mystring[0]
        for substr in mystring[1:]:
            new_str += "''" + substr
        return new_str


populate_db_file = "populate_db.sql"

# Do engine, game, company, platform first
csv_files = glob.glob("*.csv")
non_foreign_tables = ['engine', 'game', 'company', 'platform']

for i, table_name in enumerate(non_foreign_tables):
    file = next((file for file in csv_files if file == non_foreign_tables[i]+'.csv'), False)
    if file:
        non_foreign_tables[i] = file
        csv_files.remove(file)

open(populate_db_file, 'w')     # Clear the file
use_enum = False
for csv_file in non_foreign_tables:
    with open(populate_db_file, 'a') as db_file, open(csv_file, 'r') as file:
        if csv_file == 'platform.csv':
            use_enum = True

        db_file.write(f"INSERT INTO {csv_file[:len(csv_file)-4]} VALUES\n")
        rows = file.readlines()
        num_rows = len(rows)
        for i in range(num_rows):
            rows[i] = rows[i].split(DELIM)

        num_elements = len(rows[0])
        for row in rows[1:]:        # Skip the csv header info
            if is_int(row[0]):
                data = f"({int(row[0])}"
            elif is_float(row[0]):
                data = f"({float(row[0])}"
            else:
                data_str = add_quote(row[0])
                data = f"('{data_str}'"

            for i in range(1, num_elements):
                if is_int(row[i]):
                    if use_enum and i == 3:
                        data += f", '{PLATFORM_CATEGORY[int(row[i])-1]}'"
                    else:
                        data += f", {int(row[i])}"
                elif is_float(row[i]):
                    data += f", {float(row[i])}"
                else:
                    if row[i] != '' and row[i] != '\n':
                        data_str = add_quote(row[i])
                        if row[i][-1] == '\n':
                            data += f", '{data_str[0:-1]}'"
                        else:
                            data += f", '{data_str}'"
                    else:
                        data += f", NULL"
            if row == rows[-1]:
                data += f");\n\n"
            else:
                data += f"),\n"
            db_file.write(data)
        use_enum = False


use_enum = False
for csv_file in csv_files:
    with open(populate_db_file, 'a') as db_file, open(csv_file, 'r') as file:
        if csv_file == 'release_dates.csv':
            use_enum = True

        db_file.write(f"INSERT INTO {csv_file[:len(csv_file)-4]} VALUES\n")
        rows = file.readlines()
        num_rows = len(rows)
        for i in range(num_rows):
            rows[i] = rows[i].split(DELIM)

        num_elements = len(rows[0])
        for row in rows[1:]:        # Skip the csv header info
            if is_int(row[0]):
                data = f"({int(row[0])}"
            elif is_float(row[0]):
                data = f"({float(row[0])}"
            else:
                data_str = add_quote(row[0])
                data = f"('{data_str}'"

            for i in range(1, num_elements):
                if is_int(row[i]):
                    if use_enum and i == 3:
                        data += f", '{DATE_CATEGORY[int(row[i])-1]}'"
                    else:
                        data += f", {int(row[i])}"
                elif is_float(row[i]):
                    data += f", {float(row[i])}"
                else:
                    if row[i] != '' and row[i] != '\n':
                        data_str = add_quote(row[i])
                        if row[i][-1] == '\n':
                            data += f", '{data_str[0:-1]}'"
                        else:
                            data += f", '{data_str}'"
                    else:
                        data += f", NULL"
            if row == rows[-1]:
                data += f");\n\n"
            else:
                data += f"),\n"
            db_file.write(data)
        use_enum = False



