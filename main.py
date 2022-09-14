import os
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional
from sqlalchemy import select
from datetime import datetime, date
import pyMultiSerial as p

ms = p.MultiSerial()
ms.baudrate = 9600
ms.timeout = 0

load_dotenv()

class Tag(SQLModel, table = True):
    """Skapar bordet 'Tag' i databasen"""
    id: Optional[int] = Field(default = None, primary_key = True)
    tag_id: str
    valid: bool

class Scan(SQLModel, table = True):
    """Skapar bordet 'Scan' i databasen"""
    id: Optional[int] = Field(default = None, primary_key = True)
    tag_id: str
    date: str
    time: str

sqlite_file_name = os.getenv("DB_NAME")
sqlite_url = os.getenv("DB_URL")

engine = create_engine(sqlite_url, echo = False) # Skapar en engine som tillåter interaktion med databasen
SQLModel.metadata.create_all(engine)

def register(uid):
    """Lägger till en tagg i bordet 'Tag', där den räknas som registrerad och känd"""
    session = Session(engine)
    session.add(Tag(tag_id = uid, valid = True))
    session.commit()

def scan(uid):
    """Lägger till en skanning med en registrerad tagg i bordet 'Scan', inklusive datum och tid"""
    session = Session(engine)
    session.add(Scan(tag_id = uid, date = today, time = ctime))
    session.commit()


today = date.today().strftime("%d/%m/%y")
ctime = datetime.now().time().strftime("%H:%M:%S")

registering = bool
is_valid = bool

def check(comm, obj, uid):
    """Om användaren vill registrera, kollar den om taggen redan finns. 
    Om inte kollar den om taggen redan har blivit skannad idag"""
    if registering:
        with Session(engine) as session:
            statement = select(Tag).where(Tag.tag_id == uid)
            results = session.exec(statement)
            for tag in results:
                print("En tagg med den här UID finns redan.")
                return
            print(f"Lade till taggen med UID: {uid}")
            register(uid)  
    else:
        with Session(engine) as session:
            valid_statement = select(Tag).where(Tag.tag_id == uid and Tag.valid == True)
            valid_result = session.exec(valid_statement)
            is_valid = False
            for tag in valid_result:
                is_valid = True
            if is_valid:
                statement = select(Scan).where(Scan.tag_id == uid and Scan.date == today)
                results = session.exec(statement)
                for i in results:
                    print("Du har redan tagit lunch idag :p")
                    return
                print(f"Varsågod, du får en lunch! :D")
                scan(uid)
            else:
                print("Taggen är inte registrerad.")

def count(date):
    """Räknar antal skanningar som skedde under givna datumet"""
    total = 0
    with Session(engine) as session:
        statement = select(Scan).where(Scan.date == date)
        results = session.exec(statement)
        for scan in results:
            total += 1
        print(f"----------\nDet skedde {total} skanningar under {date}")

print('----------\n1. Skanna\n2. Registrera\n3. Räkna skanningar\n----------')
user_input = int(input("Välj: ")) # Frågar användaren vad de vill göra med skriptet
print("----------")

if user_input == 1:
    registering = False
elif user_input == 2:
    registering = True
elif user_input == 3:
    count(str(input("Skriv datum (DD/MM/ÅÅ): ")))

ms.port_read_callback = check
ms.Start()
