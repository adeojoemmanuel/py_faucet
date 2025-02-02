from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from .utils import check_rate_limit
from .web3_client import send_eth
from .models import Transaction
import datetime
from web3 import Web3
import os

@api_view(['POST'])
def fund(request):
    # Your existing fund function remains unchanged
    wallet_address = request.data.get('wallet_address')
    ip = request.META.get('REMOTE_ADDR')
    w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URL')))
    
    if not check_rate_limit(ip, wallet_address):
        return Response(
            {'error': 'Rate limit exceeded'}, 
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    
    try:
        if not w3.is_connected():
            raise ValueError("Web3 provider not connected")

        # Load private key
        private_key = os.getenv('FAUCET_PRIVATE_KEY')
        if not private_key:
            raise ValueError("Private key missing in environment variables")
        
        sender_account = w3.eth.account.from_key(private_key)
        sender_address = sender_account.address

        sender_balance = w3.eth.get_balance(sender_address)
        tx_cost = (100000 * 3000000000) + w3.to_wei(0.00001, 'ether')
        if sender_balance < tx_cost:
            return Response(
                {'error': f'Faucet balance insufficient. Required: {tx_cost} wei, Available: {sender_balance} wei in {sender_address}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch chain ID and nonce
        chain_id = w3.eth.chain_id
        nonce = w3.eth.get_transaction_count(sender_address)
        if None in (chain_id, nonce):
            raise ValueError("Failed to fetch chain ID or nonce")

        signed_tx = w3.eth.account.sign_transaction(dict(
                nonce=w3.eth.get_transaction_count(sender_address),
                maxFeePerGas=3000000000,
                maxPriorityFeePerGas=2000000000,
                gas=100000,
                to=wallet_address,
                value=w3.to_wei(0.0000000001, 'ether'),
                data=b'',
                type=2,
                chainId=chain_id,
            ),
            private_key,
        )

        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_data = w3.eth.get_transaction(tx_hash)

        Transaction.objects.create(
            wallet_address=wallet_address,
            tx_hash=tx_hash.hex(),
            amount=0.00001,
            status='success',
            source_ip=ip
        )


        return Response({
            'tx_hash': tx_hash.hex(),
            'tx_data': Web3.to_json(tx_data)
        }, status=status.HTTP_200_OK)

    
    except Exception as e:
        Transaction.objects.create(
            wallet_address=wallet_address,
            tx_hash='',
            amount=0.00001,
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