from .variables import UOS_Variables

class Data:
    def __init__(self, text,
                 interval = -1,
                 sound = ['typing multiple'],
                 newline = True,
                 insert_after = None,
                 update_after = None):

        self.text = text
        self.sound = sound
        self.newline = newline
        self.interval = interval
        self.insert_after = insert_after
        self.update_after = update_after

class UOS_Data:
    intro = (Data([
    "The ROBCO Model E-330 is the most reliable client terminal ever developed.",
    "Finally, a personalized home computer",
    "for the whole family to enjoy!",
    "",
    "    Keep track of activities and tasks, ",
    "    and maintain privacy.",
    "    by adding passwords to logins.*",
    "",
    "    When connected to a ROBCO-brand Mainframe,",
    "    stay organized and on the ball with our",
    "        - state-of-the-art calendar",
    "        - contact manager",
    "        - messaging system!*",
    "",
    "* No users detected. Type \"SETUP\" to create an account.",
    "* No network connection." ]), )

    loading = (Data([
    "Initializing RobCo Industries(TM) MF Boot Agent v2.3.0",
    "RETROS BIOS",
    "RBIOS-4.02.08.00 52EE5.E7.E8",
    "COPYRIGHT 2075-2077 ROBCO INDUSTRIES",
    "Uppermem: 64 KB",
    "Root (5AB)",
    "Production Mode",
    ""
    ]),

    Data([["Intitializing  ", ". . . . ."]], (-1, 100), ["hard drive", "typing multiple"]),
    Data([["[  ] Checking LOG.F  ", ". . . ."]], (-1, 100), ["hard drive", "typing multiple"],
         insert_after=(0, 1, 'OK')),
    Data([["[  ] Loading ACCOUNTS.F  ", ". ."]], (-1, 100), ["hard drive", "typing multiple"],
         insert_after=(0, 1, 'OK')),
    Data(["", "Done!"]))
