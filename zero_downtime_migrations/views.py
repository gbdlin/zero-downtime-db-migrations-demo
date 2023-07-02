from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView

from zero_downtime_migrations.models import Order, OrderLine


class MyOrdersView(ListView):
    model = Order
    context_object_name = 'orders'
    queryset = Order.objects.all()
    template_name = "order_list.html"


class MyOrderDetailView(DetailView):
    model = Order
    context_object_name = 'order'
    queryset = Order.objects.all()
    template_name = "order_detail.html"


OrderLineFormset = modelformset_factory(
    OrderLine,
    exclude=["order", "total_net", "total_tax"],
)

class MyOrderCreateView(CreateView):
    model = Order
    context_object_name = 'order'
    template_name = "order_create.html"
    success_url = "/orders/"

    fields = (
        "first_name",
        "last_name",
        "street",
        "city",
        "zip_code",
    )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = {
            "first_name": "Politechnika",
            "last_name": "Krakowska",
            "street": "Warszawska 24",
            "city": "Kraków",
            "zip_code": "31-155",
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["line_formset"] = self.line_formset
        return context

    def get_form(self, form_class = None):
        if self.request.method == "POST":
            self.line_formset = OrderLineFormset(data=self.request.POST, queryset=OrderLine.objects.none())
        else:
            self.line_formset = OrderLineFormset(
                queryset=OrderLine.objects.none(),
                initial=[
                    {
                        "item": "Rzutnik",
                        "item_price": "1087.00",
                        "item_tax": "250.1",
                        "quantity": "1",
                    },
                    {
                        "item": "Mikrofon",
                        "item_price": "342.00",
                        "item_tax": "78.69",
                        "quantity": "1",
                    },
                ],
            )
        return super().get_form(form_class = form_class)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.order_number = 123
        self.object.total_net = 0
        self.object.total_tax = 0
        lines = self.line_formset.save(commit=False)
        for line in lines:
            line.total_net = line.item_price * line.quantity
            line.total_tax = line.item_tax * line.quantity
            self.object.total_net += line.total_net
            self.object.total_tax += line.total_tax
        self.object.save()
        for line in lines:
            line.order = self.object
            line.save()
        return HttpResponseRedirect(self.get_success_url())
