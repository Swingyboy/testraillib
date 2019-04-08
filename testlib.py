from testrail import *
from project import Project



		
class Client():

	def __init__(self, url, user='anonymous', password=''):
		self._url = url
		self._user = user
		self._password = password
		self._connect = self._create_connection()
		self._projects_dict = self._get_projects_dict()
		self.projects = self._get_projects()
		
	def _create_connection(self):
		client = APIClient(self._url)
		client.user = self._user
		client.password = self._password
		
		return client
		
	def _get_projects_dict(self):
		temp_projects_dict = {}
		try:
			projects_list = self._connect.send_get('get_projects')
		except APIError as error:
			print (error)
		
		for item in projects_list:
			temp_projects_dict.update({item['name']:item['id']})

		return temp_projects_dict
		
	def _get_projects(self):
		tmp_projects_list =[]
		for key in self._projects_dict: tmp_projects_list.append(key)
		
		return tmp_projects_list
		
	def add_case_field(
			self,
			type: str,
			name: str,
			label: str,
			description: str,
			include_all: bool,
			template_ids: list,
			configs
			):
			
		properties_dict = {
			'type':type,
			'name':name,
			'label':label,
			'description':description,
			'include_all':include_all,
			'template_ids':template_ids,
			'configs':configs
			}
		try:
			self._connect.send_get('add_case_field')
		except APIError as error:
			print (error)
	
	def get_case_fields(self):
		temp_fields_list = []
		try:
			temp_fields_list = self._connect.send_get('get_case_fields')
		except APIError as error:
			print (error)
			
		return temp_fields_list
		
	def get_case_types(self):
		temp_types_list = []
		try:
			temp_types_list = self._connect.send_get('get_case_types')
		except APIError as error:
			print (error)
			
		return temp_types_list
		
	def get_priorities(self):
		temp_priorities_list = []
		try:
			temp_priorities_list = self._connect.send_get('get_priorities')
		except APIError as error:
			print (error)
			
		return temp_priorities_list
		
	def get_project(self, name):
		project = Project(self._projects_dict[name], self._connect)
		return project
		
	def add_project(
			self,
			name:str, announce:str='',
			showAnnounce:bool=True,
			suite_mode:int=1
			):
			
		properties_dict = {'name':name,
			'announcement':announce,
			'show_announcement':showAnnounce,
			'suite_mode':suite_mode
			}
		try:	
			self._connect.send_post('add_project', properties_dict)
		except APIError as error:
			print (error)
	
	def delete_project(self, name):
		try:	
			self._connect.send_post('delete_project/' + str(self._projects_dict[name]),{})
		except APIError as error:
			print (error)
			
	def get_result_fields(self):
		temp_result_list = []
		try:
			temp_result_list = self._connect.send_get('get_result_fields')
		except APIError as error:
			print (error)
		
		return temp_result_list
			

	
			
			
if __name__ == '__main__':
	client = Client('https://ams.testrail.com','SBE@apipro.com', 'Zergswarm20' )
	project = client.get_project('API PRO 10')
	print(project.get_templates())
	print(project.runs[2])
	run = project.get_run(project.runs[2])
	suite = run.get_suite()
	print(suite.info)
	case = suite.get_case(suite.cases[1])
	print(case.id)
	print(case.info)
	print(run.get_results_for_case(case.id))