from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from .serializers import AddressSerializer


class AddAddressView(APIView):
    def post(self, request):
        address_data = request.data
        user = address_data.get('user')

        # If is_default is true, set all other addresses for the user to is_default=False
        if address_data.get('is_default', False):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        # Deserialize and save the new address
        serializer = AddressSerializer(data=address_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Address added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressesView(ListAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        if not user_id:
            return Response({"message": "User id is required"}, status=status.HTTP_400_BAD_REQUEST)

        return Address.objects.filter(user=user_id)


class DeleteAddressView(APIView):
    def delete(self, request):
        address_id = request.query_params.get('address_id')
        user_id = request.query_params.get('user_id')

        if not address_id:
            return Response({"message": "Address id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not user_id:
            return Response({"message": "User id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the address to be deleted
            address = Address.objects.get(id=address_id, user=user_id)
        except Address.DoesNotExist:
            return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the address being deleted is the default address
        is_default = address.is_default

        # Delete the address
        address.delete()

        # If the deleted address was the default, find the next address and set it as the default
        if is_default:
            # Get remaining addresses for the user
            remaining_addresses = Address.objects.filter(user=user_id).order_by('id')

            if remaining_addresses.exists():
                # Set the first remaining address as the new default
                new_default_address = remaining_addresses.first()
                new_default_address.is_default = True
                new_default_address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateDefaultAddressView(APIView):
    def put(self, request):
        user_id = request.query_params.get('user_id')
        address_id = request.query_params.get('address_id')

        if not user_id or not address_id:
            return Response({"message": "user_id and address_id query parameters are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the address to be updated
            new_default_address = Address.objects.get(id=address_id, user=user_id)
        except Address.DoesNotExist:
            return Response({"message": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

        # Set the current default address to False if it exists
        Address.objects.filter(user=user_id, is_default=True).update(is_default=False)

        # Set the new default address
        new_default_address.is_default = True
        new_default_address.save()

        return Response({"message": "Default address updated successfully."}, status=status.HTTP_200_OK)
