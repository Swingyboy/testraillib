from testrail import *
from project import Project


class Client():
	""" The base class that create the connection to the test-rail URL.

	This class takes the next arguments:
		URL 		- 	The URL address of the TestRail.
		user 		- 	The name of the user that has access to the TestRail.
					The default value is "anonymous".  
		password	-	The password of the user for the access to the TestRail.
					The default value is "".
		
	The class has the next attributes:
		__url				- 	Private attribute that contains the URL address of the TestRail.
		__user				- 	Private attribute that contains the name of the user that connected to the TestRail.
		__password			- 	Private attribute that contains the password of the user.
		__connect			- 	Private attribute that contains the connection and is used for transfering the connection
							to another elements of the TestRail
		__project_dict			-	Private attribute that contains the dictionary of the "Project_name":"Project_id" pairs.
							This attribute is necessary because TestRail API v.2 uses the ID of elements, but usually
							the user knows only the names, and not these IDs.
		projects			-	Public attribute that contains the list of the projects these are present in the TestRail.

	The class has the next methods:
		__init__()					-	The class constructor accepts the URL, the loggin of the user
		__create_connection()				-	Private method that establishes the connection to TestRail using the values from the _url, 
									_user and _password attributes. Return the APIClient object as the object that is responded for the connection.
		__get_projects_dict()				- 	Private method that returns the dictionary of the "Project_name":"Project_id" pairs or prints the 
									error message if the APIClient object doesn't return the "200 OK" code.
		__get_projects()				- 	Private method that returns the list of the projects' names these are contained in the TestRail. 
									This method is used for filling the .projects attribute.
		add_case_field()				-	Public method that adds the test case custom field to the TestRail.
		get_case_fields()				-	Public method that returns the list of the test case custom fields these are present in the TestRail.
		get_case_types()				-	Public method that returns the list of available case types these are present in the TestRail.
		get_priorities()				-	Public method that returns the list of available priorities these are present in the TestRail.
		get_project()					-	Public method that returns the Project object.
		add_project()					-	Public method that adds the project to the TestRail.
		delete_project()				-	Public method that deletes the project from the TestRail.
		get_result_fields()				-	Public method that returns the list of available test result custom fields these are present in the TestRail.
	"""
		
	def __init__(self, url, user='anonymous', password=''):
		"""The class constructor accepts the URL, the loggin of the user ("anonymous" by default) and the password ("" by default)""" 
		self.__url = url 										#set the _url attribute
		self.__user = user 										#set the _user attribute
		self.__password = password 								#set the _password attribute
		self.__connect = self.__create_connection() 			#set the __connect attribute by calling the _create_connection() method
		self.__projects_dict = self.__get_projects_dict() 		#set the _projects_dict attribute by calling the _get_projects_dict() method
		self.projects = self.__get_projects() 					#set the projects attribute by calling the _get_projects() method
	
	def __create_connection(self):
		"""The method that is called by class constructor and establishes the connection to TestRail"""
		client = APIClient(self.__url)							#create the APIClient instance and setting the URL to this instance
		client.user = self.__user								#set the .user attribute for the APIClient instance
		client.password = self.__password						#set the .password attribute for the APIClient instance
		return client											#return the APIClient instance
	
	def __get_projects_dict(self):
		"""The method that returns the dictionary of the "Project_name":"Project_id" pairs."""									
		projects_list = []											#set the temporary list. This is necessary because if .send_get method doesn't return "200 OK" response the error happens
		try:														#try to get the list list of available projects with its attributes
			projects_list = self.__connect.send_get('get_projects')	#by sending "GET" request "get_projects" to the TestRail API
		except APIError as error:									#except the case when method doesn't return "200 OK" response
			print (error)											#print the response code in this case
		temp_projects_dict = {}
		for item in projects_list:									#iterate thru the list of vailable projects
			temp_projects_dict.update({item['name']:item['id']})	#fill the temporary dictionary by the "Project_name":"Project_id" pairs 
		return temp_projects_dict									#return the temporary dictionary
	
	def __get_projects(self):
		"""The method that creates the list of project names form the .__projects_dict attribute."""
		tmp_projects_list =[]											#create the temporaty list
		for key in self.__projects_dict: tmp_projects_list.append(key)	#iterate the __projects_dict and append the keys from this dict to temporary list
		return tmp_projects_list										#return the temorary list
	
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
		"""The method that adds the test case custom field to the project. The method takes next arguments:

			type			-	The type identifier for the new custom field						as 	STRING
			name			-	The name for new the custom field								as 	STRING
			label			-	The label for the new custom field								as 	STRING
			description		-	The description for the new custom field							as 	STRING
			include_all		-	The flag for including the new custom field in all templates				as 	BOOLEAN
			template_ids		-	The ID's of templates new custom field (is necessary if 'include_all' = FALSE)		as 	ARRAY 
			configs			-	The object wrapped in an array with two default keys, 'context' and 'options'		as 	OBJECT	
		"""
		properties_dict = {										#Fill the dictionary of new case field attributes 
			'type':type,
			'name':name,
			'label':label,
			'description':description,
			'include_all':include_all,
			'template_ids':template_ids,
			'configs':configs
			}
		try:																			#try to create a new case field 
			response = self.__connect.send_post('add_case_field', properties_dict)		#by sending a "POST" request "add_case_field" to the TestRail API with specified attributes
			print('Project ' + name +' was added!')
			return response
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case
			return None
	
	def get_case_fields(self):
		"""The method that returns the list of test case custom fields"""
		temp_fields_list = []												#create the temporaty list
		try:																#try to get the list of avialable custom fields
			temp_fields_list = self.__connect.send_get('get_case_fields')	#by sending "GET" request "get_case_fields" to the TestRail API
		except APIError as error:											#except the case when method doesn't return "200 OK" response
			print (error)													#print the response code in this case
		return temp_fields_list												#return the temporary list
	
	def get_case_types(self):
		"""The method that returns the list of available case types"""
		temp_types_list = []												#create the temporaty list
		try:																#try to get the list of avialable case types
			temp_types_list = self.__connect.send_get('get_case_types')		#by sending "GET" request "get_case_types" to the TestRail API
		except APIError as error:											#except the case when method doesn't return "200 OK" response
			print (error)													#print the response code in this case
		return temp_types_list												#return the temporary list
	
	def get_priorities(self):
		"""The method that returns the list of available priorities"""
		temp_priorities_list = []												#create the temporaty list
		try:																	#try to get the list of avialable priorities
			temp_priorities_list = self.__connect.send_get('get_priorities')	#by sending "GET" request "get_priorities" to the TestRail API
		except APIError as error:												#except the case when method doesn't return "200 OK" response
			print (error)														#print the response code in this case
		return temp_priorities_list												#return the temporary list
	
	def get_project(self, name):
		"""The method that takes the name of the project as STRING and returns the Project object"""
		try:															#find the project ID throught the name and call the Project class
			return Project(self.__projects_dict[name], self.__connect)	#return the instance
		except KeyError:
			print('There is no such project!')
			return None
	
	def add_project(
			self,
			name:str,														#name of a new project as STRING
			announce:str='',												#description of a new project as STRING								
			showAnnounce:bool=True,											#flag for displaying the announcement on the project's overview page (default True) as BOOLEAN
			suite_mode:int=1												#suite mode (1 - single suite mode, 2 - single suite + baseline meode, 3 - multiple suites mode) as INTEGER
			):
		"""The method that adds the project to the TestRail. The method takes next arguments:
		
			name		-	name of a new project 											as STRING
			announce	-	description of a new project 										as STRING
			showAnnounce	-	flag for displaying the announcement on the project's overview page (default True) 		as BOOLEAN
			suite_mode	-	suite mode (1 - single suite mode, 2 - single suite + baseline meode, 3 - multiple suites mode)	as INTEGER
		"""
			
		properties_dict = {'name':name,										#Fill the dictionary of new project attributes 
			'announcement':announce,
			'show_announcement':showAnnounce,
			'suite_mode':suite_mode
			}
		try:																		#try to create a new project
			response = self.__connect.send_post('add_project', properties_dict)		#by sending a "POST" request "add_project" to the TestRail API with specified attributes
			self.__projects_dict.update({response['name']:response['id']})
			self.projects.append(response['name'])
			print('Project ' + name +' was added!')
			return Project(response['id'], self.__connect)
		except APIError as error:											#except the case when method doesn't return "200 OK" response
			print (error)													#print the response code in this case
			return None
			
	def delete_project(self, name):																
		"""	The method that takes the name of the project as STRING and deletes the project to the TestRail.
			
			Deleting a project cannot be undone and also permanently deletes all test suites & cases, 
			test runs & results and everything else that is part of the project.
		"""
		try:																					#try to delete a project
			self.__connect.send_post('delete_project/' + str(self.__projects_dict[name]),{})	#by sending a "POST" request "delete_project" to the TestRail API with empty dict as attributes
			del self.__projects_dict[name]
			self.projects.remove(name)
			print('Project' + name +' was deleted!')
		except APIError as error:																#except the case when method doesn't return "200 OK" response
			print (error)																		#print the response code in this case
		except KeyError:
			print('There is no such project!')
		return None

	def get_result_fields(self):
		"""The method that returns the list of available test result custom fields."""
		temp_result_list = None															#create the temporaty list
		try:																			#try to get the list of available test result custom fields
			temp_result_list = self.__connect.send_get('get_result_fields')				#by sending "GET" request "get_result_fields" to the TestRail API
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case
		return temp_result_list															#return the temporary list