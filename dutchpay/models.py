from django.db import models

class Person(models.Model):
  name = models.CharField(max_length=30)
  nickname = models.CharField(max_length=10, blank=True)
  note = models.CharField(max_length=500, blank=True)

  def __str__(self):
    if self.nickname != '':
      return "[{}] {}".format(self.nickname, self.name)
    else:
      return self.name

class Meeting(models.Model):
  name = models.CharField(max_length=30)
  date = models.DateTimeField()
  people = models.ManyToManyField(Person, through='Participation')
  cleared = models.BooleanField(default=False)

  def __str__(self):
    return "{} on {}".format(self.name, self.date)

class Participation(models.Model):
  person = models.ForeignKey(Person, on_delete=models.CASCADE)
  meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
  cleared = models.BooleanField(default=False)

  def __str__(self):
    return "{} at {}".format(self.person.name, self.meeting.name)

class Place(models.Model):
  name = models.CharField(max_length=30)
  meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

  def __str__(self):
    return "{} for {}".format(self.name, self.meeting.name)

class Item(models.Model):
  name = models.CharField(max_length=30)
  place = models.ForeignKey(Place, on_delete=models.CASCADE)
  price = models.PositiveIntegerField()
  quantity = models.PositiveIntegerField()
  participation = models.ManyToManyField(Participation, through='Consume')

  def __str__(self):
    return "[{}] - {}, {} * {} won".format(self.place.name, self.name, self.quantity, self.price)

class Consume(models.Model):
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  participation = models.ForeignKey(Participation, on_delete=models.CASCADE)
  weight = models.PositiveIntegerField()

  def __str__(self):
    who = self.participation.person
    return "{} consumed {} {}(s)".format(who.name, self.weight, self.item.name)
