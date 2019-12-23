class Query:
    def __init__(self):
        self.query = {}
    
    def add_index(self, param):
        for index in param:
            if index == "size":
                param_list = []
                
                for item in param[index].split('-'):
                    param_list.append({index: int(item)})

                self.query["$or"] = param_list
            elif index == "cost":
                self.query["cost"] = {"$gte": int(param[index]) - 1000, "$lte": int(param[index]) + 1000}
            else:
                self.query[index] = param[index]

    def get_query(self):
        return self.query