from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import TransactionHistoryForm
from .models import Transaction_History


@login_required
def transaction_history_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TransactionHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transaction_history_list")  # Redirect to transaction list after successful creation
    else:
        form = TransactionHistoryForm()
    return render(request, "transaction_history/transaction_history_form.html", {"form": form})


@login_required
def transaction_history_list(request: HttpRequest) -> HttpResponse:
    transactions = Transaction_History.objects.all()  # Retrieve all transactions
    context = {"transactions": transactions}
    return render(request, "transaction_history/transaction_history_list.html", context)


# You can add additional views for editing and deleting transactions if needed
