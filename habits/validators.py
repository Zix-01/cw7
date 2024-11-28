from django.utils import timezone
from rest_framework import serializers
from habits.models import Habit


class RewardAndRelatedValidator:
    def __call__(self, value):
        if value.get('prize') and value.get('related'):
            raise serializers.ValidationError(
                'Одновременное заполнение поля вознаграждения и поля связанной привычки недопустимо.'
            )


class ExecutionTimeValidator:
    def __call__(self, value):
        if value.get('duration', 0) > 2:
            raise serializers.ValidationError(
                 'Привычка должна выполняться не дольше двух минут'
            )


class PleasantHabitValidator:
    def __call__(self, value):
        related_id = value.get('related')
        if related_id:
            related_habit = Habit.objects.filter(id=related_id).first()
            if related_habit and not related_habit.is_pleasant:
                raise serializers.ValidationError(
                    'Связанная привычка должна помечаться как приятная.'
                )


class PleasantHabitNoRelatedOrPrizeValidator:
    def __call__(self, value):
        if value.get('is_pleasant') and (value.get('prize') or value.get('related')):
            raise serializers.ValidationError(
                'Приятная привычка не может дополняться вознаграждением или иметь связанную привычку.'
            )


class FrequencyValidator:
    def __call__(self, value):
        if value.get('execution_interval_day', 0) > 7:
            raise serializers.ValidationError(
                'Привычку нужно выполнять минимум раз в неделю'
            )


class LastPerformedValidator:
    def __call__(self, value):
        if value.get('last_performed'):
            days_since_last = (timezone.now().date() - value['last_performed']).days
            if days_since_last > 7:
                raise serializers.ValidationError(
                    'Пропускать привычку можно не больше недели.'
                )
