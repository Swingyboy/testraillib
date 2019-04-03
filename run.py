from testrail import APIError


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
		
class Run():
	
	def __init__(self, name: str, id: int, connect):
		self.name = name
		self.id = id
		self._connect = connect
		self.info = self._get_run_info()
		self._tests_dict = self._get_tests_dict()
		self.tests = self._get_tests_list()
		
	def _get_run_info(self):
		tmp_dict = {}
		try:
			tmp_dict = self._connect.send_get('get_run/' + str(self.id))
		except APIError as error:
			print (error)
		
		return tmp_dict
		
	def _get_tests_dict(self):
		try:
			tmp_list = self._connect.send_get('get_tests/' + str(self.id))
		except APIError as error:
			print (error)
		tmp_tests_dict = dict([(item['title'], item['id']) for item in tmp_list])
			
		return tmp_tests_dict
		
	def _get_tests_list(self):
		tests_list = list([item for item in self._tests_dict])
		return tests_list	
	
			
	def update(
			self, suite_id: int,
			new_name: str,
			description: str,
			milestone_id: int,
			assignedto_id: int,
			include_all: bool,
			case_ids: list):
				
		properties_dict = {
			'suite_id':suite_id,
			'name':new_name,
			'description':description,
			'milestone_id':milestone_id,
			'assignedto_id':assignedto_id,
			'include_all':include_all,
			'case_ids':case_ids
			}
		try:	
			self._connect.send_post('add_run/' + str(self.id), properties_dict)
		except APIError as error:
			print (error)
		
	def close_run(self):
		try:	
			self._connect.send_post('close_run/' + str(self.id), {})
		except APIError as error:
			print (error)
			
	def get_test(self, name):
		tmp_test = Test(name, self._tests_dict[name], self._connect)
		return tmp_test
			
