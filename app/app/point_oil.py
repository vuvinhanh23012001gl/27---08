class PointOil:
    def __init__(self, x, y, z, brightness):
        self.x = x
        self.y = y
        self.z = z
        self.brightness = brightness

    def __str__(self):
        return f"(X={self.x}, Y={self.y}, Z={self.z}, Brightness={self.brightness})"
    def dict_point_oil(self):
        return { "x": self.x,
            "y": self.y,
            "z": self.z,
            "brightness": self.brightness,  
        }
    def show(self):
        print(f"Tọa độ dầu: {self}")