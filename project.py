from project_items import *


class Project():
	
	def __init__(self, name, id, connect):
		self.name = name
		self.id = id
		self._connect = connect
		self.info = self._get_project_info()
		self._runs_dict = self._get_runs_dict()
		self._suites_dict = self._get_suites_dict()
		self.runs = self._get_runs_list()
		self.suites = self._get_suites_list()
	
	def _get_project_info(self):
		tmp_dict = {}
		try:
			tmp_dict = self._connect.send_get('get_project/' + str(self.id))
		except APIError as error:
			print (error)
		
		return tmp_dict
	
	def _get_runs_dict(self):
		tmp_list = []
		try:
			tmp_list = self._connect.send_get('get_runs/' + str(self.id))
		except APIError as error:
			print (error)
		tmp_runs_dict = dict([(item['name'], item['id']) for item in tmp_list])
			
		return tmp_runs_dict	
	
	def _get_runs_list(self):
		runs_list = list([item for item in self._runs_dict])
		return runs_list
		
	def _get_suites_dict(self):
		tmp_list = []
		try:
			tmp_list = self._connect.send_get('get_suites/' + str(self.id))
		except APIError as error:
			print (error)
		tmp_suites_dict = dict([(item['name'], item['id']) for item in tmp_list])
			
		return tmp_suites_dict	
	
	def _get_suites_list(self):
		suites_list = list([item for item in self._suites_dict])
		return suites_list	

	def update(
			self, name: str,
			announce: str ='',
			show_announce: bool=True,
			is_completed: bool=False,
			suite_mode: int=0):
		
		properties_dict = {
			'name':name,
			'announcement':announce,
			'show_announcement':show_announce,
			'is_completed':is_completed,
			'suite_mode':suite_mode
			}
		try:	
			self._connect.send_post('update_project/' + str(self.id), properties_dict)
		except APIError as error:
			print (error)	
		
	def get_run(self, name):
		tmp_run = Run(name, self._runs_dict[name], self._connect)
		return tmp_run
	
	def add_run(
			self, suite_id: int,
			name: str,
			description: str,
			milestone_id: int,
			assignedto_id: int,
			include_all: bool,
			case_ids: list):
			
		properties_dict = {
			'suite_id':suite_id,
			'name':name,
			'description':description,
			'milestone_id':milestone_id,
			'assignedto_id':assignedto_id,
			'include_all':include_all,
			'case_ids':case_ids
			}
		try:	
			self._connect.send_post('add_run/' + str(self.Id), properties_dict)
		except APIError as error:
			print (error)
		
	def delete_run(self, name:str):
		try:	
			self._connect.send_post('delete_run/' + str(self._runs_dict[name]), {})
		except APIError as error:
			print (error)
			
	def get_suite(self, name):
		tmp_suite = Run(name, self._suites_dict[name], self._connect)
		return tmp_suite
		
	def add_suite(self, name: str, description: str):
		properties_dict = {'name':name, 'description':description}
		try:	
			self._connect.send_post('add_suite/' + str(self.Id), properties_dict)
		except APIError as error:
			print (error)

	def delete_suite(self, name:str):
		try:	
			self._connect.send_post('delete_suite/' + str(self._suites_dict[name]), {})
		except APIError as error:
			print (error)