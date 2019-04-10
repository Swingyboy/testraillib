from testrail import APIError
from items.suite import Suite


class Test():
	"""The Test class that create Test instance.
	
	This class takes the next arguments:
		id		-	The ID of the test in the TestRail.
		connect		-	The connect instance that is APIClient object.
	
	The class has the next attributes:
		__connect	- 	Private attribute that contains the connection and is used for transfering the connection
					to another elements of the TestRail.
		id		-	Public attribute that contains the ID of the test.
		info		-	Public attribute that contains the dictionary with the properties of the test instance.
	
	The class has the next methods:
		__init__()		-	The class constructor accepts the ID of the test and the connect instance.
		__get_test_info		-	Private method that returns dictionary with the properties of the test instance.
						This method is used for initialisation the .info attribute.
		add_result		-	Public method that adds result to the test instance the TestRail.
		get_results		-	Public method that return the results list of the tests instance.
	"""

	def __init__(self, id: int, connect):
		"""The class constructor accepts the ID of the test and APIClient object as connect instance"""
		
		self.id = id						#set the id attribute
		self.__connect = connect				#set the connect attribute
		self.info = self.__get_test_info()	#set the info attribute by calling the __get_test_info() method

	def __get_test_info(self):
		"""Private method that returns dictionary with the properties of the test instance."""
		
		tmp_dict = {}														#create a temporary dict
		try:																#try to get the list of test attributes
			tmp_dict = self.__connect.send_get('get_test/' + str(self.id))	#by sending "GET" request "get_test" to the TestRail API
		except APIError as error:											#except the case when method doesn't return "200 OK" response
			print (error)													#print the response code in this case
		
		return tmp_dict														#return the temporary dictionary
		
	def add_result(self,
			status_id: int,
			comment: str,
			version: str,
			elapsed: str,
			defects: str,
			assignedto_id: int
			):
		"""Public method that adds result to the test instance the TestRail. The method takes next arguments:
		
		status_id	-	The ID of the test status. You can get a full list of system and custom statuses via get_statuses.			as	INTEGER
					The built-in system statuses have the following IDs: 1 - Passed, 2 - Blocked, 3 - Untested, 4 - Retest, 5 - Failed.
		comment		-	The comment / description for the test result											as	STRING
		version		-	The version or build you tested against												as	STRING
		elapsed		-	The time it took to execute the test												as	STRING (should be TIMESPAN)
		defects		-	A comma-separated list of defects to link to the test result								as	STRING
		assignedto_id	-	The ID of a user the test should be assigned to											as	INTEGER
		"""
				
		properties_dict = {							#Fill the dictionary of result attributes 
			'status_id':status_id,
			'comment':comment,
			'version':version,
			'elapsed':elapsed,
			'defects':defects,
			'assignedto_id':assignedto_id
			}
			
		try:																		#try to add a result
			self.__connect.send_post('add_result/' + str(self.id), properties_dict)	#by sending "POST" request "add_result" to the TestRail API
		except APIError as error:													#except the case when method doesn't return "200 OK" response
			print (error)															#print the response code in this case
		
		
	def get_results(self):
		"""Public method that return the results list of the tests instance."""
		
		temp_results_list = []															#create a temporary list
		try:																			#try to get the results list
			temp_results_list = self.__connect.send_get('get_results/' + str(self.id))	#by sending "GET" request "get_results" to the TestRail API
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case
			
		return temp_results_list														#return the temporary list
		
