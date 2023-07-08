from django import template

register = template.Library()


def clinched_promotion(points, promotion_threshold):
    return points > promotion_threshold


def clinched_relegation(max_possible_points, relegation_threshold):
    return max_possible_points < relegation_threshold


def clinched_playoffs(points, playoff_threshold):
    return points > playoff_threshold


def eliminated_from_playoffs(max_possible_points, sixth_place_points):
    return max_possible_points < sixth_place_points


register.filter("clinched_promotion", clinched_promotion)
register.filter("clinched_relegation", clinched_relegation)
register.filter("clinched_playoffs", clinched_playoffs)
register.filter("eliminated_from_playoffs", eliminated_from_playoffs)
