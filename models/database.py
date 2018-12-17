#!/usr/bin/python

import mysql.connector

# create a database


class database(object):
    def __init__(self, database,tablename,user_table="user"):
        self.database = database
        self.table = tablename
        self.sql_do('create table if not exists ' + self.table +
                    ' (id int primary key auto_increment unique,task TEXT, due_by date,status integer)')
        self.query = "select * from {0} where {1} {2}"
        self.due_date = 0
        self.overdue = 1
        self.finished = 2

    def api(self,api_id,date=None):
        if api_id == self.due_date:
            return self.retrieve(self.query.format(self.table," due_by =  ",'"{}"'.format(date)))
        elif api_id == self.overdue:
            return self.retrieve(self.query.format(self.table,"due_by > "," CURDATE() and status <> 2"))
        elif api_id == self.finished:
            return self.retrieve(self.query.format(self.table,"status = ",self.finished))
        else:
            return False


    def sql_do(self, sql, *params):
        self._db.execute(sql, params)
        self._conn.commit()

    def retrieve(self, query):
        """
            returns result for select queries
        """
        print(query)
        self._db.execute(query)
        return self._db.fetchall()

    def delete(self, key):
        self._db.execute('delete from {} where id = ?'.format(self.table), (key,))
        self._db.commit()

    def __iter__(self):
        self._db.execute('select * from {} '.format(self.table))
        for row in self._db.fetchall():
            yield list(row)

    def insert(self, row):
        print('insert into {} (task,due_by, status) values ("{}", "{}", {})'
                         .format(self.table,row['task'], row['due_by'], row['status']))
        self._db.execute('insert into {} (task,due_by, status) values ("{}", "{}", {})'
                         .format(self.table,row['task'], row['due_by'], row['status']))
        self._conn.commit()

    def update(self,row):
        print('UPDATE {} SET "task" = "{}" , "due_by" = "{}" , "status" = {} where id = {};'
                         .format(self.table,row["task"],row["due_by"],row["status"],row["id"]))
        self._db.execute('UPDATE {} SET task = "{}" , due_by = "{}" , status = {} where id = {};'
                         .format(self.table,row["task"],row["due_by"],row["status"],row["id"]))
        self._conn.commit()

    @property
    def database(self):
        return self.database

    @database.setter
    def database(self, db):
        """
            initialise database
        """
        self._database = db
        self._conn = mysql.connector.connect(database=db, user="root", password="admin", host="localhost",
                                             auth_plugin='mysql_native_password')

        self._db = self._conn.cursor()
        print('-' * 3 + " connected to database - < " + db + ' >  ' + '-' * 3)

    @database.deleter
    def database(self):
        self.close()

    def close(self):
        self._db.close()


if __name__ == '__main__':
    db = database(database='todo',tablename ="todo")
    # row = { "task":'task 1',"due_by":'2018-08-02',"status":db.overdue}
    # db.insert(row)
    # row["task"] = "task 2 "
    # db.insert(row)
    for i in db:
        print(list(i))
    print(db.api(db.due_date,"2018-12-12"))
    # print(db.retrieve())
    # print(db.get_intent_1('2018-07-06'))
    # print(db.get_intent_1('2018-07-06 00:00:00'))
    # print(db.get_intent_2("today", "nestle"))
    # print(db.get_intent_2("month", "sugar 1kg", is_articleName=True))
    #
    # for row in db.get_intent_3("articles", "2018-07-06"):
    #     print(*row)
    # for row in db.get_intent_3("subcategory", "today"):
    #     print(*row)
    # print(db.get_intent_2("week", "rin"))
    # print(db.get_intent_2_1('masalas & spices', 'category', 'week'))
