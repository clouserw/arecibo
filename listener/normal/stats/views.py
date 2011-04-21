from datetime import datetime, timedelta

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

from app.decorators import arecibo_login_required
from app.utils import render_plain, safe_int
from app.paginator import Paginator, get_page

from error.models import Error

stats = {
    "priority": {
        "title": "By Priority",
        "column": "priority",
        "count": "priority__count",
        "query": (Error.objects.values('priority', 'timestamp_date')
                  .order_by('timestamp_date').annotate(Count('priority'))),
    },
    "type": {
        "title": "By Type",
        "column": "type",
        "count": "type__count",
        "query": (Error.objects.values('type', 'timestamp_date')
                  .order_by('timestamp_date').annotate(Count('type'))),
    }

}


def format_results(stat, query):
    data = {"columns":[], "rows":{}}
    for line in query:
        column = line[stat['column']]
        if column == '':
            column = '(empty)'
        if column not in data['columns']:
            data['columns'].append(column)
        data['rows'].setdefault(line['timestamp_date'], [])
        data['rows'][line['timestamp_date']].append({
            'num': data['columns'].index(column) + 1,
            'count': line[stat['count']],
        })
    return data

@arecibo_login_required    
def stats_view(request, key=None):
    data = {"nav": {"selected": "stats"} }
    if key:
        stat = stats[key]
        end = datetime.today()
        start = end - timedelta(days=30)
        query = stat["query"].filter(timestamp_date__gte=start,
                                 timestamp_date__lte=end)
        data.update({
            "stats": zip(stats.keys(), stats.values()),
            "stat": stat,
            "start": start,
            "end": end,
            "result": format_results(stat, query),
            "query": query,
        })
    return direct_to_template(request, "stats_view.html", data)