from testrail import APIError


class Case():
	
	def __init__(self, name: str, id: int, connect):
		self.id = id
		self.name = name
		self._connect = connect
		self.info = self._get_case_info()
		
	def _get_case_info(self):
		tmp_dict = {}
		try:
			tmp_dict = self._connect.send_get('get_case/' + str(self.id))
		except APIError as error:
			print (error)
		
		return tmp_dict
		
	def update(
			self, title: str,
			template_id: int,
			type_id: int,
			priority_id: int,
			estimate: str,
			milestone_id: int,
			refs: str
			):
		
		properties_dict = {
			'title':title,
			'template_id':template_id,
			'type_id':type_id,
			'priority_id':priority_id,
			'estimate':estimate,
			'milestone_id':milestone_id,
			'milestone_id':milestone_id,
			'refs':refs
			}
		try:	
			self._connect.send_post('update_case/' + str(self.id), properties_dict)
		except APIError as error:
			print (error)



class Section():
	
	def __init__(self, name: str, id: int, connect):
		self.id = id
		self.name = name
		self._connect = connect
		self.info = self._get_case_info()
		
	def _get_case_info(self):
		tmp_dict = {}
		try:
			tmp_dict = self._connect.send_get('get_section/' + str(self.id))
		except APIError as error:
			print (error)
		
		return tmp_dict
		
	def update(
			self,
			descr: str,
			name: str
			):
		
		properties_dict = {
			'description':descr,
			'name':name
			}
		try:	
			self._connect.send_post('update_section/' + str(self.id), properties_dict)
		except APIError as error:
			print (error)
			
class Suite():
	
	def __init__(self, name: str, id: int, connect):
		self.id = id
		self.name = name
		self._connect = connect
		self.info = self._get_suite_info()
		self._cases_dict = self._get_cases_dict()
		self.cases = self._get_cases_list()
		
	def _get_suite_info(self):
		tmp_dict = {}
		try:
			tmp_dict = self._connect.send_get('get_suite/' + str(self.id))
		except APIError as error:
			print (error)
		
		return tmp_dict
		
	def _get_cases_dict(self):
		tmp_list = []
		try:
			tmp_list = self._connect.send_get('get_cases/' + str(self.info['project_id']) + '&suite_id=' + str(self.id))
		except APIError as error:
			print (error)
		tmp_cases_dict = dict([(item['title'], item['id']) for item in tmp_list])
			
		return tmp_cases_dict	
		
	def _get_cases_list(self):
		cases_list = list([item for item in self._cases_dict])
		return cases_list
		
	def update(
			self, suite_id: int,
			new_name: str,
			description: str,
			milestone_id: int,
			assignedto_id: int,
			include_all: bool,
			case_ids: list
			):
				
		properties_dict = {
			'suite_id':suite_id,
			'name':new_name,
			'description':description,
			'milestone_id':milestone_id,
			'assignedto_id':assignedto_id,
			'include_all':include_all,
			'case_ids':case_ids
			}
		try:	
			self._connect.send_post('update_suite/' + str(self.id), properties_dict)
		except APIError as error:
			print (error)
	
	def get_case(self, name):
		tmp_case = Case(name, self._cases_dict[name], self._connect)
		return tmp_case	

	def delete_case(self, name):
		try:	
			self._connect.send_post('delete_case/' + str(self._cases_dict[name]), {})
		except APIError as error:
			print (error)
			
