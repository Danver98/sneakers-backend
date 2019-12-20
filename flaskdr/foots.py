class FootList:
    def __init__(self):
        self.foot_list = []

    def add_foot(self, foot):
        self.foot_list.append(foot)
    
    def get_all(self):
        return self.foot_list