from lib.event import Event


class UserAdded(Event):
    email: str

    def __hash__(self):
        return hash(self.email)


class OTPSent(Event):
    phone_number: str
    email: str
    otp: str

    def __hash__(self):
        return hash(self.phone_number + self.email)


class ForgetPasswordEvent(Event):
    email: str

    def __hash__(self):
        return hash(self.email)
