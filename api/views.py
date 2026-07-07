from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import StudentProfile, Event, Participation, StudentSkill
from django.db.models import Sum
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'Birge API работает'})

@api_view(['POST'])
@permission_classes([AllowAny])
def send_sms_code(request):
    phone = request.data.get('phone')
    if not phone:
        return Response({'error': 'Телефон обязателен'}, status=400)
    return Response({'message': 'Код отправлен', 'code': '1234'})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    phone = request.data.get('phone')
    code = request.data.get('code')
    if code == '1234':
        user, created = User.objects.get_or_create(username=phone, defaults={'email': f'{phone}@temp.com'})
        if created:
            user.set_unusable_password()
            user.save()
            StudentProfile.objects.get_or_create(user=user, defaults={'group_name': 'Новая группа'})
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            'success': True,
            'user_id': user.id,
            'access_token': access_token,
            'refresh_token': str(refresh),
        })
    return Response({'error': 'Неверный код'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    total_hours = Participation.objects.filter(student=profile, is_verified=True).aggregate(total=Sum('hours_claimed'))['total'] or 0
    skills = StudentSkill.objects.filter(student=profile, level__gt=0).select_related('skill')
    skills_data = [{'name': s.skill.name, 'level': s.level} for s in skills]
    events = Participation.objects.filter(student=profile, is_verified=True).select_related('event')[:10]
    events_data = [{'title': p.event.title, 'hours': p.hours_claimed, 'date': p.verified_at} for p in events]
    return Response({
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'middle_name': profile.middle_name,
        'university': profile.university,
        'group_name': profile.group_name,
        'total_hours': total_hours,
        'skills': skills_data,
        'events': events_data,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_event(request):
    code = request.data.get('code')
    hours = request.data.get('hours')
    try:
        event = Event.objects.get(code=code, status='active')
    except Event.DoesNotExist:
        return Response({'error': 'Мероприятие не найдено'}, status=404)
    profile = StudentProfile.objects.get(user=request.user)
    if hours > event.max_hours:
        return Response({'error': f'Максимум {event.max_hours} часов'}, status=400)
    participation, created = Participation.objects.get_or_create(student=profile, event=event, defaults={'hours_claimed': hours})
    if not created:
        return Response({'error': 'Вы уже зарегистрированы'}, status=400)
    return Response({'message': 'Зарегистрировано. Ждите подтверждения.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_list(request):
    events = Event.objects.filter(status='active')
    data = [{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'date_start': e.date_start,
        'date_end': e.date_end,
        'code': e.code,
        'max_hours': e.max_hours,
        'skills': [skill.name for skill in e.skills.all()]
    } for e in events]
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    profile = StudentProfile.objects.get(user=user)
    data = request.data

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    user.save()

    if 'middle_name' in data:
        profile.middle_name = data['middle_name']
    if 'university' in data:
        profile.university = data['university']
    if 'group_name' in data:
        profile.group_name = data['group_name']
    profile.save()

    return Response({'message': 'Профиль обновлён'})
@api_view(['POST'])
@permission_classes([AllowAny])
def register_organization(request):
    data = request.data
    org_request = OrganizationRequest.objects.create(
        name=data.get('name'),
        type=data.get('type'),
        email=data.get('email'),
        phone=data.get('phone'),
        description=data.get('description', '')
    )
    return Response({
        'message': 'Заявка отправлена. Ожидайте подтверждения.',
        'request_id': org_request.id
    })
