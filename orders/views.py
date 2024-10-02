from django.db import transaction
from django.views.generic import ListView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers import OrderSerializer, OrderItemSerializer
from stores.models import Store, StoreOrder


# Create your views here.
class OrdersPagination(PageNumberPagination):
    page_size = 20  # Number of items per page by default
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional, if you want to limit the maximum page size


class OrderListView(APIView):
    pagination_class = OrdersPagination
    serializer_class = OrderSerializer

    def get(self, request):
        # Get order_status, payment_status, and user_id from query parameters
        order_status = request.query_params.get('order_status')
        payment_status = request.query_params.get('payment_status')
        user_id = request.query_params.get('user_id')

        # Validate presence of required parameters
        if not order_status:
            return Response({"message": "Order status is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not user_id:
            return Response({"message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter orders based on order_status and user_id
        filters = {
            'order_status': order_status,
            'user': user_id,
        }
        if payment_status:
            filters['payment_status'] = payment_status

        # Validate order status
        if order_status not in ['confirmed', 'shipped', 'delivered', 'failed', 'pending']:
            return Response({"message": "Order status is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the orders based on the provided filters
        queryset = Order.objects.filter(**filters)

        # Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If no pagination is applied (e.g., when queryset is small)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        order_id = request.query_params.get('order_id')

        if not order_id:
            return Response({"message": "Order id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateView(APIView):
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request):
        # Extract order data and order_items from the request
        order_data = request.data.copy()
        order_items_data = order_data.pop('order_items', [])

        # Placeholder for created order item instances
        created_order_items = []
        store_order_items = {}

        # Create the Order instance first
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            # Save the Order and get the instance
            order = order_serializer.save()

            # Create the OrderItem instances and assign them to the Order
            for item_data in order_items_data:
                # Add the order reference to each order item
                item_data['reference'] = order.id

                # Serialize and validate the OrderItem data
                order_item_serializer = OrderItemSerializer(data=item_data)
                if order_item_serializer.is_valid():
                    # Save the OrderItem and append it to the list of created items
                    order_item = order_item_serializer.save()
                    created_order_items.append(order_item)

                    # Organize order items by store for creating StoreOrder later
                    store_id = order_item.store.id
                    if store_id in store_order_items:
                        store_order_items[store_id].append(order_item)
                    else:
                        store_order_items[store_id] = [order_item]

                else:
                    # If any OrderItem is invalid, return the error
                    return Response(order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Now create StoreOrder for each store and link the relevant order items
            for store_id, items in store_order_items.items():
                store_instance = Store.objects.get(id=store_id)

                # Check if all items belong to the same store, then create StoreOrder
                if all(item.store.id == store_id for item in items):
                    store_order = StoreOrder.objects.create(
                        store_reference=store_instance.id,
                        order_reference=order.id,
                        address=order.address
                    )
                    # Link order items to the store order
                    store_order.order_items.add(*items)
                    store_order.save()

            # Return the response with the created order data
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

        # If the Order is invalid, return the error
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
