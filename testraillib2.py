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
		
	def get_project(self, name):
		project = Project(name, self._projects_dict[name], self._connect)
		return project
		
	def add_project(self, name:str, announce:str='', showAnnounce:bool=True, suite_mode:int=1):
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
			

			
			
			
if __name__ == '__main__':
	client = Client('https://ams.testrail.com','SBE@apipro.com', 'Zergswarm20' )
	project = client.get_project('API PRO 10')
	print(project.suites[0])
	suite = project.get_suite(project.suites[0])
	print(suite.sections)
	