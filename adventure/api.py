from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from django.utils import timezone
from datetime import datetime, timedelta
from adv_blockchain.blockchain import Blockchain

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

SHOP_ROOM_ID=1
NAME_CHANGE_ROOM_ID=467
HOLLOWAY_SHRINE_ROOM_ID=22
BRADY_SHRINE_ROOM_ID=461

PENALTY_COOLDOWN_VIOLATION=5
PENALTY_NOT_FOUND=5
PENALTY_CANT_AFFORD=5
PENALTY_CANNOT_MOVE_THAT_WAY=5
PENALTY_TOO_HEAVY=5
PENALTY_UPHILL = 5
PENALTY_TRAP = 30

PENALTY_CAVE_FLY = 10

PENALTY_BAD_DASH = 20

PENALTY_BLASPHEMY = 10

MIN_COOLDOWN = 1
MAX_COOLDOWN = 600

def randomize_item(player, item):
    quality = random.triangular(-1, 1)
    adjective = ""

    if quality < 0:
        adjective = "poor"
        if quality < -.5:
            adjective = "terrible"
            if quality < -.9:
                adjective = "appalling"
    else:
        adjective = "nice"
        if quality > .5:
            adjective = "well-crafted"
            if quality > .9:
                adjective = "exquisite"

    atts = json.loads(item.attributes)

    if atts['STRENGTH'] is not None:
        atts['STRENGTH'] = int(atts['STRENGTH'] + (atts['STRENGTH'] * quality))

    if atts['SPEED'] is not None:
        atts['SPEED'] = int(atts['SPEED'] + (atts['SPEED'] * quality))

    t = Item(name=adjective+item.name,
         description=name.description+"  It has been transmogrified.",
         weight=int(item.weight - (item.weight * quality)),
         aliases="transmographied "+item.aliases,
         value=int(item.value + (item.value * quality)),
         itemtype=item.itemtype,
         attributes=json.dumps(atts),
    t.save()

def check_cooldown_error(player):
    """
    Return cooldown error if cooldown is bad, None if it's valid
    """
    if player.cooldown > timezone.now():
        t_delta = (player.cooldown - timezone.now())
        cooldown_seconds = min(MAX_COOLDOWN, t_delta.seconds + t_delta.microseconds / 1000000 + PENALTY_COOLDOWN_VIOLATION)
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.save()
        return JsonResponse({"cooldown": cooldown_seconds, 'errors':[f"Cooldown Violation: +{PENALTY_COOLDOWN_VIOLATION}s CD"]}, safe=True, status=400)
    return None

def api_response(player, cooldown_seconds, errors=None, messages=None):
    if errors is None:
        errors = []
    if messages is None:
        messages = []
    room = player.room()
    if player.is_pm:
        response = JsonResponse({'room_id':room.id,
                                 'title':room.title,
                                 'uuid':player.uuid,
                                 'description':room.description,
                                 'coordinates':room.coordinates,
                                 'elevation':room.elevation,
                                 'terrain':room.terrain,
                                 'players':room.playerNames(player.id, True),
                                 'items':room.itemNames(),
                                 'exits':room.exits(),
                                 'cooldown': cooldown_seconds,
                                 'errors': errors,
                                 'messages':messages}, safe=True)
    else:
        response = JsonResponse({'room_id':room.id,
                                 'title': room.title,
                                 'description':room.description,
                                 'coordinates':room.coordinates,
                                 'elevation':room.elevation,
                                 'terrain':room.terrain,
                                 'players':room.playerNames(player.id, True),
                                 'items':room.itemNames(),
                                 'exits':room.exits(),
                                 'cooldown': cooldown_seconds,
                                 'errors': errors,
                                 'messages':messages}, safe=True)
    return response


def player_api_response(player, cooldown_seconds, errors=None, messages=None):
    if errors is None:
        errors = []
    if messages is None:
        messages = []
    response = JsonResponse({'name':player.name,
                             'cooldown': cooldown_seconds,
                             'encumbrance': player.encumbrance,
                             'strength': player.strength,
                             'speed': player.speed,
                             'gold': player.gold,
                             'inventory': player.inventory(),
                             'status': [],
                             'errors': errors,
                             'messages': messages}, safe=True)
    return response

def item_examine_api_response(item, cooldown_seconds, errors=None, messages=None):
    if errors is None:
        errors = []
    if messages is None:
        messages = []
    response = JsonResponse({'name':item.name,
                             'description':item.description,
                             'weight':item.weight,
                             'itemtype':item.itemtype,
                             'level':item.level,
                             'exp':item.exp,
                             'attributes':item.attributes,
                             'cooldown': cooldown_seconds,
                             'errors': errors,
                             'messages': messages}, safe=True)
    return response

def player_examine_api_response(player, cooldown_seconds, errors=None, messages=None):
    if errors is None:
        errors = []
    if messages is None:
        messages = []
    response = JsonResponse({'name':player.name,
                             'description':player.name + player.description,
                             'cooldown': cooldown_seconds,
                             'errors': errors,
                             'messages': messages}, safe=True)
    return response


def get_cooldown(player, cooldown_scale):
    speed_adjustment = player.speed - 10
    time_factor = float(config('TIME_SCALE'))
    if player.is_pm:
        time_factor = min(time_factor, 5)
    return max(MIN_COOLDOWN, cooldown_scale * time_factor - speed_adjustment)



@csrf_exempt
@api_view(["GET"])
def initialize(request):
    player = request.user.player

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    cooldown_seconds = get_cooldown(player, 0.0)
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()

    return api_response(player, cooldown_seconds)


@api_view(["POST"])
def move(request):
    player = request.user.player
    # import pdb; pdb.set_trace()
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    cooldown_seconds = get_cooldown(player, 1.0)
    errors = []
    messages = []
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID >= 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        messages.append(f"You have walked {dirs[direction]}.")
        elevation_change = player.room().elevation - room.elevation
        if elevation_change > 0:
            messages.append(f"Uphill Penalty: {PENALTY_UPHILL}s CD")
            cooldown_seconds += PENALTY_UPHILL
        if player.strength <= player.encumbrance:
            messages.append(f"Heavily Encumbered: +100% CD")
            cooldown_seconds *= 2
        if nextRoom.terrain == "TRAP":
            messages.append(f"It's a trap!: +{PENALTY_TRAP}s CD")
            cooldown_seconds += PENALTY_TRAP
        if 'next_room_id' in data:
            if data['next_room_id'].isdigit() and int(data['next_room_id']) == nextRoomID:
                messages.append(f"Wise Explorer: -50% CD")
                cooldown_seconds /= 2
            else:
                messages.append(f"Foolish Explorer: +50% CD")
                cooldown_seconds *= 1.5
        if nextRoom.terrain == "MOUNTAIN" and len(Player.objects.filter(id=9)) > 0:
            pusher.trigger(f'p-channel-{Player.objects.get(id=9).uuid}', u'broadcast', {'message':f'{player.name} has walked {dirs[direction]} to room {nextRoom.id}.'})
    else:
        cooldown_seconds += PENALTY_CANNOT_MOVE_THAT_WAY
        errors.append(f"You cannot move that way: +{PENALTY_CANNOT_MOVE_THAT_WAY}s CD")
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)




