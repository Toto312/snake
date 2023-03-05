class StateGame:
    def __init__(self,is_dead,is_paused):
        self.is_dead = is_dead
        self.is_paused = is_paused
        self.has_restarted = False

    def change_values(self,is_dead,is_paused):
        self.is_dead = is_dead
        self.is_paused = is_paused
    def change_restarted(self,has_restarted):
        self.has_restarted = has_restarted
    def ret_values(self):
        return [self.is_dead,self.is_paused]
    def ret_isDead(self):
        return self.is_dead
    def ret_isPaused(self):
        return self.is_paused
    def ret_hasRestarted(self):
        return self.has_restarted