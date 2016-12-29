from django.core.exceptions import ValidationError

BADWORDS = ("caca", "culo", "pis", "pito", "meao")

#esto es un validador de django:
# TODO: make this works with content and with introduction
def badwords(text):
    """
    Validate content without barwords
    :param text: text to validate
    :return: nothing, a validator only raise an error if this is the case
    """
    for badword in BADWORDS:
        if badword in text:
            raise ValidationError("la palabra {0} no está permitida".format(badword))