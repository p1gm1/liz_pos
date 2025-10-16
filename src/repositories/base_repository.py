from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

from sqlalchemy.orm import Session

from src.utils.logger import Logger

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    def __init__(self, session: Session):
        self.session = session
        self.logger = Logger(self.__class__.__name__).get_logger()
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
