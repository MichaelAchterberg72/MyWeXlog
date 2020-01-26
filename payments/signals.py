from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from paypal.standard.models import PayPalStandardBase

from paypal.standard.models import ST_PP_COMPLETED, ST_PP_EXPIRED, ST_PP_PENDING
from paypal.standard.ipn.signals import valid_ipn_received

from .tasks import (
        SubscriptionAmountDifferentTask,
        SubscriptionExpiredTask,
        SubscriptionSignupTask,
        SubscriptionCancelledTask,
        SubscriptionFailedTask,
        SubscriptionUpgradeRefund,
)

# from M2Crypto import BIO, SMIME, X509
from django.conf import settings


@receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    ipn_username = User.objects.get(username=str(ipn_obj.custom))
    if ipn_obj.item_name == "WeXlog Passive Subscription":
        price = "4.00"

    elif ipn_obj.item_name == "WeXlog 6 Month Passive Subscription":
        price = "22.00"

    elif ipn_obj.item_name == "WeXlog 12 Month Passive Subscription":
        price = "43.56"

    elif ipn_obj.item_name == "WeXlog Active Subscription" | "WeXlog Active Subscription Upgrade":
        price = "5.20"

    elif ipn_obj.item_name == "WeXlog 6 Month Active Subscription" | "WeXlog 6 Month Active Subscription Upgrade":
        price = "29.20"

    elif ipn_obj.item_name == "WeXlog 12 Month Active Subscription" | "WeXlog 12 Month Active Subscription Upgrade":
        price = "57.96"

    elif ipn_obj.item_name == "WeXlog Passive Subscription - Beta":
        price = "4.00" | "0.00"

    elif ipn_obj.item_name == "WeXlog 6 Month Passive Subscription - Beta":
        price = "22.00" | "0.00"

    elif ipn_obj.item_name == "WeXlog 12 Month Passive Subscription - Beta":
        price = "43.56" | "0.00"

    elif ipn_obj.item_name == "WeXlog Active Subscription - Beta":
        price = "5.20" | "0.00"

    elif ipn_obj.item_name == "WeXlog 6 Month Active Subscription - Beta":
        price = "29.20" | "0.00"

    elif ipn_obj.item_name == "WeXlog 12 Month Active Subscription - Beta":
        price = "57.96" | "0.00"

     # check for payment received IPN
    if ipn_obj.txn_type == 'web_accept':
        if ipn_obj.payment_status == ST_PP_COMPLETED:
            # WARNING !
            # Check that the receiver email is the same we previously
            # set on the `business` field. (The user could tamper with
            # that fields on the payment form before it goes to PayPal)
            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass

            # ALSO: for the same reason, you need to check the amount
            # received, `custom` etc. are all what you expect or what
            # is allowed.

            # Undertake some action depending upon `ipn_obj`.
            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=True)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                # set passive subscription
                if ipn_obj.item_name == "WeXlog Passive Subscription" | "WeXlog Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="1")
                elif ipn_obj.item_name == "WeXlog 6 Month Passive Subscription" | "WeXlog 6 Month Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="2")
                elif ipn_obj.item_name == "WeXlog 12 Month Passive Subscription" | "WeXlog 12 Month Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="3")
                # set active subscription
                elif ipn_obj.item_name == "WeXlog Active Subscription" | "WeXlog Active Subscription Upgrade" | "WeXlog Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="1")
                elif ipn_obj.item_name == "WeXlog 6 Month Active Subscription" | "WeXlog 6 Month Subscription Upgrade" | "WeXlog 6 Month Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="2")
                elif ipn_obj.item_name == "WeXlog 12 Month Active Subscription" | "WeXlog 12 Month Active Subscription Upgrade" | "WeXlog 12 Month Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="3")
                else:
                    pass

            elif ipn_obj.mc_gross != price and ipn_obj.mc_currency != 'USD':
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")
                if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                    pass
                elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                    pass
                else:
                    SubscriptionAmountDifferentTask(ipn_username)


        elif ipn_obj.payment_status == ST_PP_EXPIRED:
            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass
            if ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")
                if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                    pass
                elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                    pass
                else:
                    SubscriptionExpiredTask(ipn_username)


        elif ipn_obj.payment_status == ST_PP_PENDING:
            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass

            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")


     # check for subscriber sign-up IPN
    elif ipn_obj.txn_type == "subscr_signup":

        if ipn_obj.payment_status == ST_PP_COMPLETED:

            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass

            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=True)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                # set passive subscription
                if ipn_obj.item_name == "WeXlog Passive Subscription" | "WeXlog Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="1")
                elif ipn_obj.item_name == "WeXlog 6 Month Passive Subscription" | "WeXlog 6 Month Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="2")
                elif ipn_obj.item_name == "WeXlog 12 Month Passive Subscription" | "WeXlog 12 Month Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="3")
                # set active subscription
                elif ipn_obj.item_name == "WeXlog Active Subscription" | "WeXlog Active Subscription Upgrade" | "WeXlog Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="1")
                elif ipn_obj.item_name == "WeXlog 6 Month Active Subscription" | "WeXlog 6 Month Subscription Upgrade" | "WeXlog 6 Month Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="2")
                elif ipn_obj.item_name == "WeXlog 12 Month Active Subscription" | "WeXlog 12 Month Active Subscription Upgrade" | "WeXlog 12 Month Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="3")
                elif ipn_obj.item_name == "WeXlog Active Subscription Upgrade" | "WeXlog 6 Month Active Subscription Upgrade" | "WeXlog 6 Month Active Subscription Upgrade":
                    SubscriptionUpgradeRefund(ipn_username)
                else:
                    pass

            elif ipn_obj.mc_gross != price and ipn_obj.mc_currency != 'USD':
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")
                if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                    pass
                elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                    pass
                else:
                    SubscriptionAmountDifferentTask(ipn_username)

        if ipn_obj.custom == ipn_username:
            SubscriptionSignupTask(ipn_username)
        else:
            pass

     # check for recurring payment IPN
    elif ipn_obj.txn_type == "recurring_payment":
        if ipn_obj.payment_status == ST_PP_COMPLETED:

            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass

            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=True)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                # set passive subscription
                if ipn_obj.item_name == "WeXlog Passive Subscription" | "WeXlog Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="1")
                elif ipn_obj.item_name == "WeXlog 6 Month Passive Subscription" | "WeXlog 6 Month Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="2")
                elif ipn_obj.item_name == "WeXlog 12 Month Passive Subscription" | "WeXlog 12 Month Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="3")
                # set active subscription
                elif ipn_obj.item_name == "WeXlog Active Subscription" | "WeXlog Active Subscription Upgrade" | "WeXlog Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="1")
                elif ipn_obj.item_name == "WeXlog 6 Month Active Subscription" | "WeXlog 6 Month Active Subscription Upgrade" | "WeXlog 6 Month Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="2")
                elif ipn_obj.item_name == "WeXlog 12 Month Active Subscription" | "WeXlog 12 Month Active Subscription Upgrade" | "WeXlog 12 Month Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="3")


            elif ipn_obj.mc_gross != price and ipn_obj.mc_currency != 'USD':
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")
                if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                    pass
                elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                    pass
                else:
                    SubscriptionAmountDifferentTask(ipn_username)


        elif ipn_obj.payment_status == ST_PP_EXPIRED:
            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass

            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")
                if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                    pass
                elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                    pass
                else:
                    SubscriptionExpiredTask(ipn_username)


        elif ipn_obj.payment_status == ST_PP_PENDING:
            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass

            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")


     # check for subscription payment IPN
    elif ipn_obj.txn_type == "subscr_payment":
        if ipn_obj.payment_status == ST_PP_COMPLETED:

            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass


            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=True)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                # set passive subscription
                if ipn_obj.item_name == "WeXlog Passive Subscription" | "WeXlog Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="1")
                elif ipn_obj.item_name == "WeXlog 6 Month Passive Subscription" | "WeXlog 6 Month Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="2")
                elif ipn_obj.item_name == "WeXlog 12 Month Passive Subscription" | "WeXlog 12 Month Passive Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="1")
                    Users.objects.filter(ipn_username).update(paid_type="3")
                # set active subscription
                elif ipn_obj.item_name == "WeXlog Active Subscription" | "WeXlog Active Subscription Upgrade" | "WeXlog Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="1")
                elif ipn_obj.item_name == "WeXlog 6 Month Active Subscription" | "WeXlog 6 Month Active Subscription Upgrade" | "WeXlog 6 Month Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="2")
                elif ipn_obj.item_name == "WeXlog 12 Month Active Subscription" | "WeXlog 12 Month Subscription Upgrade" | "WeXlog 12 Month Active Subscription - Beta":
                    Users.objects.filter(ipn_username).update(subscription="2")
                    Users.objects.filter(ipn_username).update(paid_type="3")


            elif ipn_obj.mc_gross != price and ipn_obj.mc_currency != 'USD':
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")
                if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                    pass
                elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                    pass
                else:
                    SubscriptionAmountDifferentTask(ipn_username)


        elif ipn_obj.payment_status == ST_PP_EXPIRED:
            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass

            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")
                if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                    pass
                elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                    pass
                else:
                    SubscriptionExpiredTask(ipn_username)


        elif ipn_obj.payment_status == ST_PP_PENDING:
            if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                # Not a valid payment
                pass

            elif ipn_obj.custom == ipn_username:
                Users.objects.filter(ipn_username).update(paid=False)
                Users.objects.filter(ipn_username).update(paid_date=datetime.now())
                Users.objects.filter(ipn_username).update(subscription="0")


     # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        if ipn_obj.custom == ipn_username:
            Users.objects.filter(ipn_username).update(paid=False)
            Users.objects.filter(ipn_username).update(paid_date=datetime.now())
            Users.objects.filter(ipn_username).update(subscription="0")
            if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                pass
            elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                pass
            else:
                SubscriptionFailedTask(ipn_username)
     # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        if ipn_obj.custom == ipn_username:
            Users.objects.filter(ipn_username).update(paid=False)
            Users.objects.filter(ipn_username).update(paid_date=datetime.now())
            Users.objects.filter(ipn_username).update(subscription="0")
            if CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.unsubscribe == True:
                pass
            elif CustomUserSettings.talent.filter(ipn_username) and CustomUserSettings.subscription_notifications == False:
                pass
            else:
                SubscriptionCancelledTask(ipn_username)

