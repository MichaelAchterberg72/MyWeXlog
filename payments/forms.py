from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.forms import PayPalEncryptedPaymentsForm
from paypal.standard.forms import PayPalSharedSecretEncryptedPaymentsForm
from django.utils.html import format_html

class ExtPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self):
        form_open  = u'''<form action="%s" id="PayPalForm" method="post">''' % (self.get_endpoint())
        form_close = u'</form>'
        # format html as you need
        submit_elm = u'''<input type="submit" class="btn btn-success my-custom-class">'''
        return format_html(form_open+self.as_p()+submit_elm+form_close)


class ExtPayPalEncryptedPaymentsForm(PayPalEncryptedPaymentsForm):
    def render(self):
        form_open  = u'''<form action="%s" id="PayPalEncryptedForm" method="post">''' % (self.get_endpoint())
        form_close = u'</form>'
        # format html as you need
        submit_elm = u'''<input type="submit" class="btn btn-success my-custom-class">'''
        return format_html(form_open+self.as_p()+submit_elm+form_close)


class ExtPayPalSharedSecretEncryptedPaymentsForm(PayPalSharedSecretEncryptedPaymentsForm):
    def render(self):
        form_open  = u'''<form action="%s" id="PayPalSharedSecretEncryptedForm" method="post">''' % (self.get_endpoint())
        form_close = u'</form>'
        # format html as you need
        submit_elm = u'''<input type="submit" class="btn btn-success my-custom-class">'''
        return format_html(form_open+self.as_p()+submit_elm+form_close)
