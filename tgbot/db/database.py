from gino import Gino
from gino.schema import GinoSchemaVisitor

db = Gino()


async def create_db(config):
    await db.set_bind(f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}")
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
