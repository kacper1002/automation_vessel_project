class Tank:
    def __init__(self, name, capacity, level):
        self.name = name
        self.capacity = capacity
        self.level = level      # in m3

    def update(self, inflow, outflow, dt):
        self.level += (inflow - outflow) * dt
        self.level = max(0, min(self.level, self.capacity))

    def level_percent(self):
        return (self.level / self.capacity) * 100