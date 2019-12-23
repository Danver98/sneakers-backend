class Query:
    def __init__(self):
        self.query = {}
    
    def add_index(self, param):
        for index in param:
            if index == "size":
                sizes=[]

                for item in param[index].split(','):
                    sizes.append({index: int(item)})

                self.query["$or"] = sizes
            else:
                self.query[index] = param[index]

    def get_query(self):
        print(self.query)
        return self.query