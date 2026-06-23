import uuid
import random

from faker import Faker

from datetime import datetime
from datetime import timedelta

from sqlalchemy import insert

from app.database import engine

from app.models import Product

fake = Faker()

TOTAL = 200000

BATCH = 10000

categories = [

    "electronics",

    "fashion",

    "books",

    "sports",

    "home",

    "beauty"

]

for start in range(

    0,

    TOTAL,

    BATCH

):

    rows = []

    for _ in range(BATCH):

        created = datetime.now() - timedelta(

            days=random.randint(0, 365)

        )

        updated = created + timedelta(

            days=random.randint(0, 30)

        )

        rows.append({

            "id": str(uuid.uuid4()),

            "name": fake.word(),

            "category": random.choice(categories),

            "price": round(

                random.uniform(

                    100,

                    50000

                ),

                2

            ),

            "created_at": created,

            "updated_at": updated

        })

    with engine.begin() as conn:

        conn.execute(

            insert(Product),

            rows

        )

    print(

        f"Inserted {start+BATCH}"

    )

print("Done")