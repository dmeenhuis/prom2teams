from marshmallow import Schema, fields, INCLUDE


class TeamsAlarmSchema(Schema):
    status = fields.Str()
    severity = fields.Str()
    summary = fields.Str()
    instance = fields.Str()
    description = fields.Str()
    name = fields.Str()
    externalURL = fields.Str()

    class Meta:
        unknown = INCLUDE


class TeamsAlarm:
    def __init__(self, name, status, severity, summary, instance, description, externalURL):
        self.name = name
        self.status = status
        self.severity = severity
        self.summary = summary
        self.instance = instance
        self.description = description
        self.externalURL = externalURL
