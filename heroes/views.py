from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import HeroModel
from .serializers import HeroSerializer

# Create your views here.


class HeroViewSet(viewsets.ViewSet):
    qs = HeroModel.objects.all()

    def list(self, request):
        params = request.query_params
        city = params.get("city")
        name = params.get("name")
        qs = self.qs

        if city:
            qs = qs.filter(city__name__contains=city)

        if name:
            qs = qs.filter(name__contains=name)

        serializer = HeroSerializer(qs, many=True)

        res = {"status": status.HTTP_200_OK, "data": serializer.data}
        return Response(data=res)

    def create(self, request):
        hero = request.data
        serializer = HeroSerializer(data=hero)

        if serializer.is_valpk():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.qs, pk=pk)
        serializer = HeroSerializer(instance)
        return Response(data=serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(self.qs)
        serializer = HeroSerializer(instance=instance, data=request.data)

        if serializer.is_valpk():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        instance = get_object_or_404(self.qs)
        serializer = HeroSerializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valpk():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(self.qs)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
