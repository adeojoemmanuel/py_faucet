from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from .utils import check_rate_limit
from .web3_client import send_eth
from .models import Transaction
import datetime

@api_view(['POST'])
def fund(request):
    # Your existing fund function remains unchanged
    wallet_address = request.data.get('wallet_address')
    ip = request.META.get('REMOTE_ADDR')
    
    if not check_rate_limit(ip, wallet_address):
        return Response(
            {'error': 'Rate limit exceeded'}, 
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    
    try:
        tx_hash = send_eth(wallet_address)
        Transaction.objects.create(
            wallet_address=wallet_address,
            tx_hash=tx_hash,
            amount=0.0001,
            status='success',
            source_ip=ip
        )
        return Response({'tx_hash': tx_hash})
    
    except Exception as e:
        Transaction.objects.create(
            wallet_address=wallet_address,
            tx_hash='',
            amount=0.0001,
            status='failed',
            source_ip=ip
        )
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def stats(request):
    # Your existing stats function remains unchanged
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    
    stats = {
        'success': Transaction.objects.filter(
            status='success',
            created_at__gte=yesterday
        ).count(),
        'failed': Transaction.objects.filter(
            status='failed',
            created_at__gte=yesterday
        ).count()
    }
    
    return Response(stats)

class IndexView(TemplateView):
    template_name = 'faucet/index.html'