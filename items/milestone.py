from testrail import APIError


class Milestone():
	"""The Mailstone class that create Mailstone instance.
	
	This class takes the next arguments:
		id		-	The ID of the mailestone in the TestRail.
		connect		-	The connect instance that is APIClient object.
	
	The class has the next attributes:
	`	__connect		- 	Private attribute that contains the connection and is used for transfering the connection
						to another elements of the TestRail.
		id			-	Public attribute that contains the ID of the mailestone.
		info			-	Public attribute that contains the dictionary with the properties of the mailestone instance.
		
	The class has the next methods:
		__init__()				-	The class constructor accepts the ID of the mailstone and the connect instance.
		__get_milestone_info()			-	Private method that returns dictionary with the properties of the mailstone instance.
								This method is used for initialisation the .info attribute.
		update()				-	Public method that updates the mailestone instance.
	"""
	
	def __init__(self, id: int, connect):
		"""The class constructor accepts the ID of the mailstone and the connect instance."""
		
		self.id = id							#set the id attribute
		self.__connect = connect					#set the connect attribute 
		self.info = self.__get_milestone_info()	#set the info attribute by calling the __get_milestone_info() method
		
	def __get_milestone_info(self):
		"""Private method that returns dictionary with the properties of the mailstone instance."""
	
		tmp_dict = {}															#create a temporary dict
		try:																	#try to get the list of milestone attributes
			tmp_dict = self.__connect.send_get('get_milestone/' + str(self.id))	#by sending "GET" request "get_milestone" to the TestRail API
		except APIError as error:												#except the case when method doesn't return "200 OK" response
			print (error)														#print the response code in this case
		
		return tmp_dict															#return the temporary dict
	
	def update(
			self,
			new_name: str,
			description: str,
			due_on: int,
			parent_id: int,
			start_on: int,
			is_completed: bool,
			is_started: bool
			):
		"""Public method that updates the mailestone instance. The method takes next arguments:
		
		new_name	-	A new name of the milestone					as	STRING
		description	-	The description of the milestone				as	STRING
		due_on		-	The due date of the milestone					as	INTEGER (should be TIMESTAMP)
		parent_id	-	The ID of the parent milestone, if any				as	INTEGER
		start_on	-	The scheduled start date of the milestone			as	INTEGER	(should be TIMESTAMP)
		is_completed	-	Flag that marks whether the milestone is completed or not	as	BOOLEAN
		is_started	-	Flag that marks whether the milestone is started or not		as	BOOLEAN
		"""
				
		properties_dict = {											#Fill the dictionary of new milestone attributes
			'name':new_name,
			'description':description,
			'due_on':due_on,
			'parent_id':parent_id,
			'start_on':start_on,
			'is_completed':is_completed,
			'is_started':is_started
			}
		try:																				#try to update a milestone 
			self.__connect.send_post('update_milestone/' + str(self.id), properties_dict)	#by sending "POST" request "update_milestone" to the TestRail API
		except APIError as error:															#except the case when method doesn't return "200 OK" response
			print (error)																	#print the response code in this case
		
