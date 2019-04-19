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
		self.__milestones_dict = self.__get_milestones_dict()
		self.childms = list(key for key in  self.__milestones_dict)
		
	def __get_milestone_info(self):
		"""Private method that returns dictionary with the properties of the mailstone instance."""
		tmp_dict = {}															#create a temporary dict
		try:																	#try to get the list of milestone attributes
			tmp_dict = self.__connect.send_get('get_milestone/' + str(self.id))	#by sending "GET" request "get_milestone" to the TestRail API
		except APIError as error:												#except the case when method doesn't return "200 OK" response
			print (error)														#print the response code in this case
		
		return tmp_dict															#return the temporary dict
		
	def __get_milestones_dict(self):
		tmp_dict ={}
		for milest in self.info['milestones']:
			tmp_dict.update({milest['name']:milest['id']})
		return tmp_dict

	def add_childms(
			self, 
			name: str,
			description: str,
			due_on: str,
			start_on: str
			):
		"""Public method that adds the Milestone to the project instance. The method takes next arguments:
		
			name			-	The name of the milestone (required)				as	STRING
			description		-	The description of the milestone				as	STRING
			due_on			-	The due date of the milestone (as UNIX timestamp) 	as 	STRING (should be TIMESTAMP)
			start_on		-	The scheduled start date of the milestone			as	STRING (should be TIMESTAMP)
		"""
		properties_dict = {						#Fill the dictionary of new milestone attributes 
			'name':name,
			'description':description,
			'due_on':due_on,
			'parent_id':self.info['id'],
			'start_on':start_on
			}
		try:																						#try to create a new milestone
			response = self.__connect.send_post('add_milestone/' + str(self.info['project_id']), properties_dict)	#by sending "POST" request "add_milestone" to the TestRail API
			self.__milestones_dict.update({response['name']:response['id']})
			self.childms.append(response['name'])
			print('Milestone ' + name +' was added!')
			return Milestone(response['id'], self.__connect)
		except APIError as error:														#except the case when method doesn't return "200 OK" response
			print (error)																#print the response code in this case
			return None
		
	def delete_childms(self, name):
		"""Public method that deletes the Milestone from the project instance."""
		try:																						#try to delete a Milestone
			self.__connect.send_post('delete_milestone/' + str(self.__milestones_dict[name]), {})	#by sending "POST" request "delete_run" to the TestRail API
			del self.__milestones_dict[name]
			self.childms.remove(name)
			print('Milestone ' + name +' was deleted!')
		except APIError as error:																#except the case when method doesn't return "200 OK" response
			print (error)																		#print the response code in this case
		except KeyError:
			print('There is no such milestone!')	
		return None
		
	def get_childms(self, name):
		"""Public method that takes the name of the milestone as STRING and returns the Milestone object."""
		try:
			return Milestone(self.__milestones_dict[name], self.__connect)		#find the milestone ID throught the name and return the Milestone instance
		except KeyError:
			print('There is no such milestone!')
			return None

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
		try:																							#try to update a milestone 
			response = self.__connect.send_post('update_milestone/' + str(self.id), properties_dict)	#by sending "POST" request "update_milestone" to the TestRail API
			self.info = self.__get_milestone_info()
			return response
		except APIError as error:															#except the case when method doesn't return "200 OK" response
			print (error)																	#print the response code in this case
			return None