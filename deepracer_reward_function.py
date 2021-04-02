import math


def distance(location1, location2):
    return ((location1[0] - location2[0]) ** 2 + (location1[1] - location2[1]) ** 2) ** 0.5

def rectangle(radius, theta):
    #param: theta degrees
    x = radius * math.cos(math.radians(theta))
    y = radius * math.sin(math.radians(theta))
    return x, y


def angle_modified_360(angle):
    """
    Mapping angles with intervals of -180 to +180 degrees.
    """

    n_degrees = math.floor(angle/360.0)

    angle_from_0_and_360 = angle - n_degrees*360.0

    if angle_from_0_and_360 <= 180.0:
        return angle_from_0_and_360
    else:
        return angle_from_0_and_360 - 360


def polar_coordinates(x, y):
    radius = (x ** 2 + y ** 2) ** .5
    theta = math.degrees(math.atan2(y,x))
    return r, theta


def get_ordered_waypoints(params):
    # waypoints are given in counter clockwise order
    if params['is_reversed']: # reversing waypoints driving clock wise
        return list(reversed(params['waypoints']))
    else: # driving counter clock wise.
        return params['waypoints']


def up_sampling(waypoints, factor):
    #Adding an extra waypoint between waypoints enhancing accuracy

    point = waypoints
    number = len(p)

    return [[i / factor * point[(j+1) % number][0] + (1 - i / factor) * point[j][0],
             i / factor * point[(j+1) % number][1] + (1 - i / factor) * point[j][1]] for j in range(number) for i in range(factor)]


def get_a_target_point(params):
    waypoints = up_sampling(get_ordered_waypoints(params), 20)

    car_position = [params['x'], params['y']]

    distances = [distance(point, car_position) for point in waypoints]
    min_distance = min(distances)
    i_closest = distances.index(min_distance)

    number_waypoints = len(waypoints)

    waypoints_starting_with_closest = [waypoints[(i+i_closest) % number_waypoints] for i in range(number_waypoints)]

    radius = params['track_width'] * 0.9

    is_inside_track = [distance(p, car_position) < radius for p in waypoints_starting_with_closest]
    i_first_outside_track = is_inside_track.index(False)

    if i_first_outside_track < 0:  # this only happens if we have a radius as big as the entire track
        return waypoints[i_closest]

    return waypoints_starting_with_closest[i_first_outside_track]


def get_target_steering_angle_degree(params):
    target_point_x, target_point_y = get_a_target_point(params)
    position_x = params['x']
    position_y = params['y']
    dx = target_point_x-position_x
    dy = target_point_y-position_y
    heading = params['heading']

    _, target_angle = polar_coordinates(dx, dy)

    steering_angle = target_angle - heading

    return angle_modified_360(steering_angle)


def score_function_steer_to_point_ahead(params):
    optimal_stearing_angle = get_target_steering_angle_degree(params)
    steer_angle = params['steering_angle']

    error_rate = (steer_angle - optimal_stearing_angle) / 60.0  # 60 degree is already really bad

    scoring = 1.0 - abs(error_rate)

    return max(scoring, 0.01)  


def reward_function(params):
    return float(score_function_steer_to_point_ahead(params))
