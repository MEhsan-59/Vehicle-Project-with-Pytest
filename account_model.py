#account_model.py
class Model:
	def __init__(self, id, user_id, password, created_at, balance):
		self.id = id
		self.user_id = user_id
		self.password = password
		self.created_at = created_at
		self.balance = balance
