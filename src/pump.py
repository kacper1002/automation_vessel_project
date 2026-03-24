class Pump:
    def __init__(
            self, 
            name, 
            flow_rate, 
            is_running=False,
            start_delay_steps = 1,
            stop_delay_steps = 0,
            ):
        """
        flow_rate: transfer rate m3/s
        """
        self.name = name
        self.flow_rate = flow_rate
        
        # Actual state
        self.is_running = is_running

        # Commanded state
        self.commanded_on = is_running

        # Fault model
        self.failed_to_start = False

        # Delay settings
        self.start_delay_steps = start_delay_steps
        self.stop_delay_steps = stop_delay_steps

        # Internal counter
        self._transition_counter = 0

    def set_command(self, on_command: bool):
        if on_command != self.commanded_on:
            self.commanded_on = on_command
            self._transition_counter = 0 
    
    def start(self):
        self.set_command(True)

    def stop(self):
        self.set_command(False)

    def update(self):
        '''
        Update actual pump running state based on command, fault and delay
        '''
        if self.failed_to_start and self.commanded_on:
            self.is_running = False
            return
        
        if self.is_running == self.commanded_on:
            self._transition_counter = 0
            return
        
        self._transition_counter += 1

        if self.commanded_on:
            if self._transition_counter >= self.start_delay_steps:
                self.is_running = True
                self._transition_counter = 0
        else:
            if self._transition_counter >= self.stop_delay_steps:
                self.is_running = False
                self._transition_counter = 0

    def get_flow(self):
        return self.flow_rate if self.is_running else 0.0
    
    def get_status(self):
        return{
            'name': self.name,
            'commanded_on': self.commanded_on,
            'is_running': self.is_running,
            'failed_to_start': self.failed_to_start,
            'start_delay_steps': self.start_delay_steps,
            'stop_delay_steps': self.stop_delay_steps
        }