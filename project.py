from items.run import Run
from items.suite import Suite
from items.milestone import Milestone


class Project():
	
	def __init__(self, id, connect):
		self.id = id
		self._connect = connect
		self._milestones_dict = self._get_milestones_dict()
		self._plans_dict = self._get_plans_dict()
		self._runs_dict = self._get_runs_dict()
		self._suites_dict = self._get_suites_dict()
		self.info = self._get_project_info()
		self.milestones = self._get_milestones_list()
		self.plans = self._get_plans_list()
		self.runs = self._get_runs_list()
		self.suites = self._get_suites_list()
	
	def _get_milestones_dict(self):
		try:
			tmp_list = self._connect.send_get('get_milestones/' + str(self.id))
		except APIError as error:
			print (error)
		tmp_milestones_dict = dict([(item['name'], item['id']) for item in tmp_list])
		
		return tmp_milestones_dict
		
	def _get_milestones_list(self):
		milestones_list = list([item for item in self._milestones_dict])
		return milestones_list	
	
	def _get_project_info(self):
		try:
			tmp_dict = self._connect.send_get('get_project/' + str(self.id))
		except APIError as error:
			print (error)
		
		return tmp_dict
		
	def _get_plans_dict(self):
		try:
			tmp_list = self._connect.send_get('get_plans/' + str(self.id))
		except APIError as error:
			print (error)
		tmp_suites_dict = dict([(item['name'], item['id']) for item in tmp_list])
			
		return tmp_suites_dict

	def _get_plans_list(self):
		plans_list = list([item for item in self._plans_dict])
		return plans_list			
	
	def _get_runs_dict(self):
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
		try:
			tmp_list = self._connect.send_get('get_suites/' + str(self.id))
		except APIError as error:
			print (error)
		tmp_suites_dict = dict([(item['name'], item['id']) for item in tmp_list])
			
		return tmp_suites_dict		
	
	def _get_suites_list(self):
		suites_list = list([item for item in self._suites_dict])
		return suites_list
		
	def _get_sections_dict(self, suite):
		tmp_list = []
		try:
			tmp_list = self._connect.send_get('get_sections/' + str(self.id) + '&suite_id=' + str(suite.id))
		except APIError as error:
			print (error)
		
		return dict([(item['name'], item['id']) for item in tmp_list])
		
	def get_sections_list(self, suite):
		self._sections_dict = self._get_sections_dict(suite)
		sections_list = list([item for item in self._sections_dict])
		return sections_list

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
			
	def get_milestone(self, name):
		tmp_milestone = Milestone(self._milestones_dict[name], self._connect)
		return tmp_milestone
		
	def add_milestone(
			self, 
			name: str,
			description: str,
			due_on: str,
			parent_id: int,
			start_on: str
			):
			
		properties_dict = {
			'name':name,
			'description':description,
			'due_on':due_on,
			'parent_id':parent_id,
			'start_on':start_on,
			'case_ids':case_ids
			}
		try:	
			self._connect.send_post('add_milestone/' + str(self.Id), properties_dict)
		except APIError as error:
			print (error)	
		
	def get_run(self, name):
		tmp_run = Run(self._runs_dict[name], self._connect)
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
		if isinstance(name, str):
			id = self._suites_dict[name]
		if isinstance(name, int):
			id = name
		
		tmp_suite = Suite(id, self._connect)
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
			
	def get_section(self, name):
		tmp_section = Section(self._sections_dict[name], self._connect)
		return tmp_section

	def add_section(
			self, name: str,
			description: str,
			parent_id: int):
			
		properties_dict = {
			'name':name,
			'description':description,
			'parent_id': parent_id
			}
		try:	
			self._connect.send_post('add_section/' + str(self.Id), properties_dict)
		except APIError as error:
			print (error)		

	def delete_section(self, name):
		try:	
			self._connect.send_post('delete_section/' + str(self._sections_dict[name]), {})
		except APIError as error:
			print (error)
			
	def get_templates(self):
		template_list = []
		try:
			template_list = self._connect.send_get('get_templates/' + str(self.id))
		except APIError as error:
			print (error)
				
		return template_list