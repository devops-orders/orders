"""
Test Factory to make fake objects for testing
"""
import factory
import uuid
from factory.fuzzy import FuzzyChoice
from service.models import Order

class OrderFactory(factory.Factory):
    """ Creates fake order that you don't have to feed """
    class Meta:
        model = Order
    id = factory.Sequence(lambda n: n)
    uuid = str(uuid.uuid4())
    product_id = 2
    customer_id = 1
    price = 20
    quantity = 1
    status = 'In Progress'

if __name__ == '__main__':
    for _ in range(10):
        order = OrderFactory()
        print(order.serialize())