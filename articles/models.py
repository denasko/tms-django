from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    like_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey('Author', on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
