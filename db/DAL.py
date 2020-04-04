import os
from collections import namedtuple
from contextlib import contextmanager
import re
import json
import MySQLdb

from db.exceptions import CallProcError, DBConnectionError, DatabaseError, SQLError

ERROR_MSG = 'ErrorMsg'

def Row(columns):
	return namedtuple('Data', columns)

class DAL: # (Data access layer)
	def __init__(self, env='dev', db='jeopardy'):
		self.db = db
		if os.environ.get('JAWS_DB'):
			# Production config
			self.config = {
				"host": os.environ.get('JAWS_HOST'),
				"user": os.environ.get('JAWS_USER'),
				"passwd": os.environ.get('JAWS_PASSWORD'),
				"db": os.environ.get('JAWS_DB')
			}
		else:
			# Local config
			with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as f:
				j = json.load(f)

				if env not in j:
					raise Exception(f"Unable to use config environment {env}")

				if db not in j[env]:
					raise Exception(f'Unable to find config for database {db} in the {env} environment')
				self.config = j[env][db]

	@contextmanager
	def connection(self, connection=None):
		try:
			connection = MySQLdb.connect(**self.config)
			cursor = connection.cursor()
			yield connection, cursor
		except (CallProcError, SQLError, DatabaseError):
			raise
		except Exception as e:
			raise DBConnectionError(self.config, e)
		finally:
			if connection:
				cursor.close(); connection.commit(); connection.close()

	def get_data(self, cursor, one_or_none=False):
		if not cursor.description: return None
		columns = [d[0] for d in cursor.description]
		Data = Row(columns)
		if one_or_none:
			return Data(*cursor.fetchone()) if cursor.rowcount else None
		else:
			return [Data(*row) for row in cursor.fetchall()]

	def execute(self, sql, args=(), one_or_none=False, many=False, insert=False):
		with self.connection() as (connection, cursor):
			try:
				if many:
					cursor.executemany(sql, args=args)
				else:
					cursor.execute(sql, args=args)
				data = self.get_data(cursor, one_or_none=one_or_none) if not insert else (cursor.lastrowid, cursor.rowcount)
				if not insert and data and ((one_or_none and ERROR_MSG in data._fields) or (not one_or_none and ERROR_MSG in data[0]._fields)):
					raise DatabaseError(data.ErrorMsg if one_or_none else data[0].ErrorMsg, args)
				return data
			except Exception as e:
				raise SQLError(sql, args, one_or_none, e)

	def callproc(self, procname, args=(), one_or_none=False):
		with self.connection() as (connection, cursor):
			try:
				cursor.callproc(procname, args)
				data = self.get_data(cursor, one_or_none=one_or_none)
				if data and ((one_or_none and ERROR_MSG in data._fields) or (not one_or_none and ERROR_MSG in data[0]._fields)):
					raise DatabaseError(data.ErrorMsg if one_or_none else data[0].ErrorMsg, args)
				return data
			except Exception as e:
				raise CallProcError(procname, args, one_or_none, e)
