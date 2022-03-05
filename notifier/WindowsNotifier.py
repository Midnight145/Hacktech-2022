import multiprocessing

import zroya
from multiprocessing import Process, Lock

mutex = Lock()
notif_done = multiprocessing.Event()

zroya.init(
    app_name="Focus Checker",
    company_name="Code Monkeys",
    product_name="Notifier",
    sub_product="Windows_Notifier",
    version="v01"
)

notifier = zroya.Template(zroya.TemplateType.Text2)
notifier.setFirstLine("Focus Check!")
notifier.setSecondLine("Are you Distracted from Work?")

notifier.addAction("Yes!")
notifier.addAction("No!")

responseY = zroya.Template(zroya.TemplateType.Text1)
responseY.setFirstLine("Get Back to Work!")

responseN = zroya.Template(zroya.TemplateType.Text1)
responseN.setFirstLine("Apologies for disturbing you.")
responseN.setAudio(audio=zroya.Audio.IM, mode=zroya.AudioMode.Silence)


def onAction(nid, action_id):
    global responseY, responseN, response

    if action_id == 0:
        zroya.show(responseY)
        response = 1
    else:
        zroya.show(responseN)
        response = 0

    notif_done.set()


def onDismiss(nid, action_id):
    notifier.setSecondLine("Were you distracted?")
    zroya.show(notifier, on_action=onAction, on_dismiss=onDismiss)


def run():
    with mutex:
        zroya.show(notifier, on_action=onAction, on_dismiss=onDismiss)
        notif_done.wait()
        return response


def notify():
    proc = Process(target=run)
    proc.start()