from future.utils import with_metaclass
from abc import ABCMeta, abstractmethod


class ApiInterface(with_metaclass(ABCMeta)):
    @abstractmethod
    def search(self, query): pass
