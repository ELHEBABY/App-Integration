

class Settings():

    integrationAutomaticIsActive = True
    integrationFrequency = 'day'

    def __init__(self, i_var):
        self.i_var = i_var

    def setIntegrationAutomaticIsActive(self, var):
        self.integrationAutomaticIsActive = var
    
    def getIntegrationAutomaticIsActive(self):
        return self.integrationAutomaticIsActive

    def setintegrationFrequency(self, var):
        self.integrationFrequency=var
    
    def getintegrationFrequency(self):
        return self.integrationFrequency