valid_ipn_received.connect(show_me_the_money)


class PaypalOrder(dict):
    """Acts as a dictionary which can be encrypted to Paypal's EWP service"""
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self['cert_id'] = settings.MY_CERT_ID

    def set_notify_url(self, notify_url):
        self['notify_url'] = notify_url

    # snip more wrapper functions
    def plaintext(self):
        """The plaintext for the cryptography operation."""
        s = ''
        for k in self:
            s += u'%s=%s\n' % (k, self[k])
        return s.encode('utf-8')

    __str__ = plaintext

    def encrypt(self):
        """Return the contents of this order, encrypted to Paypal's
        certificate and signed using the private key configured in the
        Django settings."""

        # Instantiate an SMIME object.
        s = SMIME.SMIME()

        # Load signer's key and cert.
        s.load_key_bio(
            BIO.openfile(settings.MY_KEYPAIR),
            BIO.openfile(settings.MY_CERT)
        )

        # Sign the buffer.
        p7 = s.sign(
            BIO.MemoryBuffer(self.plaintext()),
            flags=SMIME.PKCS7_BINARY
        )

        # Load target cert to encrypt the signed message to.
        x509 = X509.load_cert_bio(BIO.openfile(settings.PAYPAL_CERT))
        sk = X509.X509_Stack()
        sk.push(x509)
        s.set_x509_stack(sk)

        # Set cipher: 3-key triple-DES in CBC mode.
        s.set_cipher(SMIME.Cipher('des_ede3_cbc'))

        # Create a temporary buffer.
        tmp = BIO.MemoryBuffer()

        # Write the signed message into the temporary buffer.
        p7.write_der(tmp)

        # Encrypt the temporary buffer.
        p7 = s.encrypt(tmp, flags=SMIME.PKCS7_BINARY)

        # Output p7 in mail-friendly format.
        out = BIO.MemoryBuffer()
        p7.write(out)

        return out.read()
