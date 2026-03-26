# Views aur business logic idhar hai bhai

"""
Tutors Views
=============
Tutor directory, search, filter, and detail views.
"""

import math
import logging
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Avg

from apps.accounts.models import TutorProfile
from .models import Subject, Language, Review
from .filters import TutorDirectoryFilter


logger = logging.getLogger(__name__)


def directory_view(request):
    """
    Main tutor directory with filtering, sorting, and pagination.
    Only shows published tutors.
    """
    empty_qs = TutorProfile.objects.none()
    page_obj = Paginator(empty_qs, 12).get_page(1)
    tutor_filter = TutorDirectoryFilter(request.GET, queryset=empty_qs)
    subjects = []
    languages = []
    total_results = 0

    try:
        queryset = TutorProfile.objects.filter(
            is_published=True,
        ).select_related('user').prefetch_related('subjects', 'languages')

        tutor_filter = TutorDirectoryFilter(request.GET, queryset=queryset)
        filtered_qs = tutor_filter.qs

        user_lat = request.GET.get('lat')
        user_lng = request.GET.get('lng')
        max_distance = request.GET.get('distance')  # in km

        if user_lat and user_lng and max_distance:
            try:
                user_lat = float(user_lat)
                user_lng = float(user_lng)
                max_distance = float(max_distance)
                filtered_qs = _filter_by_distance(filtered_qs, user_lat, user_lng, max_distance)
            except (ValueError, TypeError):
                pass

        paginator = Paginator(filtered_qs, 12)  # 12 tutors per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        subjects = Subject.objects.filter(is_active=True)
        languages = Language.objects.all()
        total_results = filtered_qs.count()
    except Exception:
        logger.exception('Failed to load tutor directory data')

    context = {
        'page_obj': page_obj,
        'tutor_filter': tutor_filter,
        'subjects': subjects,
        'languages': languages,
        'total_results': total_results,
        'teaching_methods': TutorProfile.TeachingMethod.choices if hasattr(TutorProfile, 'TeachingMethod') else [],
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'tutors/partials/tutor_cards.html', context)

    return render(request, 'tutors/directory.html', context)


def tutor_detail_view(request, pk):
    """Detailed view of a single tutor profile."""
    tutor = get_object_or_404(
        TutorProfile.objects.select_related('user').prefetch_related('subjects', 'languages'),
        pk=pk,
        is_published=True,
    )

    related_tutors = TutorProfile.objects.filter(
        is_published=True,
        subjects__in=tutor.subjects.all()
    ).exclude(pk=tutor.pk).distinct()[:4]

    reviews = Review.objects.filter(tutor=tutor)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    user_review = None
    if request.user.is_authenticated and request.user.is_parent:
        user_review = Review.objects.filter(tutor=tutor, parent=request.user).first()

    context = {
        'tutor': tutor,
        'related_tutors': related_tutors,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'user_review': user_review,
    }
    return render(request, 'tutors/tutor_detail.html', context)


@login_required
def submit_review(request, pk):
    if request.method == 'POST':
        if not request.user.is_parent:
            messages.error(request, 'Only parents can submit reviews.')
            return redirect('tutors:detail', pk=pk)

        tutor = get_object_or_404(TutorProfile, pk=pk)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        if not rating or not str(rating).isdigit() or not (1 <= int(rating) <= 5):
            messages.error(request, 'Please provide a valid 1 to 5 star rating.')
            return redirect('tutors:detail', pk=pk)

        review, created = Review.objects.update_or_create(
            tutor=tutor,
            parent=request.user,
            defaults={'rating': int(rating), 'comment': comment}
        )

        if created:
            messages.success(request, 'Review submitted successfully!')
        else:
            messages.success(request, 'Review updated successfully!')

    return redirect('tutors:detail', pk=pk)


def tutor_search_api(request):
    """
    JSON API endpoint for live search/autocomplete.
    Returns tutor names and subjects matching the query.
    """
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    tutors = TutorProfile.objects.filter(
        is_published=True,
    ).filter(
        user__full_name__icontains=query
    ).select_related('user').values(
        'pk', 'user__full_name', 'price_per_hour', 'teaching_method'
    )[:10]

    results = [{
        'id': t['pk'],
        'name': t['user__full_name'],
        'price': str(t['price_per_hour']),
        'method': t['teaching_method'],
    } for t in tutors]

    return JsonResponse({'results': results})


def _haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points in km."""
    R = 6371  # Earth's radius in km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def _filter_by_distance(queryset, user_lat, user_lng, max_distance_km):
    """Filter queryset to only include tutors within max_distance_km."""

    tutors_with_coords = queryset.exclude(
        latitude__isnull=True
    ).exclude(
        longitude__isnull=True
    )

    nearby_ids = []
    for tutor in tutors_with_coords:
        distance = _haversine_distance(
            user_lat, user_lng,
            tutor.latitude, tutor.longitude
        )
        if distance <= max_distance_km:
            nearby_ids.append(tutor.pk)

    return queryset.filter(pk__in=nearby_ids)
