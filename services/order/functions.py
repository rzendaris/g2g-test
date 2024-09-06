import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import Coalesce

from services.order.constants import RedemptionPointReference
from services.order.helpers import amount_conversion, point_to_usd_exchange, usd_to_point_exchange
from services.order.models import Order, Product
from services.user.models import CustomerPoint, Customer, CustomerPointRedemptionHistory


def calculate_reward_point(customer):
    """
    Desc : Calculate Customer Reward Points
    Params/Args :
        1. customer (source : .models/Customer)
    Return: Total Remaining Points (BigInt)
    """
    customer_point = CustomerPoint.objects.filter(customer=customer, expired_at__gte=datetime.date.today()).aggregate(
        total_granted_point=Coalesce(Sum('granted_point'), 0),
        total_used_point=Coalesce(Sum('used_point'), 0),
    )

    remaining_point = customer_point['total_granted_point'] - customer_point['total_used_point']

    return remaining_point


def granted_reward_point(order):
    """
    Desc : Granted Reward Points after orders Delivered
    Params/Args :
        1. order (source : .models/Order)
    Return: None
    """
    amount_converted = amount_conversion(order.price, convert_from=order.currency)
    customer_point = CustomerPoint()
    customer_point.customer = order.customer
    customer_point.granted_point = amount_converted
    customer_point.used_point = 0
    customer_point.expired_at = datetime.date.today() + relativedelta(years=1)
    customer_point.save()


def point_deduction(reference_name, reference_data, redemption_point):
    """
    Desc : Deduct the used point, create Redemption History Point related to Customer Point used and Reference Data
    Params/Args :
        1. reference_name (source : .constants/RedemptionPointReference)
        2. reference_data (return of the model that rewards point implemented)
        3. redemption_point (number of reward point issued)
    Return: None
    """
    customer_active_points = CustomerPoint.objects.filter(
        customer=reference_data.customer, expired_at__gte=datetime.date.today()
    ).order_by('expired_at', 'id')

    for customer_point in customer_active_points:
        point_available = customer_point.granted_point - customer_point.used_point
        if point_available > 0:
            if redemption_point > 0:
                if redemption_point <= point_available:
                    point_available = redemption_point

                customer_point.used_point += point_available
                customer_point.save()

                # Store history point redemption
                customer_point_redemption = CustomerPointRedemptionHistory()
                customer_point_redemption.customer_point = customer_point
                customer_point_redemption.used_point = point_available
                customer_point_redemption.reference_name = reference_name
                customer_point_redemption.reference_id = reference_data.id
                customer_point_redemption.save()

                # Reduce Redemption Point and break if redemption point is zero
                redemption_point -= point_available
            else:
                break


def create_order(form_data):
    """
    Desc : Create new Order
    Params/Args :
        1. form_data (source : .forms/CreateOrderForm)
    Return: None
    """
    customer = Customer.objects.filter(email=form_data['email']).first()
    product = Product.objects.filter(id=form_data['product_id']).first()
    reward_point = calculate_reward_point(customer)
    discount_amount = 0
    if reward_point > 0:
        # Count the redemption point amount and convert to product currency
        redemption_point = point_to_usd_exchange(reward_point)
        discount_amount = amount_conversion(redemption_point, convert_from='USD', convert_to=product.currency)

        # Case if customer had points amount greater than product price (after convert point to USD)
        if discount_amount >= product.price:
            product_price_in_usd = amount_conversion(product.price, convert_from=product.currency)
            reward_point = usd_to_point_exchange(product_price_in_usd)
            discount_amount = amount_conversion(product_price_in_usd, convert_from='USD', convert_to=product.currency)

    # Create Order
    order = Order()
    order.customer = customer
    order.product = product
    order.price = product.price
    order.total_discount = discount_amount  # Put Point Amount as a Discount
    order.total_amount = product.price - discount_amount
    order.currency = product.currency
    order.save()

    if order:
        point_deduction(RedemptionPointReference.ORDER, order, reward_point)

    return order
