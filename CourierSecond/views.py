from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Parcel, DeliveryProof
from .serializers import CustomUserSerializer, ParcelSerializer, DeliveryProofSerializer
from .permissions import IsCustomer, IsCourier, IsAdmin

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  
            headers = self.get_success_headers(serializer.data)  
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            self.permission_classes = [IsAuthenticated, IsCustomer]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsCourier | IsAdmin]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsAdmin]
        else:
            self.permission_classes = [IsAuthenticated, IsCustomer | IsCourier | IsAdmin]
        return super().get_permissions()

    def perform_update(self, serializer):
        if self.request.user.role == 'courier' and 'status' in self.request.data:
            if self.request.data['status'] == 'delivered':
                serializer.save(delivered_at=timezone.now())
        else:
            serializer.save()

class DeliveryProofViewSet(viewsets.ModelViewSet):
    queryset = DeliveryProof.objects.all()
    serializer_class = DeliveryProofSerializer
    permission_classes = [IsAuthenticated, IsCourier | IsAdmin]

    def perform_create(self, serializer):
        serializer.save(timestamp=timezone.now())
