####
# Flask "app" initialization
#
# (1) Instantiate "app"
# (2) Get and register into "app" all blueprints from unhideapi.views
####
import logging
l = logging.getLogger(__name__)

# Get Flask for "app"
from flask import Flask

# Get all views
import ubcmhn.flaskapp.views as flaskappviews
from ubcmhn.util.flask import get_blueprints_from


####
# APP
####
# Generate "app" and plug all blueprints
l.debug("Creating Flask \"app\"...")
app = Flask(__name__)


####
# PLUG BLUEPRINTS
####
l.debug("Plugging Blueprints...")

for bp in get_blueprints_from(flaskappviews):
    l.debug("Registering Blueprint \"{0}\" (url={1})...".format(bp.name, bp.url_prefix))
    app.register_blueprint(bp)

l.info("Flask App fully initialized.")