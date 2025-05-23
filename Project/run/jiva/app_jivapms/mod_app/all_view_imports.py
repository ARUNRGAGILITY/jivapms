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
from django.http import JsonResponse
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
from django.template.loader import get_template, TemplateDoesNotExist
from PIL import Image 
from lxml import etree
from io import BytesIO
from django.core.files.base import ContentFile
from imagekit.models import ImageSpecField
from imagekit.processors import *
from imagekit.models import ProcessedImageField
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.db import transaction
from django.utils.safestring import mark_safe
import traceback
import base64
import os
import platform
import json
import random
import logging
import re
logger = logging.getLogger(__name__)
SITE_TITLE = getattr(settings, 'SITE_TITLE', 'MY SITE')



def check_model_rec_count(mark, model, name):
    check_query = model.objects.filter(name=name)
    check_query_count = check_query.count()
    logger.debug(f">>>> === {mark} CHECK_QUERY [[ {check_query} ]] === <<<")
    logger.debug(f">>>> === {mark} CHECK_QUERY_COUNT [[ {check_query_count} ]] === <<<")
    
    return True
    