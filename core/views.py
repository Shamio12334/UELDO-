from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Event, Registration, Match

# 1. Dashboard
def dashboard(request):
    categories = Category.objects.prefetch_related('subcategories__events').all()
    return render(request, 'index.html', {'categories': categories})

# 2. Event Details
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

# 3. Registration Logic
@login_required
def register_event(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        
        # Get data
        p_name = request.POST.get('name')
        p_phone = request.POST.get('phone')
        p_mode = request.POST.get('payment_mode')
        
        # Create Registration
        reg = Registration.objects.create(
            event=event,
            player_name=p_name,
            phone_number=p_phone,
            payment_mode=p_mode,
            is_paid=False 
        )

        # IF UPI: Send to Payment Page
        if p_mode == 'UPI':
            return redirect('payment_page', registration_id=reg.id)
        
        # IF VENUE: Go straight to Pass
        return redirect('view_pass', pass_id=reg.pass_id)

    return redirect('dashboard')

# 4. Payment Page (UPDATED ⚡)
@login_required
def payment_page(request, registration_id):
    reg = get_object_or_404(Registration, id=registration_id)

    if request.method == "POST":
        # User clicked "Payment Done"
        reg.is_paid = True  
        reg.save()
        
        # 👇 CHANGED THIS LINE: Redirect to Pass instead of Dashboard
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