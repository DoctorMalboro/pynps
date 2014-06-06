# -*- coding: utf-8 *-*

import unittest
from nps import transactions


class TestPayOnlineTransactionThreeSteps(unittest.TestCase):

    def test_transaction_amount(self):
        """El monto debe ser convertido a centavos."""

        url = 'http://untitest.com'
        secret = 'topsecret'
        merchant_id = 'unittest'
        transaction = transactions.PayOnlineTransactionThreeSteps(url, merchant_id, secret)

        transaction.request.psp_Amount = '105.05'
        self.assertEquals(transaction.request.psp_Amount, '10505')
        transaction.request.psp_Amount = '105,05'
        self.assertEquals(transaction.request.psp_Amount, '10505')
        transaction.request.psp_Amount = '105.05'
        self.assertEquals(transaction.request.items.get('psp_Amount'), '10505')


if __name__ == '__main__':
    unittest.main()

