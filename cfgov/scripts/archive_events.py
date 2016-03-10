import os
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from v1.models.learn_page import EventPage
from v1.models.browse_page import BrowsePage
from v1.models.browse_filterable_page import EventArchivePage
from wagtail.wagtailcore.models import Page
from modelcluster.models import get_all_child_relations


def run():
    event_page_exists = BrowsePage.objects.filter(title='Events').exists()
    archive_event_page_exists = EventArchivePage.objects.filter(title='Archive').exists()

    if event_page_exists and archive_event_page_exists:
        events = BrowsePage.objects.get(title='Events')
        archived_events = EventArchivePage.objects.get(title='Archive')

        if len(events.get_children()) > 1:
            for child in events.get_children():
                event = child.specific
                if isinstance(event, EventPage):
                    if event.end_dt:
                        if event.end_dt < timezone.now():
                            if event.can_move_to(archived_events):
                                event.move(archived_events, pos='last-child')
                                print event.title + ' Event .....archived'
        else:
            print 'No events to archive found....'
    elif not event_page_exists:
        print 'Events browse page has not been created....'
    elif not archive_event_page_exists:
        print 'No Archived events Browse page named \'Archive\' exist....'
    else:
        print 'No events exist in the database...'
