class Valve:
    def __init__(
            self, 
            name, 
            is_open=False,
            opening_delay_steps=1,
            closing_delay_steps=1,
            ):
        self.name = name
        self.is_open = is_open

        # Actual state
        self.is_open = is_open

        # Command state
        self.commanded_open = is_open

        # Simple fault model
        self.stuck_closed = False

        # Delay settings
        self.opening_delay_steps = opening_delay_steps
        self.closing_delay_steps = closing_delay_steps

        # Internal counters
        self._transition_counter = 0

    def set_command(self, open_command: bool):
        if open_command != self.commanded_open:
            self.commanded_open = open_command
            self._transition_counter = 0
        
    def open(self):
        '''Convenience method: command valve is open.'''
        self.set_command(True)

    def close(self):
        '''Convenience method: command valve is closed'''
        self.set_command(False)

    def update(self):
        '''Update actual valve position based on command and fault status.'''
        if self.stuck_closed:
            self.is_open = False
            return
        
        # Already at commanded state
        if self.is_open == self.commanded_open:
            self._transition_counter = 0
            return
        
        self._transition_counter += 1

        if self.commanded_open:
            if self._transition_counter >= self.opening_delay_steps:
                self.is_open = True
                self._transition_counter = 0
        else:
            if self._transition_counter >= self.closing_delay_steps:
                self.is_open = False
                self._transition_counter = 0

    def get_status(self):
        return {
            'name': self.name,
            'commanded_open': self.commanded_open,
            'is_open': self.is_open,
            'stuck_closed': self.stuck_closed,
            'opening_delay_stops': self.opening_delay_steps,
            'closing_delay_stops': self.closing_delay_steps
        }