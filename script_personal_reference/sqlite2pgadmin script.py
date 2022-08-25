# connect to postgress database
from unittest import skip
import main
import sqlite3
import pandas
import pathlib
parent_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
cn_string = str(parent_dir)+"\mango_app\db\pages08222022.db"
print(cn_string)
cnx = sqlite3.connect(cn_string)
cur = cnx.cursor()
res = cur.execute("SELECT * FROM hostname_table")
print(res.fetchall)


with main.engine.connect() as connection:
    #main.Base.metadata.drop_all(main.engine)
    main.Base.metadata.create_all(main.engine)
    for i,row in enumerate(res):
        #hostname_to_update=main.session.query(main.HostnameClass).filter(main.HostnameClass.username == 'jona').first()
        try:
            main.session.add(main.HostnameClass(name=row[0],hostname = row[1],city_name=row[8],state=row[9],country=row[10]))
            print(f"{hostname_to_update} added")
        except: 
            print(f"skipped { i }")
            continue
        if i%10000==0:
            main.session.commit()
            print(f"{i} committed" )
    cnx.close()
    