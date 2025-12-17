from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Event, Registration, Match

# 1. Dashboard (UPDATED to check participation)
def dashboard(request):
    categories = Category.objects.prefetch_related('subcategories__events').all()
    
    # Get a list of Event IDs the user has already joined
    my_event_ids = []
    if request.user.is_authenticated:
        my_event_ids = list(Registration.objects.filter(user=request.user).values_list('event_id', flat=True))

    return render(request, 'index.html', {
        'categories': categories,
        'my_event_ids': my_event_ids  # 👈 Sending this list to the HTML
    })

# 2. Event Details
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Check if already registered to prevent double signup
    already_registered = Registration.objects.filter(user=request.user, event=event).exists()
    return render(request, 'event_detail.html', {'event': event, 'already_registered': already_registered})

# 3. Registration Logic (UPDATED to save User)
@login_required
def register_event(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        
        p_name = request.POST.get('name')
        p_phone = request.POST.get('phone')
        p_mode = request.POST.get('payment_mode')
        
        reg = Registration.objects.create(
            user=request.user,  # 👈 SAVING THE LOGGED-IN USER HERE
            event=event,
            player_name=p_name,
            phone_number=p_phone,
            payment_mode=p_mode,
            is_paid=False 
        )

        if p_mode == 'UPI':
            return redirect('payment_page', registration_id=reg.id)
        
        return redirect('view_pass', pass_id=reg.pass_id)

    return redirect('dashboard')

# 4. Payment Page
@login_required
def payment_page(request, registration_id):
    reg = get_object_or_404(Registration, id=registration_id)
    if request.method == "POST":
        reg.is_paid = True  
        reg.save()
        return redirect('view_pass', pass_id=reg.pass_id)
    return render(request, 'payment.html', {'reg': reg})

# 5. View Pass
@login_required
def view_pass(request, pass_id):
    reg = get_object_or_404(Registration, pass_id=pass_id)
    return render(request, 'pass.html', {'reg': reg})

# 6. Lobby
@login_required
def lobby(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    players = Registration.objects.filter(event=event)
    matches = Match.objects.filter(event=event)
    return render(request, 'lobby.html', {'event': event, 'players': players, 'matches': matches})