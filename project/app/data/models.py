"""OOP Models for Data (Week 11).

This module provides object-oriented data models for the application.
References Week 11 OOP principles: encapsulation, inheritance, polymorphism.
"""

from datetime import datetime
from typing import Optional


class Entity:
    """Base class for all entities in the system.
    
    Demonstrates inheritance and encapsulation patterns from Week 11.
    """
    
    def __init__(self, entity_id: int, name: str, created_at: Optional[datetime] = None):
        """Initialize an Entity.
        
        Args:
            entity_id: Unique identifier
            name: Entity name
            created_at: Creation timestamp
            
        Raises:
            ValueError: If entity_id is not positive or name is empty
            TypeError: If entity_id is not an integer
        """
        if not isinstance(entity_id, int) or entity_id <= 0:
            raise ValueError("Entity ID must be a positive integer")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        
        self.__entity_id = entity_id
        self.__name = name.strip()
        self.__created_at = created_at or datetime.now()
    
    def get_id(self) -> int:
        """Get the entity ID."""
        return self.__entity_id
    
    def get_name(self) -> str:
        """Get the entity name."""
        return self.__name
    
    def get_created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self.__created_at
    
    def __str__(self) -> str:
        """String representation of the entity."""
        return f"{self.__class__.__name__}(id={self.__entity_id}, name={self.__name})"


class User(Entity):
    """User entity representing an application user.
    
    Inherits from Entity and adds user-specific attributes.
    Demonstrates inheritance from Week 11.
    """
    
    def __init__(self, user_id: int, username: str, email: str, role: str = "user"):
        """Initialize a User.
        
        Args:
            user_id: Unique user identifier
            username: Username
            email: Email address
            role: User role (default: "user")
            
        Raises:
            ValueError: If email or role are invalid
        """
        super().__init__(user_id, username)
        
        if not isinstance(email, str) or "@" not in email:
            raise ValueError("Email must be a valid email address")
        if not isinstance(role, str) or role not in ["user", "admin", "analyst"]:
            raise ValueError("Role must be 'user', 'admin', or 'analyst'")
        
        self.__email = email.strip()
        self.__role = role.strip()
        self.__login_count = 0
    
    def get_email(self) -> str:
        """Get the user's email."""
        return self.__email
    
    def get_role(self) -> str:
        """Get the user's role."""
        return self.__role
    
    def get_login_count(self) -> int:
        """Get the number of logins."""
        return self.__login_count
    
    def record_login(self) -> None:
        """Record a login event."""
        self.__login_count += 1
    
    def __str__(self) -> str:
        """String representation of the user."""
        return f"User({self.get_name()}, role={self.__role}, logins={self.__login_count})"


class AnalyticsRecord(Entity):
    """Analytics record for tracking analytical events.
    
    Inherits from Entity and demonstrates polymorphism.
    """
    
    def __init__(self, record_id: int, title: str, metric_type: str, value: float):
        """Initialize an AnalyticsRecord.
        
        Args:
            record_id: Unique record identifier
            title: Record title
            metric_type: Type of metric
            value: Metric value
            
        Raises:
            ValueError: If metric_type is invalid or value is not numeric
        """
        super().__init__(record_id, title)
        
        if not isinstance(metric_type, str) or not metric_type.strip():
            raise ValueError("Metric type must be a non-empty string")
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be numeric")
        
        self.__metric_type = metric_type.strip()
        self.__value = float(value)
    
    def get_metric_type(self) -> str:
        """Get the metric type."""
        return self.__metric_type
    
    def get_value(self) -> float:
        """Get the metric value."""
        return self.__value
    
    def __str__(self) -> str:
        """String representation of the record."""
        return f"AnalyticsRecord({self.get_name()}: {self.__value} {self.__metric_type})"
