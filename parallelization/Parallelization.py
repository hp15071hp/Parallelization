# -*- coding: utf-8 -*-
'''
Created on 2014/4/18
@author: Ivy Liu
'''

import threading
import time
from robot.libraries.BuiltIn import BuiltIn
from robot.errors import ExecutionFailed, ExecutionPassed, ExecutionFailures

_errors = []
_condition = threading.Condition()

class Parallelization:
    
    global _errors    
    _threads = []

    def run_async(self, keyword, *arg):
        """
        Creates a new thread to execute the given keywords, then return this thread.
		
		If you need to wait until the thread, you can use the Wait Until and returned thread to wait for action.
        
        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | ${thread2} | Run Async | My Keyword 2 | arg2 |
        | Wait Until | ${thread1} | ${thread2} |
        
		Starting from Robot Framework 2.7.6, keywords can also be run with arguments using upper case `AND` as a separator between keywords.
		
		If you need to execute the given keywords in a sequence in one thread, you can use the Run Keywords and `AND` to combine keywords.
                        
        Examples:
        | ${thread1} | Run Async | Run Keywords | My Keyword 1 | arg1 | AND | My Keyword 2 |
        | ${thread2} | Run Async | My Keyword 3 | arg3 |
        | Wait Until | ${thread1} | ${thread2} |
        """
        thread = ExecuteKeywordThread(keyword, *arg)
        thread.setDaemon(True)
        thread.start()
        time.sleep(1)
        self._threads.append(thread)
            
        return thread

    def wait_until(self, *threads):
        """
        Waits until the specified threads before continuing to do the next action.

        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | Wait Until | ${thread1} |

        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | ${thread2} | Run Async | My Keyword 2 | arg2 |
        | ${thread3} | Run Async | My Keyword 3 | arg3 |
        | Wait Until | ${thread1} | ${thread2} | ${thread3} |
        """
        for thread in threads :
            thread.join()
            time.sleep(1)

        if _errors:
            raise ExecutionFailures(_errors)
        
        _errors[:] = []
        self._threads[:] = []
    
    def stop_async_tasks(self, *threads):
        """
        Forces stop the specified threads.

        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | ${thread2} | Run Async | My Keyword 2 | arg2 |
        | ${thread3} | Run Async | My Keyword 3 | arg3 |
        | Stop Async Tasks | ${thread1} | ${thread2} | ${thread3} |
        """
        for thread in threads :
            thread.stop()
            time.sleep(1)
            
    def stop_all_async_tasks(self):
        """
        Forces stop all of the threads is executed.

        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | ${thread2} | Run Async | My Keyword 2 | arg2 |
        | ${thread3} | Run Async | My Keyword 3 | arg3 |
        | Stop All Async Tasks |
        """
        for thread in self._threads :
            thread.stop()
            time.sleep(1)
            
    def is_alive(self, thread):
        """
        Checks the specified thread is still running or not.
		
		This keyword returns `True` if the thread that is still running and `False` if it stop.

        Examples:
        | ${thread1} | Run Async | My Keyword 1 |
        | ${is_alive} | Is Alive | ${thread1} |
        """
        return thread.is_alive()

class ExecuteKeywordThread(threading.Thread):

    global _errors, _condition
    
    @property
    def _builtin_lib(self):
        return self._builtin.get_library_instance('BuiltIn')
    
    def __init__(self, keyword, *arg):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.arg = arg
        self._builtin = BuiltIn()
        self._stop = threading.Event()
        
    def run(self):
        try:
            self._builtin_lib.run_keyword(self.keyword, *self.arg)

        except ExecutionPassed, err:
            err.set_earlier_failures(_errors)
            raise err
        except ExecutionFailed, err:
            if _condition.acquire():
                _errors.extend(err.get_errors())
                _condition.notify()
                _condition.release()
            else :
                _condition.wait()
                _errors.extend(err.get_errors())
                _condition.notify()
        
    def stop(self):
        self._stop.set()
        self._Thread__stop()