from testrail import APIError


class Case():
	"""The Case class that create Case instance.
	
	This class takes the next arguments:
		id		-	The ID of the case in the TestRail.
		connect		-	The connect instance that is APIClient object.
	
	The class has the next attributes:
	`	__connect	- 	Private attribute that contains the connection and is used for transfering the connection
					to another elements of the TestRail.
		id		-	Public attribute that contains the ID of the case.
		info		-	Public attribute that contains the dictionary with the properties of the case instance.
		
	The class has the next methods:
		__init__()		-	The class constructor accepts the ID of the case and the connect instance.
		__get_case_info		-	Private method that returns dictionary with the properties of the case instance.
						This method is used for initialisation the .info attribute.
		update			-	Public method that updates the case instance.
	"""
	
	def __init__(self, id: int, connect):
		"""The class constructor accepts the ID of the case and APIClient object as connect instance."""
		self.id = id						#set the id attribute
		self.__connect = connect				#set the connect attribute
		self.info = self.__get_case_info()	#set the info attribute by calling the _get_case_info() method
		
	def __get_case_info(self):
		"""Private method that returns dictionary with the properties of the case instance."""
		tmp_dict = {}														#create a temporary dict
		try:																#try to get the list of case attributes
			tmp_dict = self.__connect.send_get('get_case/' + str(self.id))	#by sending "GET" request "get_case" to the TestRail API
		except APIError as error:											#except the case when method doesn't return "200 OK" response
			print (error)													#print the response code in this case
		return tmp_dict														#return the temporary dictionary
		
	def update(
			self,
			title: str,
			template_id: int,
			type_id: int,
			priority_id: int,
			estimate: str,
			milestone_id: int,
			refs: str
			):
		"""Public method that updates the case instance. The method takes next arguments:
		title			-	The title of the test case (required)			as	STRING
		template_id		-	The ID of the template (field layout)			as	INTEGER
		type_id			-	The ID of the case type					as	INTEGER
		priority_id		-	The ID of the case priority				as	INTEGER
		estimate		-	The estimate						as	STRING (should be TIMESPAN)
		milestone_id		-	The ID of the milestone to link to the test case	as	INTEGER
		refs			-	A comma-separated list of references/requirements	as	STRING
		"""
		properties_dict = {					#Fill the dictionary of new attributes for case 
			'title':title,
			'template_id':template_id,
			'type_id':type_id,
			'priority_id':priority_id,
			'estimate':estimate,
			'milestone_id':milestone_id,
			'milestone_id':milestone_id,
			'refs':refs
			}
		try:																						#try to update a case
			response = self.__connect.send_post('update_case/' + str(self.id), properties_dict)		#by sending "POST" request "update_case" to the TestRail API
			self.info = self.__get_case_info()
			return response
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case
			return None



class Section():
	"""The Section class that create Section instance.
	
	This class takes the next arguments:
		id		-	The ID of the section in the TestRail.
		connect		-	The connect instance that is APIClient object.
	The class has the next attributes:
	`	__connect	- 	Private attribute that contains the connection and is used for transfering the connection
					to another elements of the TestRail.
		id		-	Public attribute that contains the ID of the section.
		info		-	Public attribute that contains the dictionary with the properties of the section instance.
		
	The class has the next methods:
		__init__()		-	The class constructor accepts the ID of the section and the connect instance.
		__get_case_info		-	Private method that returns dictionary with the properties of the section instance.
						This method is used for initialisation the .info attribute.
		update			-	Public method that updates the section instance.
	"""
	
	def __init__(self, id: int, connect):
		"""The class constructor accepts the ID of the section and APIClient object as connect instance."""
		
		self.id = id							#set the id attribute
		self.__connect = connect				#set the connect attribute
		self.info = self.__get_section_info()	#set the info attribute by calling the __get_section_info() method
		
	def __get_section_info(self):
		"""Private method that returns dictionary with the properties of the section instance."""
		tmp_dict = {}															#create a temporary dict
		try:																	#try to get the list of section attributes
			tmp_dict = self.__connect.send_get('get_section/' + str(self.id))	#by sending "GET" request "get_section" to the TestRail API
		except APIError as error:												#except the case when method doesn't return "200 OK" response
			print (error)														#print the response code in this case
		return tmp_dict															#return the temporary dictionary
		
	def update(
			self,
			descr: str,
			name: str
			):
		"""Public method that updates the section instance. The method takes next arguments:
		description		-	The description of the section		as	STRING
		name			-	The name of the section			as	STRING
		"""
		properties_dict = {							#Fill the dictionary of new attributes for section 
			'description':descr,
			'name':name
			}
		try:																				#try to update a section
			response = self.__connect.send_post('update_section/' + str(self.id), properties_dict)		#by sending "POST" request "update_section" to the TestRail API
			self.info = self.__get_section_info()
			return response
		except APIError as error:															#except the case when method doesn't return "200 OK" response
			print (error)																	#print the response code in this case
			return None
			