@api_view(["POST"])
def take(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    alias = data['name']
    room = player.room()
    item = room.findItemByAlias(alias)
    cooldown_seconds = get_cooldown(player, 0.5)
    errors = []
    messages = []
    if item is None:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    elif player.strength * 2 <= player.encumbrance + item.weight:
        cooldown_seconds += PENALTY_TOO_HEAVY
        errors.append(f"Item too heavy: +{PENALTY_TOO_HEAVY}s CD")
    else:
        messages.append(f"You have picked up {item.name}")
        player.addItem(item)
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)

@api_view(["POST"])
def gamble(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    alias = data['name']
    room = player.room()
    item = player.findItemByAlias(alias)
    cooldown_seconds = get_cooldown(player, 0.5)
    errors = []
    messages = []
    if item is None:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    else:
        if Blockchain.get_user_balance(player) > 1:
            # Spend the coin by giving it back to the server
            Blockchain.new_transaction(player, 0, 1)
            # TODO: Generate new item
        else:
            # TODO: Error for not having a coin
            cooldown_seconds += PENALTY_CANT_AFFORD
            errors.append(f"You don't have a Lambda Coin: +{PENALTY_CANT_AFFORD}s CD")

    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player,
                        cooldown_seconds,
                        errors=errors,
                        messages=messages)


@api_view(["POST"])
def drop(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    alias = data['name']
    room = player.room()
    item = player.findItemByAlias(alias)
    cooldown_seconds = get_cooldown(player, 0.5)
    errors = []
    messages = []
    if item is None:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    else:
        messages.append(f"You have dropped {item.name}")
        room.addItem(item)
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)


