class Stack(object):
    def __init__(self, region, name, template, parameters={}):
        self.region = region
        self.name = name
        self.template = template
        self.parameters = parameters

    def __repr__(self):
        return '<Stack {} ({})>'.format(self.name, self.region)

    def __eq__(self, other):
        return \
            self.region == other.region and \
            self.name == other.name and \
            self.template == other.template and \
            self.parameters == other.parameters
