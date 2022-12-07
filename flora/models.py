from django.db import models

# Create your models here.
"""
AncientTree class
name
period (geological period)
classification
eaten_by many to many to animals

spec:
can be created only by authenticated users, can be viewed by all
extra points for "add_eater" method which allows to add an animal devouring this tree - this can be done only by admin or creator

Note you'll need to deal with writing a model. exposing it with a view with a serializer, wiring  it to url, and perhaps custom permission 

You might want to extract certain common stuff we did in fauna app to a common place for reuse

Extra extra points adding a property on the animal showing the number of AncientTrees it's connected to
"""