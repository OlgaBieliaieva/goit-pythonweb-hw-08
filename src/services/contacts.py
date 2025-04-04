from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contact import ContactSchema, ContactUpdateSchema


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactSchema):
        return await self.contact_repository.create_contact(body)

    async def get_contacts(self, first_name: Optional[str], 
        last_name: Optional[str], 
        email: Optional[str], 
        limit: int, 
        offset: int):
        return await self.contact_repository.get_contacts(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            limit=limit, 
            offset=offset
        )

    async def get_contacts_by_upcoming_birthdays(
        self, 
        limit: int = 10, 
        offset: int = 0
    ):
        return await self.contact_repository.get_contacts_by_upcoming_birthdays(
            limit=limit, 
            offset=offset
        )

    async def get_contact(self, contact_id: int):
        return await self.contact_repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactUpdateSchema):
        return await self.contact_repository.update_contact(contact_id, body)    

    async def remove_contact(self, contact_id: int):
        return await self.contact_repository.remove_contact(contact_id)