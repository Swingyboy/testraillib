class Milestone():
	def __init__(self, name: str, id: int, connect):
		self.id = id
		self.name = name
		self._connect = connect
		self.info = self._get_milestone_info()
		
	def _get_milestone_info(self):
		tmp_dict = {}
		try:
			tmp_dict = self._connect.send_get('get_milestone/' + str(self.id))
		except APIError as error:
			print (error)
		
		return tmp_dict
	
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
				
		properties_dict = {
			'name':new_name,
			'description':description,
			'due_on':due_on,
			'parent_id':parent_id,
			'start_on':start_on,
			'is_completed':is_completed,
			'is_started':is_started
			}
		try:	
			self._connect.send_post('update_milestone/' + str(self.id), properties_dict)
		except APIError as error:
			print (error)
		
