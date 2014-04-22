from talent_match import app, db
from config import basedir
import os.path
import logging

logging.basicConfig(
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Create the db if it doesn't exist
if not os.path.exists(os.path.join(basedir, 'talent-match.db')):
	logger.info("Creating database...")
	db.create_all()

app.testLoadFunction()

app.run(debug=True)
