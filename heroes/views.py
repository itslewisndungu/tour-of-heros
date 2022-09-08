from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import HeroModel
from .serializers import HeroSerializer
from django.shortcuts import get_object_or_404


@api_view(["GET"])
def get_all_heros(request: Request):

    qs = HeroModel.objects.all()
    serializer = HeroSerializer(qs, many=True)
    res = {"status": status.HTTP_200_OK, "data": serializer.data}
    return Response(data=res)


@api_view(["GET"])
def get_hero_by_id(request: Request, id=None):
    # Method 1
    # Method does not error gracefully unless we use a try except block

    # try:
    #    qs = HeroModel.objects.get(id=pk)
    #    serializer = HeroSerializer(qs)
    # except Snippet.DoesNotExist:
    #     return HttpResponse(status=404)

    # Method 2
    qs = HeroModel.objects.all()
    instance = get_object_or_404(qs, id=id)
    serializer = HeroSerializer(instance)

    return Response(data=serializer.data)


@api_view(["POST"])
def create_hero(request: Request):
    hero = request.data
    serializer = HeroSerializer(data=hero)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def update_hero(request: Request, id=None):
    qs = HeroModel.objects.all()
    instance = get_object_or_404(qs, id=id)
    updates = request.data

    # partial=True because this is a patch request
    serializer = HeroSerializer(instance=instance, data=updates, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def get_all_or_create_hero(request: Request):
    if request.method == "GET":
        """
        Get all heros
        """
        qs = HeroModel.objects.all()
        serializer = HeroSerializer(qs, many=True)
        res = {"status": status.HTTP_200_OK, "data": serializer.data}
        return Response(data=res)

    elif request.method == "POST":
        """
        Create a new hero
        """
        hero = request.data
        serializer = HeroSerializer(data=hero)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update(instance, updates, partial=False):
    serializer = HeroSerializer(instance=instance, data=updates, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE", "PUT"])
def get_update_delete_hero_by_id(request: Request, id=None):
    qs = HeroModel.objects.all()
    instance: HeroModel = get_object_or_404(qs, id=id)

    if request.method == "GET":
        serializer = HeroSerializer(instance)
        return Response(data=serializer.data)

    elif request.method == "PATCH":
        return update(instance=instance, updates=request.data, partial=True)

    elif request.method == "PUT":
        return update(instance=instance, updates=request.data)

    elif request.method == "DELETE":
        try:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
