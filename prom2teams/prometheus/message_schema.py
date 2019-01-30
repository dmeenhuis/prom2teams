from marshmallow import Schema, fields, post_load, INCLUDE
import logging

log = logging.getLogger('prom2teams')

class MessageSchema(Schema):
    receiver = fields.Str()
    status = fields.Str(default='unknown', missing='unknown')
    alerts = fields.Nested('AlertSchema', many=True)
    externalURL = fields.Str()
    version = fields.Str()

    class Meta:
        unknown = INCLUDE

    @post_load
    def get_alerts(self, message):
        log.debug('JSON received is:\n%s', str(message))
        prom_alerts = []
        externalURL = message['externalURL']
        for alert in message['alerts']:
            status = alert['status']
            generatorURL = alert['generatorURL']
            summary = alert['annotations']['message']
            name = alert['labels']['alertname']
            description = alert['annotations']['message']
            severity = alert['labels']['severity']

            alert = PrometheusAlert(name, status, severity, summary, generatorURL, description, externalURL)
            prom_alerts.append(alert)
        return prom_alerts


class AlertSchema(Schema):
    status = fields.Str(default='unknown', missing='unknown')
    labels = fields.Nested('LabelSchema', many=False)
    annotations = fields.Nested('AnnotationSchema', many=False)
    startsAt = fields.DateTime()
    endsAt = fields.DateTime()
    generatorURL = fields.Str()

    class Meta:
        unknown = INCLUDE

class LabelSchema(Schema):
    alertname = fields.Str(default='unknown', missing='unknown')
    device = fields.Str()
    fstype = fields.Str()
    instance = fields.Str(default='unknown', missing='unknown')
    job = fields.Str()
    mountpoint = fields.Str()
    severity = fields.Str(default='unknown', missing='unknown')

    class Meta:
        unknown = INCLUDE


class AnnotationSchema(Schema):
    description = fields.Str(default='unknown', missing='unknown')
    message = fields.Str(default='unknown', missing='unknown')
    summary = fields.Str(default='unknown', missing='unknown')

    class Meta:
        unknown = INCLUDE


class PrometheusAlert:
    def __init__(self, name, status, severity, summary, instance, description, externalURL):
        self.name = name
        self.status = status
        self.severity = severity
        self.summary = summary
        self.instance = instance
        self.description = description
        self.externalURL = externalURL
