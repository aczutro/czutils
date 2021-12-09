# Copyright (C) 2021 - present  Alexander Czutro <github@czutro.ch>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# For more details, see the provided licence file or
# <http://www.gnu.org/licenses>.
#
################################################################### aczutro ###

"""Base classes for asynchronous components that run in their own thread."""

from .czlogging import *
from .czcode import autoStr
import queue
import threading
import typing


_logger = LoggingChannel("czutils.utils.czthreading",
                         LoggingLevel.SILENT,
                         colour=True)

def setLoggingOptions(level: int, colour = True) -> None:
    """
    Sets this module's logging level.  If not called, the logging level is
    SILENT.

    :param level: One of the following:
                  - czlogging.LoggingLevel.INFO
                  - czlogging.LoggingLevel.WARNING
                  - czlogging.LoggingLevel.ERROR
                  - czlogging.LoggingLevel.SILENT

    :param colour: If true, use colour in log headers.
    """
    global _logger
    _logger = LoggingChannel("czutils.utils.czthreading", level, colour=colour)

#setLoggingOptions


@autoStr
class Message:
    """
    Base class for messages passed between threads.
    """

    def msgType(self) -> str:
        """
        Do NOT override this method.  It is used by class ReactiveThread to
        determine how to process the message.

        :returns: this object's class name.
        """
        return type(self).__name__
    #msgType

#Message


class QuitMessage(Message):
    """
    Message that makes class ReactiveThread quit the message-receiving loop.
    """
    pass
#QuitMessage


class Thread:
    """
    Base class for an asynchronous component.
    When start() is called, method threadCode()
    is executed in a separate thread.

    This class uses the module's logger.  Set the logging level and whether to
    use colour with setLoggingOptions(level, colour={True|False}).
    """

    def __init__(self, name: str):
        """
        Constructor.

        :param name: The thread's name.
        """
        super().__init__()
        self._name = name
        self._running = False
        self._thread = None
        self._lock = threading.Lock()
    #__init__


    def name(self) -> str:
        """
        :returns: the thread's name.
        """
        return self._name
    #name


    def threadCode(self) -> None:
        """
        DO override this method.  This is where the functionality that shall
        run in a separate thread is to be implemented.
        """
        pass
    #threadCode


    def running(self) -> bool:
        """
        :returns: the current value of the running flag.
        """
        return self._running
    #running


    def start(self) -> None:
        """
        Starts the execution of threadCode(), sets the running flag to True,
        and returns immediately.  threadCode() will continue to run in a
        separate thread.

        If threadCode() is already running, does nothing.
        """
        self._lock.acquire()
        if self._running:
            _logger.warning("thread", self._name, "already running")
        else:
            self._running = True
            self._thread = threading.Thread(target = self._threadCode,
                                            name = self._name,
                                            daemon = True)
            self._thread.start()
        #else
        self._lock.release()
    #start


    def stop(self) -> None:
        """
        Sets the running flag to False and waits for threadCode() to return.
        It is your responsibility to implement code in threadCode() that
        checks whether a stop has been requested.

        Will block for ever if threadCode() doesn't return.  However, if
        threadCode is NOT running (because not started or already finished),
        returns immediately without blocking.
        """
        self._lock.acquire()
        if self._running and self._thread is not None:
            self._running = False
            self._thread.join()
            self._thread = None
        #if
        self._lock.release()
    #stop


    def wait(self) -> None:
        """
        Waits for threadCode to return, but does not request a stop.

        Will block for ever if threadCode() doesn't return.  However, if
        threadCode is NOT running (because not started or already finished),
        returns immediately without blocking.
        """
        self._lock.acquire()
        if self._running and self._thread is not None:
            self._thread.join()
            self._thread = None
        #if
        self._lock.release()
    #wait


    def _threadCode(self):
        try:
            _logger.info("starting thread '%s'" % self._name)
            self.threadCode()
            self._running = False
            _logger.info("terminating thread '%s'" % self._name)
        except Exception as e:
            _logger.error("exception in thread '%s'" % self._name, e)
            raise e
        #except
    #_threadCode

#Thread


class ReactiveThread(Thread):
    """
    Base class for an asynchronous component with a standard infinite loop for
    message processing.

    The component waits for incoming messages and processes them serially (in
    receival order) until either a QuitMessage is received, or until
    the running flag is set to False (e.g. call to stop()).
    Note that if the running flag is set to False, the loop is exited as soon as
    possible, so some queued messages may remain unprocessed.

    The right way to derive from this class is to define a method for each class
    of messages that may be sent to the component, for example:

        def processSomeMsgClass(message: SomeMsgClass) -> None:
            ...

    where SomeMsgClass derives from Message.

    Then, register those message processing methods by calling
    addMessageProcessor in __init__, for example:

        self.addMessageProcessor("SomeMsgClass", self.processSomeMsgClass)

    This class uses the module's logger.  Set the logging level and whether to
    use colour with setLoggingOptions(level, colour={True|False}).
    """

    def __init__(self, name: str, messageWaitingTime: float):
        """
        Constructor.

        :param name:               The thread's name.

        :param messageWaitingTime: Maximum time in seconds to wait for the next
                                   message.  If None, wait for ever.
                                   (However, that will block the component if no
                                   messages arrive.)
                                   This is a performance parameter only.
                                   Messages are NEVER dropped and ALWAYS
                                   processed as soon as possible.
                                   If this parameter's value is too small,
                                   it may result in busy waiting.
        """
        super().__init__(name)
        self._messageWaitingTime = messageWaitingTime
        self._messageProcessor = dict()
        self._messages = queue.Queue()
    #__init__


    def addMessageProcessor(self,
                            messageType: str,
                            method: typing.Callable[[Message], None]) -> None:
        """
        Register a message processor, i.e. a method that will be used to process
        messages of a particular class.

        Use this method only within __init__.

        :param messageType: The message's class name.

        :param method:      A method that takes a message of the class in
                            question and returns None.  May be a static
                            function.
        """
        self._messageProcessor[messageType] = method
    #addMessageProcessor


    def comm(self, message: Message) -> None:
        """
        Queues up a message and returns immediately.

        :param message: An instance of a class derived from Message.
        """
        self._messages.put(message, block = True, timeout = None)
    #comm


    def threadCodePre(self) -> None:
        """
        Override this method to implement code that needs to be executed
        once BEFORE the message processing loop.
        """
        pass
    #threadCodePre


    def threadCodePost(self) -> None:
        """
        Override this method to implement code that needs to be executed
        once AFTER the message processing loop.
        """
        pass
    #threadCodePost


    def threadCode(self) -> None:
        """
        Do NOT override this method.
        This is where the message processing loop is implemented.
        """
        self.threadCodePre()
        while self._running:
            try:
                message = self._messages.get(block = True,
                                             timeout = self._messageWaitingTime)
                messageType = message.msgType()
                _logger.info("%s: received message of type %s"
                             % (self.name(), messageType))
                if messageType == "QuitMessage":
                    _logger.info("%s: received QuitMessage" % self.name())
                    break
                else:
                    try:
                        self._messageProcessor[messageType](message)
                    except KeyError:
                        _logger.warning(
                            "%s: don't know what to do with messages of type %s"
                            % (self.name(), messageType))
                    #except
                #else
            except queue.Empty:
                pass
            #except
        #while
        self.threadCodePost()
    #threadCode

#ReactiveThread


### aczutro ###################################################################
