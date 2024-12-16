##############################################################################
#
# Bремя/Vremya v24.12.1 - A simple and easy-to-use library to scheduler things 
#               (https://github.com/viniciuscruzmoura)
# 
# Usage:
#   import vremya
#   vremya.SimpleScheduler([
#       ("apps.example.module", "example_foo1", "06:00", ()),
#       ("apps.example.module", "example_foo2", "15:46", ("arg1", "arg2")),
#   ])
#
# DEPENDENCIES (included):
#   sched (https://docs.python.org/3/library/sched.html)
#   time (https://docs.python.org/3/library/time.html)
#   threading (https://docs.python.org/3/library/threading.html)
#   os (https://docs.python.org/3/library/os.html)
#   traceback (https://docs.python.org/3/library/traceback.html)
#   importlib (https://docs.python.org/3/library/importlib.html)
#
# LICENSE: MIT license
#
# Copyright (c) 2024 Vinícius Moura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################

class VremyaScheduler():
    import sched
    import time
    import threading
    import os
    import traceback
    import importlib
    import json

    def __init__(self, tasks):
        if self.os.environ.get("vremya_enabled", "1") != "1":
            return
        self.os.environ["vremya_enabled"] = "0"
        print("Scheduler Init : ")
        filtred_tasks = []
        for t in tasks:
            try:
                module_name, function_name, sch_timer, func_args = t
                now_hr, now_minute = map(int, self.time.strftime("%H %M").split())
                task_hr, task_minute = map(int, sch_timer.split(":"))
                if now_hr == task_hr and now_minute == task_minute:
                    func_obj = getattr(
                            self.importlib.import_module(module_name), 
                            function_name)
                filtred_tasks.append(t)
                print("Event scheduled:", module_name, function_name, sch_timer, func_args)
            except Exception as err:
                print("FATAL: invalid task configuration:\n", t, "\n", err)
        self.tasks = filtred_tasks
        self.scheduler = self.sched.scheduler(self.time.time, self.time.sleep)
        self.threading.Thread(target=self.start,
                         kwargs={}, 
                         daemon=False).start()

    def start(self):
        while True:
            try:
                self.events()
                self.scheduler.run()
            except Exception as err:
                self.traceback.print_exc()

    def events(self):
        for module_name, function_name, sch_timer, func_args in self.tasks:
            try:
                now_hr, now_minute = map(int, self.time.strftime("%H %M").split())
                task_hr, task_minute = map(int, sch_timer.split(":"))
                if now_hr == task_hr and now_minute == task_minute:
                    print("Event scheduled",
                          "MODULE:", module_name, 
                          "FUNCTION:", function_name, 
                          "TIMER:", sch_timer)
                    func_obj = getattr(
                            self.importlib.import_module(module_name), 
                            function_name)
                    self.scheduler.enter(60, 1, func_obj, func_args)
            except Exception as err:
                self.traceback.print_exc()
