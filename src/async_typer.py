import asyncio
import inspect
import logging
from functools import partial, wraps

import typer


class AsyncTyper(typer.Typer):
    @staticmethod
    def maybe_run_async(decorator, f):
        if inspect.iscoroutinefunction(f):

            async def run_and_complete_tasks(*args, **kwargs):
                ret_val = await f(*args, **kwargs)
                try:
                    tasks = asyncio.all_tasks()
                    main_task = asyncio.tasks.current_task()
                    if main_task:
                        remaining_tasks = [
                            task
                            for task in tasks
                            if task.get_name() != main_task.get_name()
                        ]
                        await asyncio.gather(*remaining_tasks)
                except Exception as e:
                    logging.error(f"Error running async tasks: {e}")
                return ret_val

            @wraps(f)
            def runner(*args, **kwargs):
                return asyncio.run(run_and_complete_tasks(*args, **kwargs))

            decorator(runner)
        else:
            decorator(f)
        return f

    def callback(self, *args, **kwargs):
        decorator = super().callback(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)

    def command(self, *args, **kwargs):
        decorator = super().command(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)
