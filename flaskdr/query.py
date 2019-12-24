class Query:
    def __init__(self):
        self.query = {}
        self.sort_list = []
    
    def add_index(self, param):
        for index in param:
            if index == "size":
                value_list = []
                
                for item in param[index].split('-'):
                    value_list.append({index: int(item)})

                self.query["$or"] = value_list
            elif index == "cost":
                self.query["cost"] = {"$gte": int(param[index]) - 1000, "$lte": int(param[index]) + 1000}
            elif index == "sort":
                value_list = param[index].split('-')
                param_key = value_list[0]
                param_value = value_list[1]
                if param_value == "up":
                    self.sort_list.append((param_key, 1))
                else:
                    self.sort_list.append((param_key, -1))
            else:
                self.query[index] = param[index]

    def get_query(self):
        return self.query

    def get_sort(self):
        print (self.sort_list)
        return self.sort_list