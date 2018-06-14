from random import randint


class RandomSink():

    @classmethod
    def get_emails(cls, amount):
        emails = []
        for i in range(0, amount):
            emails.append("{}@sink.sendgrid.net".format(cls.random_letters()))
        return emails

    @classmethod
    def random_letters(cls):
        string = ""

        for i in range(0, 10):
            string += chr(randint(97, 122))

        return string
