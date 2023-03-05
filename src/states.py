class StateGame:
    def __init__(self,**kwargs):
        self.is_dead = None
        self.is_paused = None
        self.is_snake_incrementing = None
        self.has_restarted = None
        self.change_values(**kwargs)
    
    def change_values(self,**kwargs):
        values = list(kwargs.values())
        keys = list(kwargs.keys())

        get_values = lambda x: values[keys.index(x)]

        for i in keys:
            if(i == "is_dead"):
                self.is_dead = get_values(i)
            elif(i == "is_paused"):
                self.is_paused = get_values(i)
            elif(i == "has_restarted"):
                self.has_restarted = get_values(i)
            elif(i == "is_snake_incrementing"):
                self.is_snake_incrementing = get_values(i)
        
    def ret_values(self,*args):    
        is_one_value = False
        if(len(args)==1):
            is_one_value = True

        out = []
        for i in args:
            if(i == "is_dead"):
                if(is_one_value):
                    return self.is_dead
                out.append(self.is_dead)
            elif(i == "is_paused"):
                if(is_one_value):
                    return self.is_paused
                out.append(self.is_paused)
            elif(i == "has_restarted"):
                if(is_one_value):
                    return self.has_restarted
                out.append(self.has_restarted)
            elif(i == "is_snake_incrementing"):
                if(is_one_value):
                    return self.is_snake_incrementing
                out.append(self.is_snake_incrementing)
            elif(i=="all"):
                return [self.is_dead,self.is_paused,self.has_restarted,self.is_snake_incrementing]
        return out
    
    def state(self):
        print("is dead:",self.ret_values("is_dead"),
        "\nis paused:",self.ret_values("is_paused"),
        "\nis snake incrementing:",self.ret_values("is_snake_incrementing"),
        "\nhas restarted:",self.ret_values("has_restarted")
        )

        print()
    
if(__name__=="__main__"):
    state = StateGame(is_dead=False,is_paused=True)
    state.state()
    state.change_values(is_dead=True,is_paused=True,hola="si")
    state.ret_values("is_dead")