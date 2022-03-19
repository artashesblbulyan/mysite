from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATHEGORIES = (
    (0, "Communication"),
    (1, "Conference Report"),
    (2, "Editorial"),
    (3, "Opinion"),
    (4, "Perspective"),
    (5, "Book Review"),
    (6, "Registered Report"),
    (7, "Review"),


)


class Article(models.Model):  # An article  the user is learning about.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    heading = models.CharField(max_length=70)
    text = models.CharField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    cathegory = models.IntegerField(choices=CATHEGORIES)

    def __str__(self):  # Return a string representation of the model.
        return self.text


class Comments(models.Model):
    # Something specific learned about a topic.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        # Return a string representation of the model.
        return f"{self.text[:50]}..."
