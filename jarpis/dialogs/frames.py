
Timestamp = {}
Date = {
    "entityType": "Date",
    "slots": {
        "timestamp": Timestamp
    },
    "responses": {}
}

DateReference = {}
DateByReference = {
    "entityType": "Date",
    "slots": {
        "reference": DateReference
    },
    "responses": {}
}

Days = {}
DateByDays = {
    "entityType": "Date",
    "slots": {
        "days": Days
    },
    "responses": {}
}

Day = {}
Month = {}
Year = {}
DateByComponents = {
    "entityType": "Date",
    "slots": {
        "day": Day,
        "month": Month,
        "year": Year
    },
    "responses": {}
}

Period = {
    "entityType": "Period",
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

EventName = {}
EventType = {}
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

EventByDate = {
    "entityType": "Event",
    "slots": {
        "period": Period,
        "user": User,
        "Visibility": Visibility
    },
    "responses": {}
}

EventsByTypeQuery = {
    "entityType": "Query",
    "slots": {
        "type": EventType,
        "period": Period,
        "events": [Event]
    }
}

EventsByDateQuery = {
    "entityType": "Query",
    "slots": {
        "period": Period,
        "events": [Event]
    }
}

EventsByCreatorQuery = {
    "entityType": "Query",
    "slots": {
        "creator": User,
        "period": Period,
        "events": [Event]
    }
}

EventsByVisibilityQuery = {
    "entityType": "Query",
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
    "entityType": "Query",
    "slots": {
        "status": Status,
        "list": List,
        "items": [Item]
    }
}
