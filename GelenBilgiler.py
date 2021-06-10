

class GelenBilgiler:
    data = []

    def __init__(self):
        self.data = []
        self.tasks = [
            {
                'id': 1,
                'title': u'Buy groceries',
                'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
                'done': False
            },
            {
                'id': 2,
                'title': u'Learn Python',
                'description': u'Need to find a good Python tutorial on the web',
                'done': False
            }
            ]


    def tasklariVer(self):
        return self.tasks



