from django.db import models
from django.urls import reverse
from datetime import date

MEALS = (
  ('B', 'Breakfast'),
  ('L', 'Lunch'),
  ('D', 'Dinner'),
)

# Create your models here.

class Food(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('foods_detail', kwargs={'pk': self.id})


class Ant(models.Model):
  name = models.CharField(max_length=100)
  species = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  foods = models.ManyToManyField(Food)

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'ant_id': self.id})

  def fed_for_today(self):
      return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


class Feeding(models.Model):
  date = models.DateField('Feeding Date')
  meal = models.CharField(
    max_length=1,
    choices=MEALS,
    default=MEALS[0][0]
  )
  # Add a ant_id column/attribute
  # The ant attribute below will return the
  # entire ant object that a feeding belongs to
  ant = models.ForeignKey(
    Ant,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f'{self.get_meal_display()} on {self.date}'

  class Meta:
    ordering = ['-date']