import logging
from typing import Sequence
from datetime import datetime, timedelta

from sqlalchemy import select, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.contact_model import Contact_model
from src.schemas.contact import ContactSchema, ContactUpdateSchema

logger = logging.getLogger("uvicorn.error")


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, limit: int, offset: int, first_name: str = None, last_name: str = None, email: str = None) -> Sequence[Contact_model]:
        filters = []
        
        if first_name:
            filters.append(Contact_model.first_name.ilike(f"%{first_name}%"))
        
        if last_name:
            filters.append(Contact_model.last_name.ilike(f"%{last_name}%"))
        
        if email:
            filters.append(Contact_model.email.ilike(f"%{email}%"))
        
        stmt = select(Contact_model).filter(and_(*filters)).offset(offset).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contacts_by_upcoming_birthdays(
        self, limit: int = 10, offset: int = 0
    ) -> list[Contact_model]:
        today = datetime.now()
        current_month = today.month
        current_day = today.day   
        upcoming_birthday_end = today + timedelta(days=7)

        stmt = select(Contact_model).filter(           
            extract('month', Contact_model.birth_date) == current_month,
            extract('day', Contact_model.birth_date) >= current_day,
            extract('day', Contact_model.birth_date) <= upcoming_birthday_end.day,
        ).order_by(Contact_model.birth_date).offset(offset).limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact_model | None:
        stmt = select(Contact_model).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactSchema) -> Contact_model:
        contact = Contact_model(**body.model_dump())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> Contact_model | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdateSchema):
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            update_data = body.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact