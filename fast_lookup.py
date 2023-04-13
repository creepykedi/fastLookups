from sqlalchemy.sql.expression import Select
import operator


class Lookup(Select):
    restricted = []

    def __init__(self, model, inst):
        self.model = model
        self.inst = inst
        self.field = None
        #self.transcribe = {'nerdstuff': 'price'}

    def __lt__(self, other):
        return self.inst.where(getattr(self.model, self.field) < other)

    def __gt__(self, other):
        return self.inst.where(getattr(self.model, self.field) > other)

    def __ge__(self, other):
        return self.inst.where(getattr(self.model, self.field) >= other)

    def __le__(self, other):
        return self.inst.where(getattr(self.model, self.field) <= other)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.inst.where(getattr(self.model, self.field).ilike(other))
        return self.inst.where(getattr(self.model, self.field) == other)

    def __ne__(self, other):
        return self.inst.where(getattr(self.model, self.field) != other)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def perform_lookup(self, field, operation, value):
        self.field = field
        if field not in list(self.model.__fields__):
            print('Something wrong dude')
            return Lookup(self.model, self.inst)
        print(field, self.restricted)
        if field in self.restricted:
            print("We don't do that here")
            return Lookup(self.model, self.inst)
        res = getattr(operator, operation)(self, value)
        response = Lookup(self.model, res)
        response.restricted = self.restricted
        return response

