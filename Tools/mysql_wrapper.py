#!/usr/bin/python3
# -*- coding: utf-8 -*-

import MySQLdb
import pandas
# from collections import namedtuple
# from itertools import repeat


class SimpleMysql:
    conn = None
    cur = None
    conf = None

    def __init__(self, db_name=None, autocommit=False):
        self.conf = {
            'db'        : db_name   or 'qvalues',
            'user'      : 'root',
            'passwd'    : 'Ahl9bael',
            'host'      : '172.17.0.2',
            'port'      : 3306,
            'charset'   : 'utf8',
            'autocommit': autocommit
        }
        self.connect()

    def connect(self):
        """Connect to the mysql server"""

        try:
            self.conn = MySQLdb.connect(db=self.conf['db'], host=self.conf['host'],
                                        port=self.conf['port'], user=self.conf['user'],
                                        passwd=self.conf['passwd'], charset=self.conf['charset'])
            self.cur = self.conn.cursor()
            self.conn.autocommit(self.conf["autocommit"])
        except:
            print("MySQL connection failed")
            raise

    def select(self, table, fields='*', where : list=None, order=None, limit=None):
        """Get all results
            table = (str) table_name
            fields = (field1, field2 ...) list of fields to select
            where = ("parameterizedstatement", [parameters])
                    eg: ("id=%s and name=%s", [1, "test"])
            order = [field, ASC|DESC]
            limit = [limit1, limit2]
        """
        if isinstance(fields, str):
            fields = [fields]
        query = self._format_select(table, fields, where, order, limit)
        print(query)
        return pandas.read_sql(query, self.conn)

    def select_or_create(self, table, fields='*', where : list=None, order=None, limit=None, data_insert : dict=None):
        df_result = self.select(table, fields, where, order, limit)
        if df_result.shape[0] > 0:
            return df_result
        self.insert(table, data_insert)
        return self.select(table, fields, where, order, limit)

    def lastId(self):
        """Get the last insert id"""
        return self.cur.lastrowid

    def last_query(self):
        """Get the last executed query"""
        try:
            return self.cur.statement
        except AttributeError:
            return self.cur._last_executed

    # def leftJoin(self, tables=(), fields=(), join_fields=(), where=None, order=None, limit=None):
    #     """Run an inner left join query
    #
    #         tables = (table1, table2)
    #         fields = ([fields from table1], [fields from table 2])  # fields to select
    #         join_fields = (field1, field2)  # fields to join. field1 belongs to table1 and field2 belongs to table 2
    #         where = ("parameterizedstatement", [parameters])
    #                 eg: ("id=%s and name=%s", [1, "test"])
    #         order = [field, ASC|DESC]
    #         limit = [limit1, limit2]
    #     """
    #
    #     cur = self._select_join(tables, fields, join_fields, where, order, limit)
    #     result = cur.fetchall()
    #
    #     rows = None
    #     if result:
    #         Row = namedtuple("Row", [f[0] for f in cur.description])
    #         rows = [Row(*r) for r in result]
    #
    #     return rows

    def insert(self, table : str, data : dict):
        """Insert a record"""
        if len(data) == 0:
            return 0

        keys, values = self._serialize_insert(data)
        sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, keys, values)
        return self.query(sql, data.values()).rowcount

    def insert_ignore(self, table : str, data : dict):
        """Insert a record"""
        if len(data) == 0:
            return 0

        keys, values = self._serialize_insert(data)
        sql = "INSERT IGNORE INTO %s (%s) VALUES (%s);" % (table, keys, values)
        return self.query(sql, data.values()).rowcount

    # def insertBatch(self, table, data):
    #     """Insert multiple record"""
    #
    #     query = self._serialize_batch_insert(data)
    #     sql = "INSERT INTO %s (%s) VALUES %s" % (table, query[0], query[1])
    #     flattened_values = [v for sublist in data for k, v in sublist.iteritems()]
    #     return self.query(sql, flattened_values).rowcount

    def update(self, table : str, data : dict, where : list=None):
        """Insert a record"""
        if len(data) == 0:
            return 0

        query = self._serialize_update(data)
        sql = "UPDATE %s SET %s" % (table, query)

        if where and len(where) > 0:
            sql += " WHERE " + " and ".join(where)

        return self.query(sql + ';', data.values()).rowcount

    def insert_update(self, table : str, data : dict, keys : list):
        """
        INSERT INTO table (a, b, c) VALUES (1, 2, 3)
        ON DUPLICATE KEY UPDATE c = 3;
        :param table: table name
        :param data:  {'a' : 1, 'b' : 2, 'c' : 3}
        :param keys:  ['a', 'b']
        """
        if len(data) == len(keys):
            return self.insert_ignore(table, data)
        insert_data = data.copy()
        data = {k: data[k] for k in data if k not in keys}

        insert_k, insert_v = self._serialize_insert(insert_data)    # ('field, field', '{!r}, {!r}')
        update = self._serialize_update(data)                       # 'field={!r}, field={!r}'

        sql = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s;" % (table, insert_k, insert_v, update)
        format_values = list(insert_data.values()) + list(data.values())
        sql = sql.format(*format_values)
        return self.query(sql).rowcount

    def delete(self, table, where : list = None):
        """Delete rows based on a where condition"""
        sql = "DELETE FROM %s" % table

        if where and len(where) > 0:
            sql += " WHERE " + " and ".join(where)
        return self.query(sql).rowcount

    def query(self, sql, params = None):
        """Run a raw query"""

        if params:
            sql = sql.format(*params)
            sql = sql.replace("'NULL'", "NULL")

        # check if connection is alive. if not, reconnect
        try:
            # print(sql)
            self.cur.execute(sql)
        # except MySQLdb.OperationalError as e:
        #     # mysql timed out. reconnect and retry once
        #     if e[0] == 2006:
        #         self.connect()
        #         self.cur.execute(sql, params)
        #     else:
        #         raise
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(e)
            print(sql)
            raise
        return self.cur

    def commit(self):
        """Commit a transaction (transactional engines like InnoDB require this)"""
        return self.conn.commit()

    def is_open(self):
        """Check if the connection is open"""
        return self.conn.open

    def end(self):
        """Kill the connection"""
        self.cur.close()
        self.conn.close()

    # ===

    def _serialize_insert(self, data):
        """Format insert dict values into strings"""
        keys = ",".join(data.keys())
        vals = ",".join(["{!r}" for k in data])
        return keys, vals

    # def _serialize_batch_insert(self, data):
    #     """Format insert dict values into strings"""
    #     keys = ",".join(data[0].keys())
    #     v = "(%s)" % ",".join(tuple("%s".rstrip(',') for v in range(len(data[0]))))
    #     l = ','.join(list(repeat(v, len(data))))
    #     return [keys, l]

    def _serialize_update(self, data):
        """Format update dict values into string"""
        return "={!r},".join(data.keys()) + "={!r}"

    def _format_select(self, table=None, fields=(), where=None, order=None, limit=None):
        """Format a select query"""

        # Try to avoid sql injection
        for i in range(len(fields)):
            fields[i] = fields[i].replace("`", "'")
        table = table.replace("`", "'")

        sql = "SELECT %s FROM %s" % (",".join(fields), table)

        # where conditions
        if where and len(where) > 0:
            sql += " WHERE " + " and ".join(where)

        # order
        if order and len(order) > 0:
            sql += " ORDER BY %s" % order[0]
            if len(order) > 1:
                sql += " %s" % order[1]

        # limit
        if limit:
            sql += " LIMIT %s" % limit[0]
            if len(limit) > 1:
                sql += ", %s" % limit[1]
        return sql
        # return self.query(sql, where[1] if where and len(where) > 1 else None)

    # def _select_join(self, tables=(), fields=(), join_fields=(), where=None, order=None, limit=None):
    #     """Run an inner left join query"""
    #
    #     fields = [tables[0] + "." + f for f in fields[0]] + \
    #              [tables[1] + "." + f for f in fields[1]]
    #
    #     sql = "SELECT %s FROM %s LEFT JOIN %s ON (%s = %s)" % \
    #           (",".join(fields),
    #            tables[0],
    #            tables[1],
    #            tables[0] + "." + join_fields[0], \
    #            tables[1] + "." + join_fields[1]
    #            )
    #
    #     # where conditions
    #     if where and len(where) > 0:
    #         sql += " WHERE %s" % where[0]
    #
    #     # order
    #     if order:
    #         sql += " ORDER BY %s" % order[0]
    #
    #         if len(order) > 1:
    #             sql += " " + order[1]
    #
    #     # limit
    #     if limit:
    #         sql += " LIMIT %s" % limit[0]
    #
    #         if len(limit) > 1:
    #             sql += ", %s" % limit[1]
    #
    #     return self.query(sql, where[1] if where and len(where) > 1 else None)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.end()
