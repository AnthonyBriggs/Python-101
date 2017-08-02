from django.db import models
from django.contrib.auth.models import User

# Create your models here.

importance_choices = (                      #3
    ('A', 'Very Important'),                #3
    ('B', 'Important'),                     #3
    ('C', 'Medium'),                        #3
    ('D', 'Unimportant'),                   #3
)                                           #3

class Todo(models.Model):                       #1
    title = models.CharField(max_length=200)    #2
    description = models.TextField()            #2
    
    importance = models.CharField(              #3
        max_length=1,                           #3
        choices=importance_choices)             #3
    
    owner = models.ForeignKey(User)
    
    def text_importance(self):
        return dict(importance_choices)[self.importance]

    def short_description(self):
        return self.description.split('\n')[0][:80]

    # def get_absolute_url(self):
    #     return str(self.id)
        
    def __unicode__(self):
        return self.title

