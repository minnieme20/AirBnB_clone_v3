#!/usr/bin/python3
"""Defines class filestorage"""
import json
import models


class FileStorage:
    """serializes and deserializes a json file"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary"""
        new_dict = {}
        if cls is None:
            return self.__objects
        if cls != "":
            for k, v in self.__objects.items():
                if cls == k.split(".")[0]:
                    new_dict[k] = v
            return new_dict
        else:
            return self.__objects

    def new(self, obj):
        """
           Set in __objects the obj with key <obj class name>.id
            Aguments:
                obj : An instance object.
        """
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        """
           Serializes __objects attribute to JSON file.
        """
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode="w", encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        """
           Deserializes the JSON file to __objects.
        """
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """deletes an obj"""
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save

    def close(self):
        """deserializes json file to objects"""
        self.reload()

    def get(self, cls, id):
        """returns an object based on class name and its ID"""
        obj_dict = self.all(cls)
        for k, v in obj_dict.items():
            matchstring = cls + "." + id
            if k == matchstring:
                return v
        return None

    def count(self, cls=None):
        """
        counts number of objects in a class (if given)
        Args:
            cls (str): class name
        Returns:
            number of objects in class, if no class name given
            return total number of objects in database
        """
        obj_dict = self.all(cls)
        return len(obj_dict)
