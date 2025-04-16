from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseForbidden
from functools import wraps
from django.db.models import *
from django.http import Http404
from django.utils.html import strip_tags
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template import Template, Context
from markdownx.utils import markdownify
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower, Trim
from itertools import chain
from markdownx.models import MarkdownxField
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Sum, FloatField
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps
from datetime import timedelta
from django.contrib.auth.models import Permission
from django.core.serializers.json import DjangoJSONEncoder
from collections import defaultdict
from django.template import Template, Context
from markdownx.utils import markdownify
from django.db import transaction
from collections import defaultdict
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from PIL import Image 
from lxml import etree
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.db import transaction
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.core.cache import cache
from collections import OrderedDict
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, time
from django.utils.timezone import now, localtime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import TruncTime
from django.db.models.functions import ExtractHour, ExtractMinute, ExtractSecond
from django.db.models import F
from django.db.models.functions import Extract

import traceback
import base64
import os
import platform
import json
import random
from django.http import JsonResponse
from django.apps import apps
from django.utils.timezone import make_aware
from datetime import datetime
import pytz
IST = pytz.timezone('Asia/Kolkata')
