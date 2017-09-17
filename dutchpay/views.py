from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
import math

from .models import Meeting, Consume, Item, Place, Participation

def index(request):
  payment_list = Meeting.objects.order_by('-date')
  context = { 'payment_list': payment_list }
  return render(request, 'dutchpay/index.html', context)

class Table:
  def __init__(self, meeting):
    places = Place.objects.filter(meeting=meeting).all()
    items = {}
    counter = {}
    consumers = {}
    for place in places:
      items[place] = Item.objects.filter(place=place).all()
      for item in items[place]:
        counter[item] = 0
        item_consumers = Consume.objects.filter(item=item).all()
        for consume in item_consumers:
          who = consume.participation.person
          if who not in consumers:
            consumers[who] = {}
          consumers[who][item] = consume.weight
          counter[item] = counter[item] + consume.weight

    self.header = [[], []]
    # Build header row 1 (category)
    for place in places:
      self.header[0].append((place.name, len(items[place])))
    # Build header row 2 (items)
    for place in places:
      for item in items[place]:
        self.header[1].append((item.name, 1))

    self.footer = [[], []]
    total_sum = 0
    place_price_sum = {}
    # Build footer row 1 (items)
    for place in places:
      place_price_sum[place] = 0
      for item in items[place]:
        price = item.price * item.quantity
        place_price_sum[place] = place_price_sum[place] + price
        self.footer[0].append((price, 1))
    # Build footer row 2 (category)
    for place in places:
      total_sum = total_sum + place_price_sum[place]
      self.footer[1].append((place_price_sum[place], len(items[place])))
    self.total_sum = total_sum

    self.body = []
    for person, consume in consumers.items():
      cleared = Participation.objects.get(person=person, meeting=meeting).cleared
      row = ['O' if cleared else '', person.name]
      pay = 0
      for place in places:
        for item in items[place]:
          if item in consume:
            weight = consume[item] / counter[item]
            price = int(item.price * item.quantity * weight)
            pay = pay + price
            row.append(price)
          else:
            row.append('')
      row.extend([pay, int(math.floor(pay / 100) * 100)])
      self.body.append(row)

def detail(request, payment_id):
  context = {}
  try:
    meeting = Meeting.objects.get(pk=payment_id)
    context['meeting'] = meeting
    context['table'] = Table(meeting)
  except Meeting.DoesNotExist:
    raise Http404("Meeting does not exist")
  return render(request, 'dutchpay/detail.html', context)
