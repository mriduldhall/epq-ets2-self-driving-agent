class Estimator:
    def __init__(self, centre=222, x_impact=0.1):
        self.centre = centre
        self.x_impact = x_impact

    def estimate_exponential_distance(self, object_x_position, object_width, object_y_distance):
        object_x_distance = object_x_position + (object_width / 2)
        pixel_distance = ((self.x_impact * (self.centre - object_x_distance)) ** 2 + object_y_distance ** 2) ** 0.5
        distance = (1.033 ** pixel_distance) + (0.1 * pixel_distance) + (0.0002 * (pixel_distance ** 2)) + 9
        return str(distance)

    def estimate_polynomial_distance(self, object_x_position, object_width, object_y_distance):
        object_x_distance = object_x_position + (object_width / 2)
        pixel_distance = ((self.x_impact * (self.centre - object_x_distance)) ** 2 + object_y_distance ** 2) ** 0.5
        distance = (0.00000015 * (pixel_distance ** 4)) + (0.000004 * (pixel_distance ** 3)) + (0.00099 * (pixel_distance ** 2)) + (0.099 * pixel_distance) + 10
        return str(distance)
