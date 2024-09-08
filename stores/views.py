from django.db.models import Sum, Count
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from orders.models import OrderItem
from orders.serializers import StoreOrderSerializer
from .models import Store, StoreOrder
from .serializers import StoreSerializer
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear


class CreateStoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user already owns a store
        if Store.objects.filter(owner=request.user).exists():
            return Response({"message": "You already own a store."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and create the store
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            # Set the owner to the currently authenticated user
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetStoresByOwnerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter stores by the owner (authenticated user)
        store = Store.objects.filter(owner=request.user).first()

        if not store.exists():
            # Return a 404 not found response if no stores are found
            return Response({"message": "No stores found for the authenticated user."},
                            status=status.HTTP_404_NOT_FOUND)

        # Serialize the stores
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStores(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.all()


class StoreOrdersListView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = StoreOrderSerializer

    def get_queryset(self):
        store_id = self.request.query_params.get('store_id', None)

        if not store_id:
            return Response({"message": "Store id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response({"message": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

        return StoreOrder.objects.filter(store_reference=store_id)


class StoreOrderStatisticsView(APIView):

    def get(self, request):
        store_id = request.query_params.get('store_id', None)

        # Filter by store if store_id is provided
        if store_id:
            orders = StoreOrder.objects.filter(store_reference=store_id)
        else:
            orders = StoreOrder.objects.all()

        # Define the possible statuses
        all_statuses = dict(StoreOrder.ORDER_STATUS_CHOICES)

        # Get total orders for each status
        status_counts = orders.values('order_status').annotate(total=Count('id'))

        # Initialize counts for all statuses, even if they're zero
        status_counts_dict = {statuc: 0 for statuc in all_statuses.keys()}

        # Update counts with actual data
        for statuc in status_counts:
            status_counts_dict[statuc['order_status']] = statuc['total']

        # Format status data for the response
        formatted_status_counts = [
            {"status": all_statuses[statuc], "total": total}
            for statuc, total in status_counts_dict.items()
        ]

        # Calculate total revenue only for delivered orders
        total_revenue = orders.filter(order_status='delivered').aggregate(
            total_revenue=Sum('order_items__price')
        )['total_revenue'] or 0

        # Get the total number of delivered orders
        total_orders = orders.filter(order_status='delivered').count()

        # Get total number of items sold
        total_items_sold = orders.filter(order_status='delivered').aggregate(
            total_items=Sum('order_items__quantity')
        )['total_items'] or 0

        # Retrieve the top 3 products by total quantity sold
        top_products = OrderItem.objects.filter(store_orders__in=orders).values('product', 'product__title').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:3]

        # Format top products data
        top_products_data = [
            {"product_id": product['product'], "title": product['product__title'],
             "quantity_sold": product['total_quantity']}
            for product in top_products
        ]

        # Prepare statistics for response
        statistics = {
            'total_revenue': total_revenue,
            'total_delivered_orders': total_orders,
            'total_items_sold': total_items_sold,
            'status_counts': formatted_status_counts,
            'top_products': top_products_data
        }

        return Response(statistics, status=status.HTTP_200_OK)


class SalesChartDataView(APIView):
    def get(self, request):

        period = request.query_params.get('period', 'daily')
        store_id = request.query_params.get('store_id', None)

        if store_id:
            store_orders = StoreOrder.objects.filter(store_reference=store_id, order_status='delivered')
        else:
            Response({"message": "Store id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for valid period ('daily', 'weekly', 'monthly', 'yearly')
        if period not in ['daily', 'weekly', 'monthly', 'yearly']:
            return Response({"message": "Invalid period provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Choose truncation function based on the period
        if period == 'daily':
            trunc_function = TruncDay
        elif period == 'weekly':
            trunc_function = TruncWeek
        elif period == 'monthly':
            trunc_function = TruncMonth
        elif period == 'yearly':
            trunc_function = TruncYear

        # Annotate and aggregate sales data based on the selected period
        sales_data = store_orders.annotate(
            period=trunc_function('created_at')  # Group by the selected period
        ).values('period').annotate(
            total_sales=Sum('order_items__price'),  # Sum the total sales for that period
            total_items_sold=Sum('order_items__quantity')  # Sum the total items sold for that period
        ).order_by('period')

        # If no sales data exists, return a message
        if not sales_data:
            return Response({"message": "No sales data available."}, status=status.HTTP_404_NOT_FOUND)

        # Format response
        chart_data = {
            "period": period,
            "sales": list(sales_data)  # List of dicts with period, total_sales, and total_items_sold
        }

        return Response(chart_data, status=status.HTTP_200_OK)
