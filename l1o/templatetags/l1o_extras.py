from django import template

register = template.Library()


def clinched_promotion(points, promotion_threshold):
    return points > promotion_threshold


def clinched_relegation(max_possible_points, relegation_threshold):
    return max_possible_points < relegation_threshold


register.filter("clinched_promotion", clinched_promotion)
register.filter("clinched_relegation", clinched_relegation)
