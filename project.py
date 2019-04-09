from testrail import APIError

from items.run import Run
from items.suite import Suite
from items.milestone import Milestone


class Project():
	""" The Project class that create Project instance.

	This class takes the next arguments:
		id 			- 	The ID of the project in the TestRail.
		connect 		- 	The connect instance that is APIClient object.

	The class has the next attributes:
		__connect		- 	Private attribute that contains the connection and is used for transfering the connection
							to another elements of the TestRail
		__milestones_dict	-	Private attribute that contains the dictionary of the "Milestone_name":"Milestone_id" pairs
							This attribute is necessary because TestRail API v.2 uses the ID of elements, but usually
							the user knows only the names, and not these IDs.
		__plans_dict		-	Private attribute that contains the dictionary of the "Plan_name":"Plan_id" pairs.
							This attribute is necessary because TestRail API v.2 uses the ID of elements, but usually
							the user knows only the names, and not these IDs.
		__runs_dict		-	Private attribute that contains the dictionary of the "Run_name":"Run_id" pairs.
							This attribute is necessary because TestRail API v.2 uses the ID of elements, but usually
							the user knows only the names, and not these IDs.
		__suites_dict		-	Private attribute that contains the dictionary of the "Suite_name":"Suite_id" pairs.
							This attribute is necessary because TestRail API v.2 uses the ID of elements, but usually
							the user knows only the names, and not these IDs.
		
		id				-	Public attribute that contains the ID of the project
		info				-	Public attribute that contains the dictionary with the properties of the project instance.
		milestones			-	Public attribute that contains the list of the milestones these are present in the project instance.
		plans				-	Public attribute that contains the list of the plans these are present in the project instance.
		runs				-	Public attribute that contains the list of the runs these are present in the project instance.
		suites				-	Public attribute that contains the list of the suites these are present in the project instance.

	The class has the next methods:
		__init__()					-	The class constructor accepts the ID of the project and the connect instance.
		_get_milestones_dict()				-	Private method that returns the dictionary of the "Milestone_name":"Milestone_id" pairs or prints the 
									error message if the APIClient object doesn't return the "200 OK" code.
									This method is used for initialisation the .__milestones_dict attribute.
		__get_milestones_list()				-	Private method that returns the list of the milestones names these are contained in the project instance. 
									This method is used for filling the .milestones attribute.
		__get_plans_dict()				- 	Private method that returns the dictionary of the "Plan_name":"Plan_id" pairs or prints the
									error message if the APIClient object doesn't return the "200 OK" code. 
									The method is used for initialisation the .__plans_dict attribute.
		__get_plans_list()				-	Private method that returns the list of the plans names these are contained in the project instance. 
									This method is used for filling the .plans attribute.
		__get_project_info()				-	Private method that returns dictionary with the properties of the project instance.
									This method is used for initialisation the .info attribute.
		__get_runs_dict()				- 	Private method that returns the dictionary of the "Run_name":"Run _id" pairs or prints the
									error message if the APIClient object doesn't return the "200 OK" code. 
									The method is used for initialisation the .__runs_dict attribute.
		__get_runs_list()				-	Private method that returns the list of the runs names these are contained in the project instance. 
									This method is used for filling the .runs attribute.
		__get_sections_dict()				-	Private method that returns the dictionary of the "Section_name":"Section_id" pairs or prints the
									error message if the APIClient object doesn't return the "200 OK" code. 
		__get_suites_dict()				- 	Private method that returns the dictionary of the "Suite_name":"Suite _id" pairs or prints the
									error message if the APIClient object doesn't return the "200 OK" code. 
									The method is used for initialisation the .__plans_dict attribute.
		__get_suites_list()				-	Private method that returns the list of the suites names these are contained in the project instance. 
									This method is used for filling the .suites attribute.
		
		add_milestone()					-	Public method that adds the Milestone to the project instance.
		add_run()					-	Public method that adds the Run to the project instance.
		add_section()					- 	Public method that adds the Section to the project instance.
		add_suite()					- 	Public method that adds the Suite to the project instance.
		delete_milestone()				-	Public method that deletes the Milestone from the project instance
		delete_run()					-	Public method that deletes the Run from the project instance.
		delete_section()				-	Public method that deletes the Section from the project instance.
		delete_suite()					-	Public method that deletes the Suite from the project instance.
		get_templates()					-	Public method that returns the list of available templates for the project instance.
		get_milestone()					-	Public method that returns the Milestone object.
		get_run()					-	Public method that returns the Run object.
		get_sections_list()				-	Public method that returns the list of the sections that are connected to the project instance.
		get_section()					-	Public method that returns the Section object.
		get_suite()					-	Public method that returns the Suite object.
		update()					-	Public method that updates the project instance.
	"""
	
	def __init__(self, id, connect):
		"""The class constructor accepts the ID of the project and APIClient object as connect instance"""
		
		self.id = id													#set the id attribute
		self.__connect = connect											#set the connect attribute 
		self.__milestones_dict = self.__get__milestones_dict()				#set the __milestones_dict attribute by calling the __get__milestones_dict() method
		self.__plans_dict = self.__get__plans_dict()						#set the __plans_dict attribute by calling the __get__plans_dict() method
		self.__runs_dict = self.__get__runs_dict()							#set the __runs_dict attribute by calling the __get__runs_dict() method
		self.__suites_dict = self.__get__suites_dict()						#set the __suites_dict attribute by calling the __get__suites_dict() method
		self.info = self.__get_project_info()							#set the info attribute by calling the __get_project_info() method
		self.milestones = self.__get_milestones_list()					#set the milestones attribute by calling the __get_milestones_list() method
		self.plans = self.__get_plans_list()								#set the plans milestones by calling the __get_plans_list() method
		self.runs = self.__get_runs_list()								#set the runs milestones by calling the __get_runs_list() method
		self.suites = self.__get_suites_list()							#set the suites milestones by calling the __get_suites_list() method
	
	def __get__milestones_dict(self):
		"""Private method that returns the dictionary of the "Milestone_name":"Milestone_id" pairs
		or prints the error message if the APIClient object doesn't return the "200 OK" code.
		"""
		try:																				#try to get the list of project milestones with its attributes
			tmp_list = self.__connect.send_get('get_milestones/' + str(self.id))				#by sending "GET" request "get_milestones" to the TestRail API
		except APIError as error:															#except the case when method doesn't return "200 OK" response
			print (error)																	#print the response code in this case
		
		tmp_milestones_dict = dict([(item['name'], item['id']) for item in tmp_list])		#create the temporary dictionary of the "Milestone_name":"Milestone_id" pairs
		return tmp_milestones_dict															#return the temporary dictionary
		
	def __get_milestones_list(self):
		"""Private method that returns the list of the milestones names these are contained in the project instance."""
		
		milestones_list = list([item for item in self.__milestones_dict])			#iterate the __milestones_dict and create the temporary list from the keys 
		return milestones_list														#return the temporary list
		
	def __get__plans_dict(self):
		"""Private method that returns the dictionary of the "Plan_name":"Plan_id" pairs 
		or prints the error message if the APIClient object doesn't return the "200 OK" code.
		"""
		try:																		#try to get the list of project plans with its attributes
			tmp_list = self.__connect.send_get('get_plans/' + str(self.id))			#by sending "GET" request "get_plans" to the TestRail API
		except APIError as error:													#except the case when method doesn't return "200 OK" response
			print (error)															#print the response code in this case
		
		tmp__suites_dict = dict([(item['name'], item['id']) for item in tmp_list])	#create the temporary dictionary of the "Plan_name":"Plan_id" pairs
		return tmp__suites_dict														#return the temporary dictionary

	def __get_plans_list(self):
		"""Private method that returns the list of the plans names these are contained in the project instance."""
		
		plans_list = list([item for item in self.__plans_dict])				#iterate the __plans_dict and create the temporary list from the keys
		return plans_list													#return the temporary list
		
	def __get_project_info(self):
		"""Private method that returns dictionary with the properties of the project instance."""
		
		try:																	#try to get the list of project attributes
			tmp_dict = self.__connect.send_get('get_project/' + str(self.id))	#by sending "GET" request "get_project" to the TestRail API
		except APIError as error:												#except the case when method doesn't return "200 OK" response
			print (error)														#print the response code in this case
		
		return tmp_dict															#return the temporary dictionary
	
	def __get__runs_dict(self):
		"""Private method that returns the dictionary of the "Run_name":"Run _id" pairs
		or prints the error message if the APIClient object doesn't return the "200 OK" code.
		"""
		try:																#try to get the list of project runs with its attributes
			tmp_list = self.__connect.send_get('get_runs/' + str(self.id))	#by sending "GET" request "get_runs" to the TestRail API
		except APIError as error:											#except the case when method doesn't return "200 OK" response
			print (error)													#print the response code in this case
		
		tmp_runs_dict = dict([(item['name'], item['id']) for item in tmp_list])	#create the temporary dictionary of the "Run_name":"Run_id" pairs
		return tmp_runs_dict													#return the temporary dictionary
		
	def __get_runs_list(self):
		"""Private method that returns the list of the runs names these are contained in the project instance."""
		
		runs_list = list([item for item in self.__runs_dict])			#iterate the __runs_dict and create the temporary list from the keys
		return runs_list												#return the temporary list

	def _get_sections_dict(self, suite):
		"""Private method that returns the dictionary of the "Section_name":"Section_id" pairs
		or prints the error message if the APIClient object doesn't return the "200 OK" code.
		The method takes next arguments:
		
		suite - The ID of the test suite (optional if the project is operating in single suite mode)	as	INTEGER 
		"""
		tmp_list = []																							#create the temporaty list														
		try:																									#try to get the list of avialable sections
			tmp_list = self.__connect.send_get('get_sections/' + str(self.id) + '&suite_id=' + str(suite.id))	#by sending "GET" request "get_sections" to the TestRail API
		except APIError as error:																				#except the case when method doesn't return "200 OK" response
			print (error)																						#print the response code in this case
		
		return dict([(item['name'], item['id']) for item in tmp_list])											#iterate throught the tmp_list, create the dictionary of "Section_name":"Section_id" pairs and return it.	
		
	def __get__suites_dict(self):
		"""Private method that returns the dictionary of the "Suite_name":"Suite _id" pairs
		or prints the error message if the APIClient object doesn't return the "200 OK" code.
		"""
		
		try:																				#try to get the list of avialable suites
			tmp_list = self.__connect.send_get('get_suites/' + str(self.id))					#by sending "GET" request "get_suites" to the TestRail API
		except APIError as error:															#except the case when method doesn't return "200 OK" response
			print (error)																	#print the response code in this case
		
		return dict([(item['name'], item['id']) for item in tmp_list])						#iterate throught the tmp_list, create the dictionary of "Section_name":"Section_id" pairs and return it.
	
	def __get_suites_list(self):
		"""Private method that returns the list of the suites names these are contained in the project instance."""
		
		suites_list = list([item for item in self.__suites_dict])	#iterate the __suites_dict and create the temporary list from the keys
		return suites_list											#return the temporary list
		
	def add_milestone(
			self, 
			name: str,
			description: str,
			due_on: str,
			parent_id: int,
			start_on: str
			):
		"""Public method that adds the Milestone to the project instance. The method takes next arguments:
		
			name			-	The name of the milestone (required)				as	STRING
			description		-	The description of the milestone				as	STRING
			due_on			-	The due date of the milestone (as UNIX timestamp) 	as 	STRING (should be TIMESTAMP)
			parent_id		-	The ID of the parent milestone					as	INTEGER
			start_on		-	The scheduled start date of the milestone			as	STRING (should be TIMESTAMP)
		"""
			
		properties_dict = {						#Fill the dictionary of new milestone attributes 
			'name':name,
			'description':description,
			'due_on':due_on,
			'parent_id':parent_id,
			'start_on':start_on,
			'case_ids':case_ids
			}
		try:																			#try to create a new milestone
			self.__connect.send_post('add_milestone/' + str(self.Id), properties_dict)	#by sending "POST" request "add_milestone" to the TestRail API
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case

	def add_run(
			self, 
			suite_id: int,
			name: str,
			description: str,
			milestone_id: int,
			assignedto_id: int,
			include_all: bool,
			case_ids: list):
		"""Public method that adds the Run to the project instance. The method takes next arguments:
		
			suite_id	-	The ID of the test suite for the test run (optional if the project is operating in single suite mode, required otherwise)	as	INTEGER
			name		-	The name of the test run														as	STRING
			description	-	The description of the test run														as	STRING
			milestone_id	-	The ID of the milestone to link to the test run												as	INTEGER
			assignedto_id	-	The ID of the user the test run should be assigned to										as	INTEGER
			include_all	-	Flag that is responded for including all test cases of the test suite								as	BOOLEAN
			case_ids	-	An array of case IDs for the custom case selection											as	ARRAY
		"""
			
		properties_dict = {									#Fill the dictionary of new run attributes 
			'suite_id':suite_id,
			'name':name,
			'description':description,
			'milestone_id':milestone_id,
			'assignedto_id':assignedto_id,
			'include_all':include_all,
			'case_ids':case_ids
			}
		try:																		#try to create a new run 
			self.__connect.send_post('add_run/' + str(self.Id), properties_dict)		#by sending "POST" request "add_run" to the TestRail API
		except APIError as error:													#except the case when method doesn't return "200 OK" response
			print (error)															#print the response code in this case

	def add_section(
			self,
			name: str,
			description: str,
			parent_id: int,
			suite_id: int
			):
		"""Public method that adds the Section to the project instance. The method takes next arguments:
			
			name			-		The name of the section (required)											as		STRING
			description		-		The description of the section												as		STRING
			parent_id		-		The ID of the parent section (to build section hierarchies)							as		INTEGER
			suite_id		-		The ID of the test suite (ignored if the project is operating in single suite mode, required otherwise)		as		INTEGER
		"""
			
		properties_dict = {					#Fill the dictionary of new section attributes 
			'name':name,
			'description':description,
			'parent_id': parent_id,
			'suite_id':suite_id
			}
		try:																			#try to create a new section 
			self.__connect.send_post('add_section/' + str(self.Id), properties_dict)		#by sending "POST" request "add_section" to the TestRail API
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case

	def add_suite(self,
			name: str,
			description: str
			):
		"""Public method that adds the Suite to the project instance. The method takes next arguments:
		
			name		-		The name of the test suite (required)		as	STRING
			description	-		The description of the test suite		as	STRING
		"""
			
		properties_dict = {'name':name, 'description':description}					#fill the dictionary of new suite attributes 
		try:																		#try to create a new section 
			self.__connect.send_post('add_suite/' + str(self.Id), properties_dict)	#by sending "POST" request "add_suite" to the TestRail API
		except APIError as error:													#except the case when method doesn't return "200 OK" response
			print (error)															#print the response code in this case
			
	def delete_milestone(self, name:str):
		"""Public method that deletes the Milestone from the project instance."""
		
		try:																					#try to delete a Milestone 	
			self.__connect.send_post('delete_milestone/' + str(self.__milestones_dict[name]), {})	#by sending "POST" request "delete_run" to the TestRail API
		except APIError as error:																#except the case when method doesn't return "200 OK" response
			print (error)																		#print the response code in this case

	def delete_run(self, name:str):
		"""Public method that deletes the Run from the project instance."""
		
		try:																		#try to delete a run 	
			self.__connect.send_post('delete_run/' + str(self.__runs_dict[name]), {})	#by sending "POST" request "delete_run" to the TestRail API
		except APIError as error:													#except the case when method doesn't return "200 OK" response
			print (error)															#print the response code in this case

	def delete_section(self, name):
		"""Public method that deletes the Section from the project instance."""
		
		try:																				#try to delete a section
			self.__connect.send_post('delete_section/' + str(self._sections_dict[name]), {})	#by sending "POST" request "delete_section" to the TestRail API
		except APIError as error:															#except the case when method doesn't return "200 OK" response
			print (error)																	#print the response code in this case

	def delete_suite(self, name:str):
		"""Public method that deletes the Suite from the project instance."""
		
		try:																				#try to delete a suite
			self.__connect.send_post('delete_suite/' + str(self.__suites_dict[name]), {})		#by sending "POST" request "delete_suite" to the TestRail API
		except APIError as error:															#except the case when method doesn't return "200 OK" response
			print (error)																	#print the response code in this case

	def get_templates(self):
		"""Public method that returns the list of available templates for the project instance."""
		
		template_list = []																#create the temporaty list
		try:																			#try to get the list of available templates
			template_list = self.__connect.send_get('get_templates/' + str(self.id))		#by sending "GET" request "get_templates" to the TestRail API
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case
				
		return template_list															#return the temporary list

	def get_milestone(self, name):
		"""Public method that takes the name of the milestone as STRING and returns the Milestone object."""
		
		tmp_milestone = Milestone(self.__milestones_dict[name], self.__connect)		#find the milestone ID throught the name and call the Milestone class
		return tmp_milestone														#return the instance
		
	def get_sections_list(self, suite):
		"""Public method that takes a name of the suite as STRING and returns the list of the sections that are connected to the project instance."""
		
		self._sections_dict = self._get_sections_dict(suite)					#set the ._sections_dict attribute by calling the _get_sections_dict() method
		sections_list = list([item for item in self._sections_dict])			#iterate throught the ._sections_dict attribute and create the list from the keys
		return sections_list													#return sections list
		
	def get_run(self, name):
		"""Public method that takes the name of the run as STRING and returns the Run object."""
		
		tmp_run = Run(self.__runs_dict[name], self.__connect)					#find the run ID throught the name and call the Run class
		return tmp_run														#return the instance
		
	def get_section(self, name):
		"""Public method that takes the name of the section as STRING and returns the Section object."""
	
		tmp_section = Section(self._sections_dict[name], self.__connect)		#find the section ID throught the name and call the Section class
		return tmp_section													#return the instance

	def get_suite(self, name):
		"""Public method that takes the name of the suite as STRING and returns the Suite object."""
	
		if isinstance(name, str):						#check the type of "name" variable
			id = self.__suites_dict[name]				#if STRING then need to find the ID
		if isinstance(name, int):
			id = name									#if INTEGER the name is id
		
		tmp_suite = Suite(id, self.__connect)			#find the section ID throught the name and call the Section class
		return tmp_suite								#return the instance

	def update(
			self, 
			name: str,
			announce: str ='',
			show_announce: bool=True,
			is_completed: bool=False,
			suite_mode: int=0):
		"""Public method that updates the project instance. The method takes next arguments:
		
			name			-		The name of the project (required)						as		STRING
			announce		-		The description of the project							as		STRING
			show_announce		-		Flag that is responded for showing announcement				as		BOOLEAN
			is_completed		-		Specifies whether a project is considered completed or not		as		BOOLEAN
			suite_mode		-		The suite mode of the project							as		INTEGER
		"""
		
		properties_dict = {							#Fill the dictionary of new attributes for project 
			'name':name,
			'announcement':announce,
			'show_announcement':show_announce,
			'is_completed':is_completed,
			'suite_mode':suite_mode
			}
		try:																			#try to update a project
			self.__connect.send_post('update_project/' + str(self.id), properties_dict)	#by sending "POST" request "update_project" to the TestRail API
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case