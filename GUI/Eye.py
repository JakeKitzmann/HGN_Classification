class Eye:
        def __init__(self):
            self.x = None
            self.y = None

            self.center_x = None
            self.center_y = None

            self.l = None
            self.w = None

        def magnitude(self):
            return ( ( self.x - self.center_x ) ** 2 + ( self.y - self.center_y ) ** 2 ) ** 0.5