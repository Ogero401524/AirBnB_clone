#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all hbnb models"""

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if kwargs:
            # Convert datetime strings back to datetime objects if present
            self.id = kwargs.get('id', str(uuid.uuid4()))
            created = kwargs.get('created_at')
            updated = kwargs.get('updated_at')

            self.created_at = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f') if created else datetime.now()
            self.updated_at = datetime.strptime(updated, '%Y-%m-%dT%H:%M:%S.%f') if updated else datetime.now()

            # Remove __class__ if it exists, then update __dict__
            kwargs.pop('__class__', None)
            for key, value in kwargs.items():
                if key not in ['created_at', 'updated_at', 'id']:
                    setattr(self, key, value)
        else:
            # Default initialization
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            # Register the new instance with storage
            from models import storage
            storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls_name = self.__class__.__name__
        return f'[{cls_name}] ({self.id}) {self.__dict__}'

    def save(self):
        """Updates updated_at with current time and saves to storage"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance suitable for serialization"""
        dictionary = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')  # Skip private/internal attributes
        }
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def __eq__(self, other):
        """Defines equality comparison by object ID"""
        return isinstance(other, BaseModel) and self.id == other.id