@api_view(["POST"])
def examine(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    alias = data['name']
    room = player.room()
    # import pdb; pdb.set_trace()
    item = room.findItemByAlias(alias)
    if item is None:
        item = player.findItemByAlias(alias)
    players = room.findPlayerByName(alias)
    cooldown_seconds = get_cooldown(player, 0.5)
    errors = []
    messages = []
    if item is not None:
        # Examine item
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.save()
        return item_examine_api_response(item, cooldown_seconds, errors=errors, messages=messages)
    if len(players) > 0:
        # Examine player
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.save()
        return player_examine_api_response(players[0], cooldown_seconds, errors=errors, messages=messages)
    cooldown_seconds += PENALTY_NOT_FOUND
    errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)




@api_view(["POST"])
def status(request):
    player = request.user.player

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    cooldown_seconds = get_cooldown(player, 0)

    return player_api_response(player, cooldown_seconds)


@api_view(["POST"])
def sell(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    cooldown_seconds = get_cooldown(player, 0.2)

    errors = []
    messages = []

    if player.currentRoom != SHOP_ROOM_ID:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append("Shop not found: +{PENALTY_NOT_FOUND}")
    else:
        item = player.findItemByAlias(data["name"])
        if item is None:
            cooldown_seconds += PENALTY_NOT_FOUND
            errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
        elif "confirm" not in data or data["confirm"].lower() != "yes":
            messages.append(f"I'll give you {item.value} gold for that {item.name}.")
            messages.append(f"(include 'confirm':'yes' to sell {item.name})")
        else:
            messages.append(f"Thanks, I'll take that {item.name}.")
            messages.append(f"You have received {item.value} gold.")
            if item.itemtype == "TREASURE":
                item.levelUpAndRespawn()
            else:
                item.unsetItem()
            player.gold += item.value

    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)


@api_view(["POST"])
def wear(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    alias = data['name']
    item = player.findItemByAlias(alias)
    cooldown_seconds = get_cooldown(player, 0.5)
    errors = []
    messages = []
    if item is None:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    else:
        if player.wearItem(item):
            messages.append(f"You wear {item.name}")
        else:
            messages.append(f"You cannot wear {item.name}")
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)


@api_view(["POST"])
def remove(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    # alias = data['name']
    # item = player.findItemByAlias(alias)
    # cooldown_seconds = get_cooldown(player, 0.5)
    # errors = []
    # messages = []
    # if item is None:
    #     cooldown_seconds += PENALTY_NOT_FOUND
    #     errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    # else:
    #     if player.wearItem(item):
    #         messages.append(f"You wear {item.name}")
    #     else:
    #         messages.append(f"You cannot wear {item.name}")
    # player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    # player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)



@api_view(["POST"])
def change_name(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    new_name = data['name']
    cooldown_seconds = get_cooldown(player, 2.0)
    errors = []
    messages = []
    if player.currentRoom != NAME_CHANGE_ROOM_ID:
        cooldown_seconds += 5 * PENALTY_NOT_FOUND
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.save()
        errors.append("Name changer not found: +{5 * PENALTY_NOT_FOUND}")
    else:
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.name = new_name
        player.save()
        messages.append(f"You have changed your name to {new_name}.")
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)




@api_view(["POST"])
def pray(request):
    player = request.user.player

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    cooldown_seconds = get_cooldown(player, 5.0)
    errors = []
    messages = []
    if player.currentRoom == HOLLOWAY_SHRINE_ROOM_ID:
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.can_fly = True
        player.save()
        messages.append(f"You notice your body starts to hover above the ground.")
        if len(Player.objects.filter(id=9)) > 0:
            pusher.trigger(f'p-channel-{Player.objects.get(id=9).uuid}', u'broadcast', {'message':f'{player.name} has prayed.'})
    elif player.currentRoom == BRADY_SHRINE_ROOM_ID:
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.can_dash = True
        player.save()
        messages.append(f"You feel a mysterious power and speed coiling in your legs.")
    else:
        cooldown_seconds += 5 * PENALTY_NOT_FOUND
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.save()
        errors.append(f"Shrine not found: +{5 * PENALTY_NOT_FOUND}")
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)





