class Test():

	def __init__(self, name: str, id: int, connect):
		self.name = name
		self.id = id
		self._connect = connect
		self.info = self._get_run_info()

	def _get_run_info(self):
		tmp_dict = {}
		try:
			tmp_dict = self._connect.send_get('get_test/' + str(self.id))
		except APIError as error:
			print (error)
		
		return tmp_dict