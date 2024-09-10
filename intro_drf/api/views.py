from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from django.core.cache import cache
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import urllib.parse

# Create your views here.
class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstituionsSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        top_buyer_name = self.request.query_params.get('top_buyer_name', None)
        top_seller_name = self.request.query_params.get('top_seller_name', None)
        symbol = self.request.query_params.get('symbol', None)
        updated_on = self.request.query_params.get('updated_on', None)
        net_transaction = self.request.query_params.get('net_transaction', None)
        date = self.request.query_params.get('date', None)
        fromDate = self.request.query_params.get('from-date', None)
        toDate = self.request.query_params.get('to-date', None)

        
        if top_buyer_name:
            queryset = queryset.filter(Q(top_buyers__contains=[{'name': top_buyer_name}]))
        
        if top_seller_name:
            queryset = queryset.filter(Q(top_sellers__contains=[{'name': top_seller_name}]))

        if symbol:
            queryset = queryset.filter(symbol=symbol)
        
        if updated_on:
            queryset = queryset.filter(updated_on=updated_on)
        
        if net_transaction:
            queryset = queryset.filter(net_transaction=net_transaction)

        if date:
            queryset = queryset.filter(date=date)

        if fromDate and toDate:
            queryset = queryset.filter(date__gte=fromDate, date__lte=toDate)

        return queryset

    def list(self, request):
        cache_key = f"institution:{self.request.query_params.get('top_buyer_name', None)}:{self.request.query_params.get('top_seller_name', None)}:{self.request.query_params.get('symbol', None)}:{self.request.query_params.get('updated_on', None)}:{self.request.query_params.get('net_transaction', None)}:{self.request.query_params.get('date', None)}"
        #cache_key = self.request.get_full_path()
        result = cache.get(cache_key)
        
        if not result:
            print('Hitting DB')
            result = self.get_queryset()
            
            print(result.values())
            
            cache.set(cache_key, result, 60)
        else:
            print('Cache retrieved!')
        
        result = self.serializer_class(result, many=True)
        print(result.data)

        return Response(result.data)



class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer


    def get_queryset(self):
        queryset = super().get_queryset()

        sub_sector = self.request.query_params.get('sub_sector', None)
        top_mcap = self.request.query_params.get('top-mcap', None)

        if sub_sector:
            subsectors = sub_sector.split(',')
            query = Q()

            for subsector in subsectors:
                query |= Q(sub_sector__icontains=subsector)
            queryset = queryset.filter(query)
        
        if top_mcap:
            queryset = queryset.order_by('total_market_cap')[:int(top_mcap)]

        return queryset

    
    def list(self, request):
        cache_key = f'sub_sector:{self.request.query_params.get('sub_sector', None)}'
        #cache_key = self.request.get_full_path()
        result = cache.get(cache_key)
        
        if not result:
            print('Hitting DB')
            result = self.get_queryset()
            
            print(result.values())
            
            cache.set(cache_key, result, 60)
        else:
            print('Cache retrieved!')
        
        result = self.serializer_class(result, many=True)
        print(result.data)

        return Response(result.data)

class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sector = self.request.query_params.get('sector', None)
        if sector:
            queryset = queryset.filter(sector=sector)
        return queryset

    
    def list(self, request):
        cache_key = f'sector:{self.request.query_params.get('sector', None)}'
        result = cache.get(cache_key)
        
        if not result:
            print('Hitting DB')
            result = self.get_queryset()
            
            print(result.values())
            
            cache.set(cache_key, result, 60)
        else:
            print('Cache retrieved!')
        
        result = self.serializer_class(result, many=True)
        print(result.data)

        return Response(result.data)


