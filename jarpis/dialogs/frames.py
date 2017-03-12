EventName = {}
EventType = {}
Date = {}

Period = {
    "entityType": None,
    "slots": {
        "start": Date,
        "end": Date
    }
}

Username = {}

User = {
    "entityType": "User",
    "slots": {
        "name": Username
    }
}

Scheduling = {
    # TODO define
}

Privacy = {}

Visibility = {
    "entityType": "Visibility",
    "slots": {
        "privacy": Privacy
    }
}

Item = {
    # TODO define
}

Event = {
    "entityType": "Event",
    "slots": {
        "name": EventName,
        "type": EventType,
        "period": Period,
        "creator": User,
        "scheduling": Scheduling,
        "visibility": Visibility,
        "listItems": [Item]
    }
}

EventByName = {
    "entityType": "Event",
    "slots": {
        "name": EventName
    }
}

EventByDate = {
    "entityType": "Event",
    "slots": {

    }
}

EventsByTypeQuery = {
    "entityType": None,
    "slots": {
        "type": EventType,
        "events": [Event]
    }
}

EventsByDateQuery = {
    "entityType": None,
    "slots": {
        "period": Period,
        "events": [Event]
    }
}

EventsByCreatorQuery = {
    "entityType": None,
    "slots": {
        "creator": User,
        "period": Period,
        "events": [Event]
    }
}

EventsByVisibilityQuery = {
    "entityType": None,
    "slots": {
        "visibility": Visibility,
        "creator": User,
        "period": Period,
        "events": [Event]
    }
}