@api_view(["POST"])
def fly(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    cooldown_seconds = get_cooldown(player, 1.0)
    errors = []
    messages = []
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if not player.can_fly:
        cooldown_seconds += PENALTY_BLASPHEMY
        errors.append(f"You cannot fly: +{PENALTY_BLASPHEMY}s CD")
    elif nextRoomID is not None and nextRoomID >= 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        messages.append(f"You have flown {dirs[direction]}.")
        elevation_change = player.room().elevation - room.elevation
        if player.strength <= player.encumbrance:
            messages.append(f"Flying while Heavily Encumbered: +200% CD")
            cooldown_seconds *= 3
        elif elevation_change < 0:
            messages.append(f"Downhill Flight Bonus: Instant CD")
            cooldown_seconds = 1.0
        elif nextRoom.terrain == "CAVE":
            messages.append(f"You bump your head on the cave ceiling: +{PENALTY_CAVE_FLY}s CD")
            cooldown_seconds += PENALTY_CAVE_FLY
        else:
            messages.append(f"Flight Bonus: -10% CD")
            cooldown_seconds *= 0.9
        if nextRoom.terrain == "TRAP":
            messages.append(f"It's a trap!: +{PENALTY_TRAP}s CD")
            cooldown_seconds += PENALTY_TRAP
        if 'next_room_id' in data:
            if data['next_room_id'].isdigit() and int(data['next_room_id']) == nextRoomID:
                messages.append(f"Wise Explorer: -50% CD")
                cooldown_seconds /= 2
            else:
                messages.append(f"Foolish Explorer: +50% CD")
                cooldown_seconds *= 1.5
        if nextRoom.terrain == "MOUNTAIN" and len(Player.objects.filter(id=1)) > 0:
            pusher.trigger(f'p-channel-{Player.objects.get(id=1).uuid}', u'broadcast', {'message':f'{player.name} has flown {dirs[direction]} to room {nextRoom.id}.'})
    else:
        cooldown_seconds += PENALTY_CANNOT_MOVE_THAT_WAY
        errors.append(f"You cannot move that way: +{PENALTY_CANNOT_MOVE_THAT_WAY}s CD")
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)



@api_view(["POST"])
def dash(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    direction = data['direction']
    room_ids = data['next_room_ids'].split(",")
    room_int_ids = [r for r in room_ids if r.isdigit()]
    num_rooms = data['num_rooms']
    cooldown_seconds = get_cooldown(player, 1.0)
    errors = []
    messages = []
    if not player.can_dash:
        cooldown_seconds += PENALTY_BLASPHEMY
        errors.append(f"You cannot dash: +{PENALTY_BLASPHEMY}s CD")
    elif not (num_rooms.isdigit() and int(num_rooms) == len(room_ids) and len(room_int_ids) == int(num_rooms)):
        cooldown_seconds += PENALTY_BAD_DASH
        errors.append(f"Malformed Dash: +{PENALTY_BAD_DASH}s CD")
    else:
        for room_id in room_int_ids:
            room = player.room()
            if direction == "n":
                nextRoomID = room.n_to
            elif direction == "s":
                nextRoomID = room.s_to
            elif direction == "e":
                nextRoomID = room.e_to
            elif direction == "w":
                nextRoomID = room.w_to
            else:
                cooldown_seconds += PENALTY_BAD_DASH
                errors.append(f"Bad Dash: +{PENALTY_BAD_DASH}s CD")
            if int(nextRoomID) == int(room_id):
                player.currentRoom = nextRoomID
                cooldown_seconds += 0.5
                messages.append(f"You have dashed to room {nextRoomID}.")

                elevation_change = player.room().elevation - room.elevation
                if player.strength <= player.encumbrance:
                    messages.append(f"Dashing while Heavily Encumbered: +1s CD")
                    cooldown_seconds += 1
                if elevation_change < 0:
                    messages.append(f"Downhill Dash Bonus: Instant CD")
                    cooldown_seconds -= 0.5
                elif elevation_change > 0:
                    messages.append(f"Uphill Dash Penalty: +0.5s")
                    cooldown_seconds += 0.5
            else:
                cooldown_seconds += PENALTY_BAD_DASH
                errors.append(f"Bad Dash: +{PENALTY_BAD_DASH}s CD")
                break
        if player.room().terrain == "TRAP":
            messages.append(f"It's a trap!: +{PENALTY_TRAP}s CD")
            cooldown_seconds += PENALTY_TRAP

    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)







@api_view(["GET"])
def player_state(request):
    player = request.user.player
    if not player.is_pm:
        response = JsonResponse({'ERROR':'BAD_REQUEST'}, safe=True)
    else:
        players = Player.objects.all()
        rooms = []
        for p in players:
            rooms.append ([p.name, p.currentRoom])
        response = JsonResponse({'rooms':rooms}, safe=True)
    return response










