from collections import namedtuple

ORDER_STATUSES = namedtuple('ORDER_STATUSES', 'new processing shipped complete canceled')._make(range(5))

ORDER_STATUSES_CHOICES = (
    (ORDER_STATUSES.new, 'New'),
    (ORDER_STATUSES.processing, 'Processing'),
    (ORDER_STATUSES.shipped, 'Shipped'),
    (ORDER_STATUSES.complete, 'Complete'),
    (ORDER_STATUSES.canceled, 'Canceled'),
)
