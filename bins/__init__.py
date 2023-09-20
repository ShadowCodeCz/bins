from .v1 import app as app_v1
from .v2 import app as app_v2


def run_v1():
    app_v1.run()

# TODO: frameless presentation mode (black / white)
# TODO: inject form
# TODO: Double click on bit -> flip value
def run_v2():
    app_v2.run()