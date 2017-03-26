EventName = {}
EventType = {}
Date = {}

Period = {
    "entityType": None,
    "slots": {
        "start": Date,
        "end": Date
    },
    "responses": {
        "missing": ["When should this event start?", "From when to when shall I schedule the event?", "Until when shall I schedule it?"]
    }
}

Username = {}
Reference = {}

User = {
    "entityType": "User",
    "slots": {
        "name": Username
    },
    "responses": {}
}

UserByReference = {
    "entityType": "User",
    "slots": {
        "reference": Reference
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
    },
    "responses": {
        "missing": "Shall I consider only your private or all Events?"
    }
}


Description = {}

Status = {}

Item = {
    "entityType": "ListItem",
    "slots": {
        "description": Description,
        "status": Status
    }
}

List = {
    "entityType": "List",
    "slots": {
        "description": Description,
        "creator": User,
        "visibility": Visibility,
        "items": [Item]
    }
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
        "list": List
    },
    "responses": {}
}

EventByName = {
    "entityType": "Event",
    "slots": {
        "name": EventName
    },
    "responses": {}
}

EventByDate = {
    "entityType": "Event",
    "slots": {
        "period": Period
    },
    "responses": {}
}

EventsByTypeQuery = {
    "entityType": None,
    "slots": {
        "type": EventType,
        "period": Period,
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

ListByName = {
    "entityType": "List",
    "slots": {
        "event": Event,
        "name": Description
    }
}

ListByCreator = {
    "entityType": "List",
    "slots": {
        "event": Event,
        "creator": User
    }
}

ListByVisibility = {
    "entityType": "List",
    "slots": {
        "event": Event,
        "creator": User,
        "visibility": Visibility
    }
}

FinishedListItemsQuery = {
    "entityType": None,
    "slots": {
        "status": Status,
        "list": List,
        "items": [Item]
    }
}
