from datetime import datetime

from fastapi import APIRouter, Depends

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from .database import get_db
from .models import Product

router = APIRouter()


@router.get("/products")
def get_products(
    limit: int = 20,
    category: str | None = None,
    cursor_updated_at: str | None = None,
    cursor_id: str | None = None,
    db: Session = Depends(get_db),
):

    query = db.query(Product)

    if category:
        query = query.filter(
            Product.category == category
        )

    if cursor_updated_at and cursor_id:

        cursor_updated_at = datetime.fromisoformat(
            cursor_updated_at
        )

        query = query.filter(

            or_(

                Product.updated_at < cursor_updated_at,

                and_(

                    Product.updated_at
                    == cursor_updated_at,

                    Product.id < cursor_id

                )

            )

        )

    products = query.order_by(

        Product.updated_at.desc(),

        Product.id.desc()

    ).limit(limit).all()

    next_cursor = None

    if products:

        last = products[-1]

        next_cursor = {

            "updated_at": last.updated_at.isoformat(),

            "id": last.id

        }

    return {

        "count": len(products),

        "next_cursor": next_cursor,

        "data": [

            {

                "id": p.id,

                "name": p.name,

                "category": p.category,

                "price": float(p.price),

                "created_at": p.created_at,

                "updated_at": p.updated_at,

            }

            for p in products

        ]

    }