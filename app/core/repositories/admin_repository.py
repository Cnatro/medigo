from abc import ABC, abstractmethod


class AdminRepository(ABC):

    @abstractmethod
    def get_dashboard_stats(self):
        pass

    @abstractmethod
    def get_weekly_appointments(self):
        pass

    @abstractmethod
    def get_top_doctors(self):
        pass

    @abstractmethod
    def get_recent_appointments(self):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_all_clinics(self):
        pass

    @abstractmethod
    def get_all_schedules(self):
        pass

    @abstractmethod
    def get_all_orders(self):
        pass

    @abstractmethod
    def get_all_payment_transactions(self):
        pass

    @abstractmethod
    def get_schedule_pending_requests(self):
        pass
