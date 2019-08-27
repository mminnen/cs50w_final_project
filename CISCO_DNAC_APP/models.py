from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DnacControllers(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


# class WebhookEvents:


class NetworkHealth(models.Model):
    """
    {
    "version": "1.0",
    "response": [
        {
            "time": "2019-08-26T14:30:00.000+0000",
            "healthScore": 100,
            "totalCount": 14,
            "goodCount": 14,
            "unmonCount": 0,
            "fairCount": 0,
            "badCount": 0,
            "entity": null,
            "timeinMillis": 1566829800000
        }
    ],
    "measuredBy": "global",
    "latestMeasuredByEntity": null,
    "latestHealthScore": 100,
    "monitoredDevices": 14,
    "monitoredHealthyDevices": 14,
    "monitoredUnHealthyDevices": 0,
    "unMonitoredDevices": 0,
    "healthDistirubution": [
        {
            "category": "Access",
            "totalCount": 2,
            "healthScore": 100,
            "goodPercentage": 100,
            "badPercentage": 0,
            "fairPercentage": 0,
            "unmonPercentage": 0,
            "goodCount": 2,
            "badCount": 0,
            "fairCount": 0,
            "unmonCount": 0,
            "kpiMetrics": []
        },
        {
            "category": "Distribution",
            "totalCount": 1,
            "healthScore": 100,
            "goodPercentage": 100,
            "badPercentage": 0,
            "fairPercentage": 0,
            "unmonPercentage": 0,
            "goodCount": 1,
            "badCount": 0,
            "fairCount": 0,
            "unmonCount": 0,
            "kpiMetrics": []
        },
        {
            "category": "WLC",
            "totalCount": 1,
            "healthScore": 100,
            "goodPercentage": 100,
            "badPercentage": 0,
            "fairPercentage": 0,
            "unmonPercentage": 0,
            "goodCount": 1,
            "badCount": 0,
            "fairCount": 0,
            "unmonCount": 0,
            "kpiMetrics": []
        },
        {
            "category": "AP",
            "totalCount": 10,
            "healthScore": 100,
            "goodPercentage": 100,
            "badPercentage": 0,
            "fairPercentage": 0,
            "unmonPercentage": 0,
            "goodCount": 10,
            "badCount": 0,
            "fairCount": 0,
            "unmonCount": 0,
            "kpiMetrics": []
        }
    ]
}
    """


