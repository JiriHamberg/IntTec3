"""
Base class for game framework modules.
"""


import abc


class BaseModule:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def tick(self, event):
        """
        This method is being called by the framework for every new record of gaze data.
        :param event: Gaze-event from eyetracker
        """
