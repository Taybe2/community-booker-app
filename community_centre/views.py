from datetime import datetime, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .models import CommunityCentre
from .utils import generate_time_slots

@staff_member_required
def generate_time_slots_view(request, centre_id):
    """View to generate time slots for a specific community center."""
    centre = get_object_or_404(CommunityCentre, pk=centre_id)
    
    if request.method == "POST":
        # Get the user-specified start and end dates
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Convert them to datetime.date objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        generate_time_slots(centre, start_date, end_date, slot_duration_minutes=60)
        messages.success(request, f"Time slots for {centre.name} were successfully generated.")
        return redirect('admin:community_centre_communitycentre_changelist')  # Redirect to admin list
    
    return render(request, 'community_centre/generate_time_slots.html', {'centre': centre})


class HomePage(TemplateView):
    template_name = 'community_centre/home.html'  # Specify the template to use

    def get_context_data(self, **kwargs):
        # Dictionary mapping numeric days to day names
        DAYS_OF_WEEK = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday',
        }
        # Fetch the first (or only) community centre from the database
        community_centre = CommunityCentre.objects.first()
        context = super().get_context_data(**kwargs)
        context['community_centre'] = community_centre

        # Add operating start and end day names to the context
        if community_centre:
            context['openning_day_name'] = DAYS_OF_WEEK.get(
                community_centre.operating_start_day, "Invalid Day"
            )
            context['closing_day_name'] = DAYS_OF_WEEK.get(
                community_centre.operating_end_day, "Invalid Day"
            )

        return context