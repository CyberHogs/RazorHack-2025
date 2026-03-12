import sqlite3

con = sqlite3.connect('i_ran_out_of_names_database.db')
cur = con.cursor()

# Get license_key for RazorPower
res = cur.execute("SELECT license_key FROM customer where company_name = 'RazorPower'")
print('\n'.join(row[0] for row in cur.fetchall()))
