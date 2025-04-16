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
import base64
import os
import platform
import json
import random

SITE_TITLE = getattr(settings, 'SITE_TITLE', 'MY SITE')


# MPTT TREE COPY


## common options to store ##

def clone_mptt_instance(model_class, original_instance, parent=None, fields=None):
    """
    Clone an MPTT model instance without using direct instance copying.
    :param model_class: The class of the MPTT model to create a new instance from.
    :param original_instance: The instance to clone.
    :param parent: The parent instance for the new clone.
    :param fields: List of fields to be copied.
    :return: The new cloned instance.
    """
    # Ensure model_class is indeed a model class
    if not issubclass(model_class, MPTTModel):
        raise ValueError("model_class must be a subclass of MPTTModel")

    # Create a new instance of the model class
    new_instance = model_class()  
    
    # Determine which fields to copy if not specified
    if fields is None:
        fields = [field.name for field in original_instance._meta.fields
                  if field.name not in ['id', 'lft', 'rght', 'tree_id', 'level', 'parent']]
    
    # Explicitly set field values from original to new instance
    for field_name in fields:
        setattr(new_instance, field_name, getattr(original_instance, field_name))
    
    # Set parent for the new instance
    new_instance.parent = parent
    new_instance.save()

    # Recursively clone child instances
    for child in original_instance.get_children():
        clone_mptt_instance(model_class, child, parent=new_instance, fields=fields)
    
    return new_instance

@transaction.atomic
def clone_mptt_tree(model_class, root_instance, fields=None):
    """
    Initiates the cloning process for a root node and all its descendants using a model class.
    :param model_class: The MPTT model class for creating new instances.
    :param root_instance: The root node of the MPTT tree to clone.
    :param fields: List of fields to copy.
    :return: The new root node of the cloned tree.
    """
    return clone_mptt_instance(model_class, root_instance, fields=fields)


#######################################################################################################
# SCRUM RELATED DEFINITIONS
#######################################################################################################


GLOBAL_DELIVERY_TYPES = {
    "PROJECT": {
        "label": "Project",
        "icon": "fa-solid fa-diagram-project",
        "description": "Temporary effort to create a unique product, service, or result."
    },
    "PRODUCT": {
        "label": "Product",
        "icon": "fa-solid fa-box",
        "description": "A tangible or digital item offered to customers."
    },
    "SERVICE": {
        "label": "Service",
        "icon": "fa-solid fa-screwdriver-wrench",
        "description": "Support or operational assistance provided to clients or users."
    },
    "CONSULTING": {
        "label": "Consulting",
        "icon": "fa-solid fa-comments",
        "description": "Expert advice provided to solve business problems."
    },
    "INTERNAL": {
        "label": "Internal",
        "icon": "fa-solid fa-building-lock",
        "description": "Tasks and operations focused on internal teams or infrastructure."
    },
    "ADMIN": {
        "label": "Admin",
        "icon": "fa-solid fa-user-gear",
        "description": "Administrative and clerical functions within the organization."
    },
    "MANAGEMENT": {
        "label": "Management",
        "icon": "fa-solid fa-people-roof",
        "description": "Overseeing, planning, and decision-making at various levels."
    },
    "LEADERSHIP": {
        "label": "Leadership",
        "icon": "fa-solid fa-chess-king",
        "description": "Guiding teams toward vision, mission, and goals."
    },
    "GENERAL": {
        "label": "General",
        "icon": "fa-solid fa-clipboard",
        "description": "General or uncategorized activities and tasks."
    },
    "HR": {
        "label": "HR",
        "icon": "fa-solid fa-user-group",
        "description": "Human resources and employee lifecycle management."
    },
    "FINANCE": {
        "label": "Finance",
        "icon": "fa-solid fa-indian-rupee-sign",
        "description": "Budgeting, accounting, and financial analysis activities."
    },
    "SALES": {
        "label": "Sales",
        "icon": "fa-solid fa-cart-shopping",
        "description": "Processes related to selling products or services."
    },
    "MARKETING": {
        "label": "Marketing",
        "icon": "fa-solid fa-bullhorn",
        "description": "Promoting products, services, and brand awareness."
    },
    "IT": {
        "label": "IT",
        "icon": "fa-solid fa-computer",
        "description": "Infrastructure, systems, and technical support operations."
    },
    "RESEARCH": {
        "label": "Research",
        "icon": "fa-solid fa-microscope",
        "description": "Investigation and study to discover or develop new knowledge."
    },
    "DEVELOPMENT": {
        "label": "Development",
        "icon": "fa-solid fa-code",
        "description": "Building or coding software, applications, or platforms."
    },
    "DESIGN": {
        "label": "Design",
        "icon": "fa-solid fa-palette",
        "description": "Creating visual, UX, or UI assets for projects and products."
    },
    "SUPPORT": {
        "label": "Support",
        "icon": "fa-solid fa-headset",
        "description": "Assisting users, resolving issues, and maintaining systems."
    },
    "TRAINING": {
        "label": "Training",
        "icon": "fa-solid fa-chalkboard-user",
        "description": "Educational activities to upskill individuals or teams."
    },
    "LOGISTICS": {
        "label": "Logistics",
        "icon": "fa-solid fa-truck-fast",
        "description": "Managing supply chain, delivery, and transportation."
    },
    "LEGAL": {
        "label": "Legal",
        "icon": "fa-solid fa-scale-balanced",
        "description": "Compliance, contracts, and legal advisory activities."
    },
    "PROCUREMENT": {
        "label": "Procurement",
        "icon": "fa-solid fa-truck-ramp-box",
        "description": "Purchasing goods and services for operational needs."
    },
    "QUALITY": {
        "label": "Quality",
        "icon": "fa-solid fa-check-double",
        "description": "Ensuring standards, testing, and assurance processes."
    },
    "STRATEGY": {
        "label": "Strategy",
        "icon": "fa-solid fa-lightbulb",
        "description": "Long-term planning and strategic initiatives."
    },
    "OPERATIONS": {
        "label": "Operations",
        "icon": "fa-solid fa-gears",
        "description": "Day-to-day execution and optimization of business processes."
    },
    "ORGANIZATION": {
        "label": "Organization",
        "icon": "fa-solid fa-sitemap",
        "description": "Structuring teams, departments, and workflows efficiently."
    },
    "DEVOPS": {
        "label": "DevOps",
        "icon": "fa-solid fa-infinity",
        "description": "Automating and integrating development and IT operations."
    },
    "BUILD_RELEASE": {
        "label": "Build & Release",
        "icon": "fa-solid fa-rocket",
        "description": "Building, packaging, and deploying software versions to production."
    },
}
