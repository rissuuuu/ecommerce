import logging
from typing import Union

from entrypoint.messagebus import commands_events_mappings
from lib import command, event, unit_of_work

logger = logging.getLogger("werkzeug")

Message = Union[command.Command, event.Event]


async def handle(message: Message, uow: unit_of_work.SqlAlchemyUnitOfWork):
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, event.Event):
            await handle_event(message, uow, queue)
        elif isinstance(message, command.Command):
            cmd_res = await handle_command(message, uow, queue)
            results.append(cmd_res)
        else:
            raise Exception(f"{message} was not an Event or Command")
    return results


async def handle_event(
    events: event.Event,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
    queue,
):
    handler = commands_events_mappings.EVENT_HANDLERS[type(events)]
    try:
        logger.debug("handling event %s with handler %s", event, handler)
        await handler(events)
        queue.extend(uow.collect_new_events())
    except Exception:
        logger.exception("Exception handling event %s", event)
        raise


async def handle_command(
    command: command.Command,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
    queue,
):
    logger.debug("handling command %s", command)
    try:
        handler = commands_events_mappings.COMMAND_HANDLERS[type(command)]
        result = await handler(command, uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise
