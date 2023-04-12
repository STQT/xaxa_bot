import asyncio
import os
import openpyxl

from gino import Gino
from gino.schema import GinoSchemaVisitor

from tgbot.config import load_config
from tgbot.db.models import Market


config = load_config(".env")


async def runn():
    for filename in os.listdir("files"):
        f = os.path.join("files", filename)
        print(f)
        book = openpyxl.load_workbook(str(f), read_only=True)
        sheet = book.active
        row_count = len([row for row in sheet if not all([cell.value is None for cell in row])])
        for i in range(1, row_count + 1):
            print(f"{i}.{filename} {sheet[f'B{i}'].value}")
            await Market.create(name_uz=str(sheet[f"B{i}"].value), region=filename.replace(".xlsx", ""), address=str(sheet[f"C{i}"].value), type=str(sheet[f"D{i}"].value), activity=str(sheet[f"E{i}"].value), number=str(sheet[f"F{i}"].value))


