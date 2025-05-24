from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Prop, UsageLog, PropUse, Borrower
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib import messages
from pprint import pprint


def home(request):
    return render(request, 'inventory/home.html') 

# Prop Views
class PropListView(ListView):
    model = Prop
    template_name = 'inventory/prop_list.html'
    context_object_name = 'props'  # use 'props' here

class PropCreateView(CreateView):
    model = Prop
    fields = '__all__'
    success_url = reverse_lazy('prop_list')
    template_name = 'inventory/prop_form.html'

class PropUpdateView(UpdateView):
    model = Prop
    fields = '__all__'
    success_url = reverse_lazy('prop_list')
    template_name = 'inventory/prop_form.html'

class PropDeleteView(DeleteView):
    model = Prop
    success_url = reverse_lazy('prop_list')
    template_name = 'inventory/prop_confirm_delete.html'

# Borrower Views
def borrower_list(request):
    borrowers = Borrower.objects.all()
    return render(request, 'inventory/borrower_list.html', {'borrowers': borrowers})

def borrower_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Borrower.objects.create(name=name)
            messages.success(request, f"Borrower '{name}' added successfully.")
            return redirect('borrower_list')  # underscore
        else:
            messages.error(request, "Name cannot be empty.")
    return render(request, 'inventory/borrower_form.html', {'action': 'Add'})

def borrower_edit(request, borrower_id):
    borrower = get_object_or_404(Borrower, id=borrower_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            borrower.name = name
            borrower.save()
            messages.success(request, f"Borrower '{name}' updated successfully.")
            return redirect('borrower_list')
        else:
            messages.error(request, "Name cannot be empty.")
    return render(request, 'inventory/borrower_form.html', {'borrower': borrower, 'action': 'Edit'})

# UsageLog Views
class UsageLogListView(ListView):
    model = UsageLog
    template_name = 'inventory/usagelog_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(date_of_use=date)
        return queryset

def reports(request):
    most_used = UsageLog.objects.values('prop__name').annotate(total=Count('id')).order_by('-total')[:5]
    damaged_or_missing = UsageLog.objects.filter(return_status__in=['Damaged', 'Missing']).values('prop__name').annotate(total=Count('id'))
    return render(request, 'inventory/reports.html', {
        'most_used': most_used,
        'damaged_or_missing': damaged_or_missing
    })

def dashboard(request):
    most_used_props = (
        UsageLog.objects.values('prop__id', 'prop__name')
        .annotate(use_count=Count('id'))
        .order_by('-use_count')[:5]
    )

    condition_summary = Prop.objects.values('condition').annotate(count=Count('id'))

    pprint(list(most_used_props))

    return render(request, 'inventory/dashboard.html', {
        'most_used_props': most_used_props,
        'condition_summary': condition_summary,
    })

def use_prop(request, prop_id):
    prop = get_object_or_404(Prop, id=prop_id)
    borrowers = Borrower.objects.all()

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        borrower_id = request.POST.get('borrower_id')

        if quantity and quantity.isdigit() and borrower_id:
            quantity = int(quantity)
            if quantity > 0:
                borrower = get_object_or_404(Borrower, id=borrower_id)
                PropUse.objects.create(
                    prop=prop,
                    quantity=quantity,
                    borrower=borrower,
                )
                messages.success(request, f"Successfully recorded usage of {quantity} {prop.name} by {borrower.name}.")
                return redirect('home')
            else:
                messages.error(request, "Quantity must be a positive number.")
        else:
            messages.error(request, "Please enter a valid quantity and select a borrower.")

    return render(request, 'inventory/use_prop.html', {'prop': prop, 'borrowers': borrowers})

def prop_use_history(request, prop_id):
    prop = get_object_or_404(Prop, id=prop_id)
    use_logs = PropUse.objects.filter(prop=prop).order_by('-timestamp')

    return render(request, 'inventory/prop_use_history.html', {
        'prop': prop,
        'use_logs': use_logs
    })
