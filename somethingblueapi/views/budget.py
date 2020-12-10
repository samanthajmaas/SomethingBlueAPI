from django.http.response import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import uuid
import base64
from django.core.files.base import ContentFile
from somethingblueapi.models import Wedding, BudgetItem, WeddingBudget, Bride
from somethingblueapi.views.wedding import WeddingSerializer

class Budgets(ViewSet):
    def create(self, request):
        """Handle POST operations for Budget items for a wedding"""
        item = BudgetItem()
        item.save_for = request.data["save_for"]
        item.default= False
        try:
            item.save()
            serializer = BudgetItemSerializer(item, context={'request': request})

            bride = Bride.objects.get(user=request.auth.user)
            wedding = Wedding.objects.get(bride=bride)
            
            wedding_budget = WeddingBudget()
            wedding_budget.wedding = wedding
            wedding_budget.budget_item = int(serializer.data["id"])
            wedding_budget.estimated_cost = request.data["estimated_cost"]
            wedding_budget.actual_cost = request.data["actual_cost"]
            wedding_budget.paid = request.data["paid"]
            if "proof_img" in request.data:
                format, imgstr = request.data["proof_img"].split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{proof_img}-{request.data["name"]}.{ext}')

                wedding_budget.proof_img = data


            wedding_budget.save()
            weddingSerializer = WeddingBudgetSerializer(wedding_budget, context={'request': request})
            return Response(weddingSerializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET request for single budget relationship"""
        try:
            item = WeddingBudget.objects.get(pk=pk)
            serializer = WeddingBudgetSerializer(item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a relationship item"""
        try:
            item = WeddingBudget.objects.get(pk=pk)
            item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except WeddingBudget.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        """handles getting a list of all checklist items special to a wedding"""
        budget = WeddingBudget.objects.all()

        wedding = self.request.query_params.get('wedding', None)

        if wedding is not None:
            budget = budget.filter(wedding__id=wedding)

        serializer = WeddingBudgetSerializer(
            budget, many=True, context={'request': request})
        return Response(serializer.data)

class BudgetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetItem
        fields = ('id', 'save_for', 'default')

class WeddingBudgetSerializer(serializers.ModelSerializer):
    budget_item = BudgetItemSerializer(many=False)
    wedding = WeddingSerializer(many=False)

    class Meta:
        model = WeddingBudget
        fields = ('id', 'wedding', 'budget_item', 'estimated_cost', 'actual_cost', 'paid', 'proof_img')
        depth = 1

