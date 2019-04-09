from testrail import APIError
from items.suite import Suite


class Test():

	def __init__(self, id: int, connect):
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
		
	def add_result(self,
			status_id: int,
			comment: str,
			version: str,
			elapsed: str,
			defects: str,
			assignedto_id: int
			):
				
		properties_dict = {
			'status_id':status_id,
			'comment':comment,
			'version':version,
			'elapsed':elapsed,
			'defects':defects,
			'assignedto_id':assignedto_id
			}
			
		try:	
			self._connect.send_post('add_result/' + str(self.id), properties_dict)
		except APIError as error:
			print (error)
		
		
	def get_results(self):
		temp_results_list = []
		try:
			temp_results_list = self._connect.send_get('get_results/' + str(self.id))
		except APIError as error:
			print (error)
			
		return temp_results_list
		
class Run():
	
	def __init__(self, id: int, connect):
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
			case_ids: list
			):
				
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
			
	def get_suite(self):
		return Suite(self.info['suite_id'], self._connect)
			
	def get_test(self, name):
		tmp_test = Test(self._tests_dict[name], self._connect)
		return tmp_test
		
	def add_result_for_case(self,
			case_id,
			status_id: int,
			comment: str,
			version: str,
			elapsed: str,
			defects: str,
			assignedto_id: int
			):
				
		properties_dict = {
			'status_id':status_id,
			'comment':comment,
			'version':version,
			'elapsed':elapsed,
			'defects':defects,
			'assignedto_id':assignedto_id
			}
			
		try:	
			self._connect.send_post('add_result_for_case/' + str(self.id) +'/' + str(case_id), properties_dict)
		except APIError as error:
			print (error)
			
	def add_results_for_tests(self, results_list:list):
		try:	
			self._connect.send_post('add_results/' + str(self.id), results_list)
		except APIError as error:
			print (error)
			
	def add_results_for_cases(self, results_list:list):
		try:	
			self._connect.send_post('add_results/' + str(self.id), results_list)
		except APIError as error:
			print (error)

	def get_results(self):
		temp_results_list = []
		try:
			temp_results_list = self._connect.send_get('get_results_for_run/' + str(self.id))
		except APIError as error:
			print (error)
			
		return temp_results_list
		
	def get_results_for_case(self, case_id):
		temp_results_list = []
		try:
			temp_results_list = self._connect.send_get('get_results_for_case/' + str(self.id) +'/' + str(case_id))
		except APIError as error:
			print (error)
			
		return temp_results_list
		

			