class Run():
	"""The Run class that create Run instance.
	
	This class takes the next arguments:
		id		-	The ID of the run in the TestRail.
		connect		-	The connect instance that is APIClient object.
	
	The class has the next attributes:
	`	__connect		- 	Private attribute that contains the connection and is used for transfering the connection
						to another elements of the TestRail.
		__tests_dict		- 	Private attribute that contains the dictionary of the "Test_name":"Test_id" pairs.
						This attribute is necessary because TestRail API v.2 uses the ID of elements, but usually
						the user knows only the names, and not these IDs.
		id			-	Public attribute that contains the ID of the run.
		info			-	Public attribute that contains the dictionary with the properties of the run instance.
		tests			-	Public attribute that contains the list of the tests these are present in the run instance.
		
	The class has the next methods:
		__init__()				-	The class constructor accepts the ID of the run and the connect instance.
		__get_run_info()			-	Private method that returns dictionary with the properties of the run instance.
								This method is used for initialisation the .info attribute.
		__get_tests_dict()			-	Private method that returns the dictionary of the "Test_name":"Test_id" pairs
								or prints the error message if the APIClient object doesn't return the "200 OK" code. 
								The method is used for initialisation the .__tests_dict attribute.
		__get_tests_list()			-	Private method that returns the list of the test names these are contained in the run instance. 
								This method is used for filling the .tests attribute.
		add_result_for_case()			-	Public method that adds a new test result, comment or assigns a test (for a test run and case combination).
								For more information see http://docs.gurock.com/testrail-api2/reference-results
		add_results_for_cases()			-	Public method that takes the list of the results and adds one or more new test results, comments or assigns one or more tests.
								The difference to add_results_for_tests() is that this method expects test case IDs instead of test IDs in the list of results.
								For more information see http://docs.gurock.com/testrail-api2/reference-results
		add_results_for_tests()			-	Public method that takes the list od the results and adds one or more new test results, comments or assigns one or more tests.
								For more information see http://docs.gurock.com/testrail-api2/reference-results
		close_run()				-	Public method that closes a current run instance and archives its tests & results.
		get_results()				-	Public method that returns a list of test results for a run instance.
		get_results_for_case()			-	Public method that returns a list of test results for a run instance and case combination.
		get_suite()				-	Public method that returns a Suite object connected to current run.
		get_test()				-	Public method that returns a Test object.
		update()				-	Public method that updates the run instance.						
	"""
	
	def __init__(self, id: int, connect):
		"""The class constructor accepts the ID of the run and the connect instance."""
		
		self.id = id									#set the id attribute
		self.__connect = connect						#set the connect attribute 
		self.info = self.__get_run_info()				#set the info attribute by calling the __get_run_info() method
		self.__tests_dict = self.__get_tests_dict()		#set the __tests_dict attribute by calling the __get_tests_dict() method
		self.tests = self.__get_tests_list()			#set the .tests attribute by calling the __get_tests_list() method
		
	def __get_run_info(self):
		"""Private method that returns dictionary with the properties of the run instance.
		This method is used for initialisation the .info attribute.
		"""
		
		tmp_dict = {}														#create a temporary dict
		try:																#try to get the list of run attributes
			tmp_dict = self.__connect.send_get('get_run/' + str(self.id))	#by sending "GET" request "get_run" to the TestRail API
		except APIError as error:											#except the case when method doesn't return "200 OK" response
			print (error)													#print the response code in this case
		
		return tmp_dict														#return the temporary dict
		
	def __get_tests_dict(self):
		"""Private method that returns the dictionary of the "Test_name":"Test_id" pairs
		or prints the error message if the APIClient object doesn't return the "200 OK" code.
		The method is used for initialisation the .___tests_dict attribute.
		"""
		try:																		#try to get the list of tests with its attributes
			tmp_list = self.__connect.send_get('get_tests/' + str(self.id))			#by sending "GET" request "get_tests" to the TestRail API
		except APIError as error:													#except the case when method doesn't return "200 OK" response
			print (error)															#print the response code in this case
			
		tmp__tests_dict = dict([(item['title'], item['id']) for item in tmp_list])	#create the temporary dictionary of the "Test_name":"Test_id" pairs
		return tmp__tests_dict														#return the temporary dictionary
		
	def __get_tests_list(self):
		"""Private method that returns the list of the test names these are contained in the run instance. 
		This method is used for filling the .tests attribute.
		"""
		tests_list = list([item for item in self.__tests_dict])		#iterate the __tests_dict and create the temporary list from the keys
		return tests_list											#return the temporary list

	def add_result_for_case(self,
			case_id,
			status_id: int,
			comment: str,
			version: str,
			elapsed: str,
			defects: str,
			assignedto_id: int
			):
		"""Public method that adds a new test result, comment or assigns a test (for a test run and case combination).
		For more information see http://docs.gurock.com/testrail-api2/reference-results.
		The method takes next arguments:
		
		case_id			-	ID of the case to which the results will be added										as	INTEGER
		status_id		-	The ID of the test status. You can get a full list of system and custom statuses via get_statuses.			as	INTEGER
						The built-in system statuses have the following IDs: 1 - Passed, 2 - Blocked, 3 - Untested, 4 - Retest, 5 - Failed.
		comment			-	The comment / description for the test result											as	STRING
		version			-	The version or build you tested against												as	STRING
		elapsed			-	The time it took to execute the test												as	STRING (should be TIMESPAN)
		defects			-	A comma-separated list of defects to link to the test result								as	STRING
		assignedto_id		-	The ID of a user the test should be assigned to											as	INTEGER
		"""
		
		properties_dict = {											#fill the dictionary of new suite attributes 
			'status_id':status_id,
			'comment':comment,
			'version':version,
			'elapsed':elapsed,
			'defects':defects,
			'assignedto_id':assignedto_id
			}
			
		try:																										#try to add a new result
			self.__connect.send_post('add_result_for_case/' + str(self.id) +'/' + str(case_id), properties_dict)		#by sending "POST" request "add_result_for_case" to the TestRail API
		except APIError as error:																					#except the case when method doesn't return "200 OK" response
			print (error)																							#print the response code in this case
		
	def add_results_for_cases(self, results_list:list):
		"""Public method that takes the list of the results and adds one or more new test results, comments or assigns one or more tests.
		The difference to add_results_for_tests() is that this method expects test case IDs instead of test IDs in the list of results.
		For more information see http://docs.gurock.com/testrail-api2/reference-results.
		The method takes next arguments:
		
		results_list - The list of the results in format [{result 1 atributes},{result 2 atributes},... ,{result n atributes}]
		"""
		try:																									#try to add the new results
			self.__connect.send_post('add_results_for_cases/' + str(self.id), dict("results", results_list))		#by sending "POST" request "add_results_for_cases" to the TestRail API
		except APIError as error:																				#except the case when method doesn't return "200 OK" response
			print (error)																						#print the response code in this case
			
	def add_results_for_tests(self, results_list:list):
		"""Public method that takes the list of the results and adds one or more new test results, comments or assigns one or more tests.
		For more information see http://docs.gurock.com/testrail-api2/reference-results.
		The method takes next arguments:
		
		results_list - The list of the results in format [{result 1 atributes},{result 2 atributes},... ,{result n atributes}]	as	LIST
		"""
		try:																						#try to add the new results
			self.__connect.send_post('add_results/' + str(self.id), dict("results", results_list))	#by sending "POST" request "add_results" to the TestRail API
		except APIError as error:																	#except the case when method doesn't return "200 OK" response
			print (error)																			#print the response code in this case
		
	def close_run(self):
		"""Public method that closes a current run instance and archives its tests & results."""
		
		try:															#try to close a run
			self.__connect.send_post('close_run/' + str(self.id), {})	#by sending "POST" request "close_run" to the TestRail API
		except APIError as error:										#except the case when method doesn't return "200 OK" response
			print (error)												#print the response code in this case
			
	def get_results(self):
		"""Public method that returns a list of test results for a run instance."""
		
		temp_results_list = []																	#create a temporary list
		try:																					#try to get a list of results
			temp_results_list = self.__connect.send_get('get_results_for_run/' + str(self.id))	#by sending "GET" request "get_results_for_run" to the TestRail API
		except APIError as error:																#except the case when method doesn't return "200 OK" response
			print (error)																		#print the response code in this case
			
		return temp_results_list																#return the temporary list
		
	def get_results_for_case(self, case_id):
		"""Public method that returns a list of test results for a run instance and case combination.
		The method takes next arguments:
		
		case_id	-	ID of the case (the case must be a part of the suite of the current run)	as	INTEGER
		"""
		
		temp_results_list = []																						#create a temporary list
		try:																										#try to get a list of results
			temp_results_list = self.__connect.send_get('get_results_for_case/' + str(self.id) +'/' + str(case_id))	#by sending "GET" request "get_results_for_run" to the TestRail API
		except APIError as error:																					#except the case when method doesn't return "200 OK" response
			print (error)																							#print the response code in this case
			
		return temp_results_list																					#return the temporary list
			
	def get_suite(self):
		"""Public method that returns a Suite object that connected to current run."""
		
		return Suite(self.info['suite_id'], self.__connect)	#take suite ID from the .info atribute and create a Suite instance from it
			
	def get_test(self, name):
		"""Public method that returns a Test object. The method takes next arguments:
		
		name	-	Name of the test	as	STRING
		"""
		return Test(self.__tests_dict[name], self.__connect) 

	def update(
			self,
			suite_id: int,
			new_name: str,
			description: str,
			milestone_id: int,
			assignedto_id: int,
			include_all: bool,
			case_ids: list
			):
		"""Public method that updates the run instance. The method takes next arguments:
		
		suite_id	-	The ID of the test suite for the test run (optional if the project is operating in single suite mode, required otherwise)	as	INTEGER
		name		-	The name of the test run														as	STRING
		description	-	The description of the test run														as	STRING
		milestone_id	-	The ID of the milestone to link to the test run												as	INTEGER
		assignedto_id	-	The ID of the user the test run should be assigned to											as	INTEGER
		include_all	-	Flag that is responded for including all test cases of the test suite								as	BOOLEAN
		case_ids	-	An array of case IDs for the custom case selection											as	ARRAY
		"""
				
		properties_dict = {												#Fill the dictionary of new run attributes
			'suite_id':suite_id,
			'name':new_name,
			'description':description,
			'milestone_id':milestone_id,
			'assignedto_id':assignedto_id,
			'include_all':include_all,
			'case_ids':case_ids
			}
		try:																		#try to update a run 
			self.__connect.send_post('update_run/' + str(self.id), properties_dict)	#by sending "POST" request "update_run" to the TestRail API
		except APIError as error:													#except the case when method doesn't return "200 OK" response
			print (error)															#print the response code in this case