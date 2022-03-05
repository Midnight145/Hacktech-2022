import asyncio
from desktop_notifier import DesktopNotifier, Urgency, Button

notify = DesktopNotifier()
response = -1


async def main():
    await notify.send(
        title="Focus Check!",
        message="Are you Distracted from Work?",
        urgency=Urgency.Critical,
        buttons=[
            Button(
                title="Yes!",
                on_pressed=responseY
            ),
            Button(
                title="No!",
                on_pressed=responseN
            )
        ],
        on_dismissed=main,
        sound=True,
    )


def responseY():
    global response
    notify.send_sync(title="Focus Check!", message="Get Back to Work!", urgency=Urgency.Critical)
    response = 1


def responseN():
    global response
    notify.send_sync(title="Focus Check!", message="Apologies for disturbing you.", urgency=Urgency.Low)
    response = 0


def run():
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
    return response
