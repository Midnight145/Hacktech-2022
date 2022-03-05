import asyncio
from desktop_notifier import DesktopNotifier, Urgency, Button

notify = DesktopNotifier()


async def main():
    await notify.send(
        title="Focus Check!",
        message="Are you Distracted from Work?",
        urgency=Urgency.Critical,
        buttons=[
            Button(
                title="Yes!",
                on_pressed=await responseY()
            ),
            Button(
                title="No!",
                on_pressed=await responseN()
            )
        ],
        on_dismissed=lambda: main(),
        sound=True,
    )


async def responseY():
    global response
    await notify.send(title="Focus Check!", message="Get Back to Work!", urgency=Urgency.Critical)
    response = 1


async def responseN():
    global response
    await notify.send(title="Focus Check!", message="Apologies for disturbing you.", urgency=Urgency.Low)
    response = 0


def run():
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
    return response
