class CallProcError(Exception):
	def __init__(self, procname, args, one_or_none, e):
		self.message = (
				f"\n<--------- Stored Procedure Error --------->\n"
		 			f"Procedure: {procname}\n"
		 			f"Passed in Args: {args}\n"
		 			f"One or None: {one_or_none}\n"
		 		)
		if len(e.args) == 2:
			self.message += (
						f"SQL Error Code: {e.args[0]}\n"
						f"SQL Error Message: {e.args[1]}"
					)
		elif len(e.args) == 1:
			self.message += f"{e.args[0]}\n"
		super().__init__(self.message)

class DBConnectionError(Exception):
	def __init__(self, config, e):
		self.message = (
				"\n<---- Database Connection Error ---->\n"
		 			f"Host: {config['host']}\n"
		 			f"User: {config['user']}\n"
		 			f"Password: {'*'*len(config['passwd'])}\n"
		 			f"Database: {config['db']}\n"
		 			f"Exception: {e}"
	 			)
		super().__init__(self.message)

class DatabaseError(Exception):
	def __init__(self, db_exception, args):
		self.message = (
				f"\n<--------- Database Error --------->\n"
				f"ErrorMsg: {db_exception}\n"
				f"Passed in Args: {args}\n"
			)
		super().__init__(self.message)
		
class SQLError(Exception):
	def __init__(self, sql, args, one_or_none, e):
		self.message = (
					f"\n<--------- SQL Error -------->\n"
		 			f"SQL Statement: \n"
		 			f"{sql}\n"
		 			f"Passed in Args: {args}\n"
		 			f"One or None? {one_or_none}\n"
		 		)
		if len(e.args) == 2:
			self.message += (
						f"SQL Error Code: {e.args[0]}\n"
						f"SQL Error Message: {e.args[1]}"
					)
		elif len(e.args) == 1:
			self.message += f"{e.args[0]}\n"
		super().__init__(self.message)
