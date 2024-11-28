from django.utils import timezone
from rest_framework import serializers
from habits.models import Habit


class RewardAndRelatedValidator:
    def __call__(self, value):
        if value.get('prize') and value.get('related'):
            raise serializers.ValidationError(
                'Заполнение поля вознаграждения и поля связанной привычки одновременно недопустимо.'
            )


class ExecutionTimeValidator:
    def __call__(self, value):
        if value.get('duration', 0) > 2:
            raise serializers.ValidationError(
                'Привычка не должна выполняться дольше 2-х минут'
            )


class PleasantHabitValidator:
    def __call__(self, value):
        related_id = value.get('related')
        if related_id:
            related_habit = Habit.objects.filter(id=related_id).first()
            if related_habit and not related_habit.is_pleasant:
                raise serializers.ValidationError(
                    'Связанная должна быть отмечена как приятная.'
                )


class PleasantHabitNoRelatedOrPrizeValidator:
    def __call__(self, value):
        if value.get('is_pleasant') and (value.get('prize') or value.get('related')):
            raise serializers.ValidationError(
                'Приятная привычка не нуждается в вознаграждении или связанной привычки'
            )


class FrequencyValidator:
    def __call__(self, value):
        if value.get('execution_interval_day', 0) > 7:
            raise serializers.ValidationError(
                'Привычка должна быть выполнена хотя бы раз в неделю.'
            )


class LastPerformedValidator:
    def __call__(self, value):
        if value.get('last_performed'):
            days_since_last = (timezone.now().date() - value['last_performed']).days
            if days_since_last > 7:
                raise serializers.ValidationError(
                    'Перерыв от привычки составил более недели.'
                )
