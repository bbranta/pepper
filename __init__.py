# -*- coding: utf-8 -*-
import sys, os
import pepper.utils

__all__ = ['Controller', 'TestCase']

from .base.controller import Controller
from .base.test_case import TestCase

__controllers = {}
__instances = {}
__classes = {}


def __init():
    global __controllers

    print 'Pepper v0.1\n'

    controllers = {}
    for f in os.listdir('app/'):
        if f.endswith('_controller.py'):
            name = f[0:-14]
            mod_name = 'app.' + f[0:-3]
            __import__(mod_name, globals(), locals(), [], -1)
            controller_class = name.capitalize() + 'Controller'
            controller_class = sys.modules[mod_name].__dict__[controller_class]
            controllers[name] = controller_class

    __controllers = controllers


def execute(*args):

    if len(args) < 1 or not args[0] in __controllers:
        print ' ! Choose one of the valid options:\n'
        for name in __controllers:
            print sys.argv[0], name, __controllers[name].__doc__
        return

    controller_name = args[0]
    controller = __controllers[controller_name]()

    if len(args) < 2 or not controller.validMethod(args[1]):
        if len(args) >= 2:
            print u' ! Error: method ' + repr(args[1]) + u' not found.\n'

        print 'Choose a valid method:'
        controller.printMethods()
        return

    controller.setMethod(args[1])
    controller.setArgs(*args[2:])
    controller.execute()


def getClass(class_name):
    global __classes

    if class_name in __classes:
        return __classes

    mod_name = 'app.' + pepper.utils.deCamelCase(class_name)
    __import__(mod_name, globals(), locals(), [], -1)
    instance_class = sys.modules[mod_name].__dict__[class_name.replace('/', '')]

    __classes[class_name] = instance_class
    return instance_class


def build(class_name):
    global __instances

    if class_name in __instances:
        return __instances[class_name]

    if class_name.endswith('Instance'):
        return False

    instance_class = getClass(class_name)
    instance = instance_class()

    __instances[class_name] = instance
    return instance


def createWrapper(class_name, *args, **kwargs):
    file_name = pepper.utils.deCamelCase(class_name)
    if os.path.exists('app/wrapper/' + file_name + '.py'):
        mod_name = 'app.wrapper.' + file_name
        __import__(mod_name, globals(), locals(), [], -1)
        instance_class = sys.modules[mod_name].__dict__['Wrapper' + class_name.replace('/', '')]

    elif os.path.exists('pepper/wrapper/' + file_name + '.py'):
        mod_name = 'pepper.wrapper.' + file_name
        __import__(mod_name, globals(), locals(), [], -1)
        instance_class = sys.modules[mod_name].__dict__['BaseWrapper' + class_name.replace('/', '')]

    else:
        raise Exception('Wrapper class not found: ' + repr(class_name))

    if 'createInstance' in dir(instance_class):
        return instance_class.createInstance(*args, **kwargs)

    instance = instance_class(*args, **kwargs)
    return instance

__init()