class Suite():
	"""The Section class that create Section instance.
	
	This class takes the next arguments:
		id		-	The ID of the suite in the TestRail.
		connect		-	The connect instance that is APIClient object.
		
	The class has the next attributes:
	`	__connect		-	Private attribute that contains the connection and is used for transfering the connection
						to another elements of the TestRail.
		__cases_dict		-	Private attribute that contains the dictionary of the "Case_name":"Case_id" pairs.
						This attribute is necessary because TestRail API v.2 uses the ID of elements, but usually
						the user knows only the names, and not these IDs.
		cases			-	Public attribute that contains the list of the cases these are present in the suite instance.
		id			-	Public attribute that contains the ID of the suite.
		info			-	Public attribute that contains the dictionary with the properties of the suite instance.
		
		The class has the next methods:
		__init__()				-	The class constructor accepts the ID of the suite and the connect instance.
		__get_cases_dict()			-	Private method that returns the dictionary of the "Case_name":"Case_id" pairs or prints the
								error message if the APIClient object doesn't return the "200 OK" code. 
								The method is used for initialisation the .__cases_dict attribute.
		_get_cases_list()			-	Private method that returns the list of the cases names these are contained in the suite instance. 
								This method is used for filling the .cases attribute.
		__get_suite_info()			-	Private method that returns dictionary with the properties of the suite instance.
								This method is used for initialisation the .info attribute.
		get_case()				-	Public method that returns the Case object.
		delete_case()				-	Public method that deletes the Case object.
		update()				-	Public method that updates the case instance.
	"""
	
	def __init__(self, id: int, connect):
		"""The class constructor accepts the ID of the suite and APIClient object as connect instance."""
		self.id = id								#set the id attribute
		self.__connect = connect						#set the connect attribute 
		self.info = self.__get_suite_info()			#set the info attribute by calling the __get_suite_info() method
		self._cases_dict = self.__get_cases_dict()	#set the _cases_dict attribute by calling the __get_cases_dict() method
		self.cases = self._get_cases_list()			#set the .cases attribute by calling the _get_cases_list() method
		
	def __get_cases_dict(self):
		"""Private method that returns the dictionary of the "Case_name":"Case_id" pairs 
		or prints the error message if the APIClient object doesn't return the "200 OK" code
		"""
		tmp_list = []																										#create a temporary list
		try:																												#try to get the list of suite cases with its attributes
			tmp_list = self.__connect.send_get('get_cases/' + str(self.info['project_id']) + '&suite_id=' + str(self.id))	#by sending "GET" request "get_cases" to the TestRail API
		except APIError as error:																							#except the case when method doesn't return "200 OK" response
			print (error)																									#print the response code in this case
		return dict([(item['title'], item['id']) for item in tmp_list])		#create the temporary dictionary of the "Case_name":"Case_id" pairs and return it
		
	def _get_cases_list(self):
		"""Private method that returns the list of the cases names these are contained in the suite instance."""
		return list([item for item in self._cases_dict])			#iterate the _cases_dict, create and return the temporary list
		
	def __get_suite_info(self):
		"""Private method that returns dictionary with the properties of the suite instance."""
		tmp_dict = {}															#create a temporary dict
		try:																	#try to get the list of suite attributes
			tmp_dict = self.__connect.send_get('get_suite/' + str(self.id))		#by sending "GET" request "get_suite" to the TestRail API
		except APIError as error:												#except the case when method doesn't return "200 OK" response
			print (error)														#print the response code in this case
		return tmp_dict															#return the temporary dict

	def delete_case(self, name:str):
		"""Public method that deletes the Case from the suite instance."""
		try:																			#try to delete a suite
			self.__connect.send_post('delete_case/' + str(self._cases_dict[name]), {})	#by sending "POST" request "delete_case" to the TestRail API
			del self._cases_dict[name]
			self.cases.remove(name)
			print('Case ' + name +' was deleted!')	
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case
		except KeyError:
			print('There is no such case!')		
		return None
		
	def get_case(self, name):
		""""Public method that takes the name of the case as STRING and returns the Case object."""
		try:
			return Case(self._cases_dict[name], self.__connect)		#find the case ID throught the name and return the Class instance
		except KeyError:
			print('There is no such case!')
			return None
			
	def update(
			self,
			new_name: str,
			description: str,
			):
		"""Public method that updates the suite instance. The method takes next arguments:
		
		name		-		The name of the test suite (required)		as	STRING
		description	-		The description of the test suite		as	STRING
		"""
		properties_dict = {								#fill the dictionary of new suite attributes 
			'name':new_name,
			'description':description,
			}
		try:																						#try to create a new section
			response = self.__connect.send_post('update_suite/' + str(self.id), properties_dict)	#by sending "POST" request "update_suite" to the TestRail API
			self.info = self.__get_suite_info()
			return response	
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case
			return None