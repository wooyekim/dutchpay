from django.http import HttpResponse
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.template.defaulttags import register
import math

from .models import Meeting, Consume, Item, Place, Participation, Person

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

from .forms import PersonForm, MeetingForm

def person_new(request):
  if request.method == 'POST':
    form = PersonForm(request.POST)
    if form.is_valid():
      person = form.save()
      return redirect('index')
  else:
    form = PersonForm()
  return render(request, 'dutchpay/person_edit.html', {'form': form})

def meeting_new(request):
  if request.method == 'POST':
    sid = transaction.savepoint()
    try:
      meeting = parseMeeting(request)
      meeting.save()
      places = parsePlaces(request, meeting)
      for k, place in places.items():
        place.save()
      items = parseItems(request, places)
      for k, item in items.items():
        item.save()
      participations = parseParticipations(request, meeting)
      for k, participation in participations.items():
        participation.save()
      consumes = parseConsumes(request, items, participations)
      for consume in consumes:
        consume.save()
      transaction.savepoint_commit(sid)
    except IntegrityError:
      transaction.savepoint_rollback(sid)
      raise;
    context = {}
    context['meeting'] = meeting
    context['table'] = Table(meeting)
    return render(request, 'dutchpay/detail.html', context)
  else:
    form = MeetingForm()
    return render(request, 'dutchpay/meeting_edit.html', {'form': form})

def parseMeeting(request):
  # Parse meeting
  meeting = Meeting()
  meeting.name = request.POST['name']
  meeting.date = request.POST['date']
  return meeting

def parsePlaces(request, meeting):
  # Parse places
  places = {}
  for name, value in request.POST.items():
    if name.startswith('place_'):
      parsed_name = name.split('_')
      key = parsed_name[1]
      if key not in places:
        places[key] = Place(meeting = meeting)
      setattr(places[key], parsed_name[2], value)
  return places

def parseItems(request, places):
  # Parse items
  items = {}
  for name, value in request.POST.items():
    if name.startswith('item_'):
      parsed_name = name.split('_')
      key = parsed_name[1]
      if key not in items:
        items[key] = Item()
      item = items[key]
      if parsed_name[2] == 'place':
        item.place = places[value]
      else:
        setattr(item, parsed_name[2], value)
  return items

def parseParticipations(request, meeting):
  # Parse participations
  participations = {}
  for name, value in request.POST.items():
    if name.startswith('participation_'):
      parsed_name = name.split('_')
      key = parsed_name[1]
      if key not in participations:
        participations[key] = Participation()
        participations[key].meeting = meeting
      part = participations[key]
      if parsed_name[2] == 'person':
        part.person = Person.objects.get(pk=int(value))
      elif parsed_name[2] == 'cleared':
        part.cleared = True if value == 'on' else False
      else:
        setattr(part, parsed_name[2], value)
  return participations

def parseConsumes(request, items, participations):
  # Parse consumes
  consumes = []
  for name, value in request.POST.items():
    if value == '' or value == '0':
        continue
    if name.startswith('consume_'):
      parsed_name = name.split('_')
      item_key = parsed_name[1]
      participation_key = parsed_name[2]
      consume = Consume()
      consume.item = items[item_key]
      consume.participation = participations[participation_key]
      consume.weight = value
      consumes.append(consume)
  return consumes
