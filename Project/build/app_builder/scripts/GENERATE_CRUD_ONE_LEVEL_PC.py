
forms_py = """
from ___APPNAME___.mod_app.all_form_imports import *
from ___APPNAME___.mod____singularmodname___.models____singularmodname___ import *

class ___MODELNAME___Form(forms.ModelForm):
    class Meta:
        model = ___MODELNAME___
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(___MODELNAME___Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

"""

list_objects_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% load mptt_tags %}
{% block content %}
{% include 'app_common/common_files/navbar.html' %}
{% include 'app_jivapms/mod_web/common_files/css.html' %}
<style>
  .trash-icon {
    position: fixed;
    right: 10px;
    bottom: 10px;
    font-size: 24px;  /* Size of the icon */
    cursor: pointer;
    color: #707070;  /* Color of the icon */
  }
</style>
<!-- Begin: Content -->
<div class="content-wrapper">
   {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
    
    {% include 'app_organization/mod_project/sidebar_menu.html' %}
    <form method="post">
    {% csrf_token %}
    <div class="contentbar mb-5" id="contentbar">
        <div class="container-fluid">
            <div class="row">
                <div class="col col-md-12">           
                    <!-- display -->
                    
                    <div class="row">
                        <div class="col col-md-12">
                            <div class="container-fluid-width">
                                <div class="row pb-2">
                                    <div class="col col-md-5">                                
                                        <b class="h3">
                                        <a href="{% url 'list___pluralfirstmodname___' %}" style="text-decoration: none;">
                                            {{organization}}
                                        </a>
                                        </b>
                                        &nbsp;&nbsp;
                                        ___DISPMODNAME___ List
                                    
                                    </div>
                                    <div class="col col-md-4">
                                        <form method="get">
                                            <input type="text" name="search" placeholder="Search" value="{{ search }}">
                                            &nbsp;&nbsp;  
                                            <button type="submit" class="btn btn-sm btn-primary">Search</button> 
                                            &nbsp;&nbsp;  
                                            <button type="submit" class="btn btn-sm btn-info">Clear</button>   
                                        </form>
                                    </div>
                                    <div class="col col-md-3 text-end">
                                        <span class="display_count">{{objects_count}} ___singularmodname___(s)</span>
                                        &nbsp;&nbsp;
                                        <a href="{% url 'create____singularmodname___' ___firstid___  %}" 
                                        class="btn btn-sm btn-success"><b>+ Create ___DISPMODNAMESINGULAR___</b></a>
                                        
                                        &nbsp;&nbsp;
                                        <a href="{% url 'list___pluralfirstmodname___' %}" class="btn btn-primary">
                                            <i class="bi bi-arrow-left"></i>
                                        </a>
                                        &nbsp;&nbsp;
                                        {% if deleted_count > 0 %}
                                        <a href="{% url 'list_deleted____pluralmodname___' ___firstid___ %}"><i class="bi bi-trash-fill"></i></a>   
                                        {% endif %}
                                    </div>
                                </div>
                            </div>
                            <form action="" method="POST">
                            {% csrf_token %}
                            <table class="table table-bordered sortable_table">
                                <thead>
                                    <tr>
                                        <th width="2%"><i class="bi bi-grip-vertical"></i></th>
                                        <th width="2%">
                                            <input type="checkbox" name="select_all" id="select_all" onclick='checkUncheck(this)'>
                                        </th>                                
                                        <th width="2%">#</th>
                                        <th>___DISPMODNAMESINGULAR___</th>
                                        <th width="20%">Description</th>
                                        <th width="10%">Configure</th>
                                        <th width="50%">                                    
                                            Actions
                                            &nbsp;&nbsp;
                                            <select name="pagination" id="paginationselect">
                                                <option value="none" {% if selected_pagination == 'none' %}selected{% endif %}>-Page-</option>
                                                {% for option in pagination_options %}
                                                    <option value="{{ option }}" {% if show_all|lower == option|lower|stringformat:"s" %}selected{% endif %}>
                                                        {{ option|capfirst }}
                                                    </option>
                                                {% endfor %}
                                            </select>
                                            
                                            &nbsp;&nbsp;
                                            <b>Bulk:</b>&nbsp;&nbsp; 
                                            <select name="bulk_operations" id="bulk_operations"  onchange="this.form.submit()">
                                                <option value="none" {% if 'none' in selected_bulk_operations %}selected{% endif %}>-- Ops --</option>
                                                <option value="bulk_done" {% if 'bulk_done' in selected_bulk_operations %}selected{% endif %}>Done</option>
                                                <option value="bulk_not_done" {% if 'bulk_not_done' in selected_bulk_operations %}selected{% endif %}>Not Done</option>
                                                <option value="bulk_blocked" {% if 'bulk_blocked' in selected_bulk_operations %}selected{% endif %}>Blocked</option>
                                                <option value="bulk_delete" {% if 'bulk_delete' in selected_bulk_operations %}selected{% endif %}>Delete</option>
                                            </select>
                                                                
                                        </th>
                                    </tr>
                                </thead>

                                <tbody  id="sortable" class="sortable-tbody">
                                    {% for tobject in page_obj %}
                                    <tr id="{{tobject.id}}_{{ forloop.counter }}" class="sortable-row display_tr">
                                        <td class="drag-handle">
                                            <i class="bi bi-grip-vertical"></i>
                                        </td>
                                        <td width="2%">
                                            <input type="checkbox" name="selected_item" id="selected_item_ids" value="{{tobject.id}}">
                                        </td>
                                        <td>{{forloop.counter}}</td>
                                        <td width="20%" ondblclick="makeEditable(this)"
                                        onblur="save_element_text(this, '{{ tobject.id }}',  '___APPNAME___', '___MODELNAME___', 'name')"
                                        ><strong>{% if tobject.name != None %}{{tobject.name}}{% endif %}</strong></td>
                                        <td width="" ondblclick="makeEditable(this)"
                                        onblur="save_element_text(this, '{{ tobject.id }}',  '___APPNAME___', '___MODELNAME___', 'description')"
                                        >{% if tobject.description != None %}{{tobject.description}}{% endif %}</td>
                                        <td width="20%">
                                        
                                        </td>
                                        <td width="50%">
                                            <a href="{% url 'view____singularmodname___' ___firstid___  tobject.id  %}"
                                            class="btn btn-sm btn-primary"><i class="bi bi-eye"></i></a>
                                            &nbsp;&nbsp;
                                            <a href="{% url 'edit____singularmodname___' ___firstid___  tobject.id %}"
                                            class="btn btn-sm btn-warning"><i class="bi bi-pencil-square"></i></a>
                                            &nbsp;&nbsp;
                                            <a href="{% url 'delete____singularmodname___' ___firstid___  tobject.id %}"
                                            class="btn btn-sm btn-danger"><i class="bi bi-x-square"></i></a>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                                    <tr>
                                        <td colspan="7">
                                            {% include 'app_common/common_files/pagination.html' %}
                                        </td>
                                    </tr>                        
                            </table>
                        <!-- end display -->
                </div>
            </div>
        
        </div>
    </div>
</div>
</form>
<script>
// Select all / checkbox
function checkUncheck(checkBox) {
    get = document.getElementsByName('selected_item');
    for(var i=0; i<get.length; i++) {
        get[i].checked = checkBox.checked;
    }
}
</script>

<script>
    // pagination select
document.addEventListener("DOMContentLoaded", function () {
  const redirectSelect = document.getElementById("paginationselect");
  redirectSelect.addEventListener("change", function () {
    const selectedValue = redirectSelect.value;
    
    // Redirect the user based on the selected value
    if (selectedValue === "5") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=5";
    } else if (selectedValue === "10") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=10";
    } else if (selectedValue === "15") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=15";
    } else if (selectedValue === "25") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___  %}?page=1&all=25";
    } else if (selectedValue === "50") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=50";
    } else if (selectedValue === "100") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=100";
    } else if (selectedValue === "all") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=all";
    } 
    // Add more conditions for other options as needed
  });
});
</script>

<script>
    $(".sortable_table").find("tbody").sortable({
      items: "> tr",
      handle: ".drag-handle",
      appendTo: "parent",
      cancel: "[contenteditable]",
      update: function(event, ui) {
              var serialOrder = $('#sortable').sortable('serialize');
              var arrayOrder = $('#sortable').sortable('toArray');
              //alert(arrayOrder);
              $.ajax({
                url: '/common/common_ajax/ajax_update_model_list_sorted/',
                type: 'POST',
                data : {
                  'csrfmiddlewaretoken': "{{ csrf_token }}",
                  'model_name': '___MODELNAME___',
                  'app_name': '___APPNAME___',
                  'sorted_list_data': JSON.stringify(arrayOrder),
                  
                },
                dataType: 'json',
                success: function(data) {
                  console.log(data);
                }
              })
            }
    });
</script>


<script>
    function makeEditable(element) {
        element.contentEditable = true;
        element.focus();
    }


    function save_element_text(element, id,  appName, modelName, fieldName) {
        element.contentEditable = false;
        $.ajax({
            url: '/common/common_ajax/ajax_save_element_text/',
            type: 'POST',
            data : {
            'csrfmiddlewaretoken': "{{ csrf_token }}",
            'model_name': modelName,
            'app_name': appName,
            'field_name': fieldName,
            'text': element.textContent, 
            'id': id,
            },
            dataType: 'json',
            success: function(data) {
            console.log(data);
            }
        })
    }
</script>

<!-- End: Content -->
{% endblock content %}
"""


list_deleted_objects_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% load mptt_tags %}
{% block content %}
{% include 'app_common/common_files/navbar.html' %}
{% include 'app_jivapms/mod_web/common_files/css.html' %}

<!-- Begin: Content -->
<div class="content-wrapper">
    {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
    
    {% include 'app_organization/mod_project/sidebar_menu.html' %}
    <form method="post">
    {% csrf_token %}
    <div class="contentbar mb-5" id="contentbar">
        <div class="container-fluid">
            <div class="row">
                <div class="col col-md-12">           
                    <!-- display -->
                    
                    <div class="row">
                        <div class="col col-md-12">
                            <div class="container-fluid-width">
                                <div class="row pb-2">
                                    <div class="col col-md-8">
                                        <b class="h3">
                                        <a href="{% url 'list___pluralfirstmodname___' %}" style="text-decoration: none;">
                                            {{organization}}
                                        </a>
                                        </b>
                                        &nbsp;&nbsp;
                                        ___DISPMODNAME___ List
                                    </div>
                                    <div class="col col-md-4 text-end">
                                        <span class="display_count">{{objects_count}} ___singularmodname___(s)</span>
                                        &nbsp;&nbsp;
                                        <a href="{% url 'create____singularmodname___' ___firstid___  %}" 
                                        class="btn btn-sm btn-success"><b>+ Create ___DISPMODNAMESINGULAR___</b></a>
                                        
                                        &nbsp;&nbsp;
                                        <a href="{% url 'list___pluralfirstmodname___' %}" class="btn btn-primary">
                                            <i class="bi bi-arrow-left"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <form action="" method="POST">
                            {% csrf_token %}
                            <table class="table table-bordered sortable_table">
                                <thead>
                                    <tr>
                                        <th width="2%"><i class="bi bi-grip-vertical"></i></th>
                                        <th width="2%">
                                            <input type="checkbox" name="select_all" id="select_all" onclick='checkUncheck(this)'>
                                        </th>
                                        <th width="2%">#</th>
                                        <th>___DISPMODNAMESINGULAR___</th>
                                        <th width="20%">Description</th>
                                        <th width="10%">Configure</th>
                                        <th width="50%">                                    
                                            Actions
                                            &nbsp;&nbsp;
                                            <select name="pagination" id="paginationselect">
                                                <option value="none" {% if selected_pagination == 'none' %}selected{% endif %}>-Page-</option>
                                                {% for option in pagination_options %}
                                                    <option value="{{ option }}" {% if show_all|lower == option|lower|stringformat:"s" %}selected{% endif %}>
                                                        {{ option|capfirst }}
                                                    </option>
                                                {% endfor %}
                                            </select>
                                            
                                            &nbsp;&nbsp;
                                            <b>Bulk:</b>&nbsp;&nbsp; 
                                            <select name="bulk_operations" id="bulk_operations"  onchange="this.form.submit()">
                                                <option value="none" {% if 'none' in selected_bulk_operations %}selected{% endif %}>-- Ops --</option>
                                                <option value="bulk_restore" {% if 'bulk_restore' in selected_bulk_operations %}selected{% endif %}>Restore</option>
                                                <option value="bulk_erase" {% if 'bulk_erase' in selected_bulk_operations %}selected{% endif %}>Erase</option>
                                            </select>                                                         
                                        </th>
                                    </tr>
                                </thead>

                                <tbody  id="sortable" class="sortable-tbody">
                                    {% for tobject in page_obj %}
                                    <tr id="{{tobject.id}}_{{ forloop.counter }}" class="sortable-row display_tr">
                                        <td class="drag-handle">
                                            <i class="bi bi-grip-vertical"></i>
                                        </td>
                                        <td width="2%">
                                            <input type="checkbox" name="selected_item" id="selected_item_ids" value="{{tobject.id}}">
                                        </td>
                                        <td>{{forloop.counter}}</td>
                                        <td width="20%"><strong>{{tobject.name}}</strong></td>
                                        <td width="">{% if tobject.description != None %}{{tobject.description}}{% endif %}</td>
                                        <td width="20%">
                                        
                                        </td>
                                        <td width="50%">
                                            <a href="{% url 'view____singularmodname___' ___firstid___  tobject.id  %}"
                                            class="btn btn-sm btn-primary"><i class="bi bi-eye"></i></a>
                                            &nbsp;&nbsp;
                                            <a href="{% url 'edit____singularmodname___' ___firstid___  tobject.id %}"
                                            class="btn btn-sm btn-warning"><i class="bi bi-pencil-square"></i></a>
                                            &nbsp;&nbsp;
                                            <a href="{% url 'permanent_deletion____singularmodname___' ___firstid___  tobject.id %}"
                                            class="btn btn-sm btn-danger"><i class="bi bi-x-square"></i></a>
                                            &nbsp;&nbsp;
                                            <a href="{% url 'restore____singularmodname___' ___firstid___  tobject.id %}"
                                            class="btn btn-sm btn-success"><i class="bi bi-x-square"></i></a>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                                    <tr>
                                        <td colspan="7">
                                            {% include 'app_common/common_files/pagination.html' %}
                                        </td>
                                    </tr>                        
                            </table>
                        <!-- end display -->
                </div>
            </div>        
        </div>
    </div>
</div>
</form>
<script>
// Select all / checkbox
function checkUncheck(checkBox) {
    get = document.getElementsByName('selected_item');
    for(var i=0; i<get.length; i++) {
        get[i].checked = checkBox.checked;
    }
}
</script>

<script>
    // pagination select
document.addEventListener("DOMContentLoaded", function () {
  const redirectSelect = document.getElementById("paginationselect");
  redirectSelect.addEventListener("change", function () {
    const selectedValue = redirectSelect.value;
    
    // Redirect the user based on the selected value
    if (selectedValue === "5") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=5";
    } else if (selectedValue === "10") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=10";
    } else if (selectedValue === "15") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=15";
    } else if (selectedValue === "25") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___  %}?page=1&all=25";
    } else if (selectedValue === "50") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=50";
    } else if (selectedValue === "100") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=100";
    } else if (selectedValue === "all") {
      window.location.href = "{% url 'list____pluralmodname___' ___firstid___ %}?page=1&all=all";
    } 
    // Add more conditions for other options as needed
  });
});
</script>

<script>
    $(".sortable_table").find("tbody").sortable({
      items: "> tr",
      handle: ".drag-handle",
      appendTo: "parent",
      cancel: "[contenteditable]",
      update: function(event, ui) {
              var serialOrder = $('#sortable').sortable('serialize');
              var arrayOrder = $('#sortable').sortable('toArray');
              //alert(arrayOrder);
              $.ajax({
                url: '/common/common_ajax/ajax_update_model_list_sorted/',
                type: 'POST',
                data : {
                  'csrfmiddlewaretoken': "{{ csrf_token }}",
                  'model_name': '___MODELNAME___',
                  'app_name': '___APPNAME___',
                  'sorted_list_data': JSON.stringify(arrayOrder),
                  
                },
                dataType: 'json',
                success: function(data) {
                  console.log(data);
                }
              })
            }
    });
    </script>

<!-- End: Content -->
{% endblock content %}
"""


create_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% load mptt_tags %}
{% block content %}
{% include 'app_common/common_files/navbar.html' %}
{% include 'app_jivapms/mod_web/common_files/css.html' %}

<!-- Begin: Content -->
<div class="content-wrapper">
   {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
    
    {% include 'app_organization/mod_project/sidebar_menu.html' %}
    <form method="post">
    {% csrf_token %}
    <div class="contentbar mb-5" id="contentbar">
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>{% if form.instance.pk %}Edit{% else %}Create{% endif %} 
                                ___DISPMODNAMESINGULAR___</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___' ___firstid___ %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAMESINGULAR___(s)</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th colspan="2">{{page_title}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td width="15%">
                                <strong>___DISPMODNAMESINGULAR___</strong>
                            </td>
                            <td>
                                {{form.name|as_crispy_field}}
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Description</strong>
                            </td>
                            <td>
                                {{form.description|as_crispy_field}}
                            </td>
                        </tr>
                       <tr>
                            <td colspan="2" class="text-center"><button type="submit"
                                class="btn btn-sm btn-success">Save</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
</div>
</form>
<script>
    focusField = document.getElementById('id_name');
    focusField.focus();
</script>

<!-- End: Content -->
{% endblock content %}
"""

edit_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% load mptt_tags %}
{% block content %}
{% include 'app_common/common_files/navbar.html' %}
{% include 'app_jivapms/mod_web/common_files/css.html' %}

<!-- Begin: Content -->
<div class="content-wrapper">
   {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
    
    {% include 'app_organization/mod_project/sidebar_menu.html' %}
    <form method="post">
    {% csrf_token %}
    <div class="contentbar mb-5" id="contentbar">
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>{% if form.instance.pk %}Edit{% else %}Create{% endif %} 
                                ___DISPMODNAMESINGULAR___</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___' ___firstid___ %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAMESINGULAR___(s)</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th colspan="2">
                                <div class="container-fluid-width">
                                    <div class="row">
                                        <div class="col col-md-5">
                                            {{page_title}}:: {{form.instance}}
                                        </div>
                                        <div class="col col-md-7">
                                            <div class="text-end">
                                                <a href="{% url 'view____singularmodname___' ___firstid___ form.instance.id %}" class="btn btn-sm btn-primary"><b>View</b></a>
                                                &nbsp;&nbsp;&nbsp;
                                                <a href="{% url 'delete____singularmodname___' ___firstid___ form.instance.id %}" class="btn btn-sm btn-danger"><b>Delete</b></a>
                                                
                                            </div>
    
                                        </div>
                                    </div>
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td width="15%">
                                <strong>___DISPMODNAMESINGULAR___</strong>
                            </td>
                            <td>
                                {{form.name|as_crispy_field}}
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Description</strong>
                            </td>
                            <td>
                                {{form.description|as_crispy_field}}
                            </td>
                        </tr>
                       <tr>
                            <td colspan="2" class="text-center"><button type="submit"
                                class="btn btn-sm btn-success">Save</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    </div>
</div>
</form>
<script>
    focusField = document.getElementById('id_name');
    focusField.focus();
</script>

<!-- End: Content -->
{% endblock content %}
"""

delete_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% load mptt_tags %}
{% block content %}
{% include 'app_common/common_files/navbar.html' %}
{% include 'app_jivapms/mod_web/common_files/css.html' %}


<!-- Begin: Content -->
<div class="content-wrapper">
   {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
    
    {% include 'app_organization/mod_project/sidebar_menu.html' %}
    <form method="post">
    {% csrf_token %}
    <div class="contentbar mb-5" id="contentbar">
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>Delete 
                                ___DISPMODNAMESINGULAR___ :: {{object}}</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___' ___firstid___ %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAMESINGULAR___(s)</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <div class="container-fluid-width">
                                <div class="row">
                                    <div class="col col-md-5">
                                        {{page_title}}:: {{object}}
                                    </div>
                                    <div class="col col-md-7">
                                        <div class="text-end">
                                            <a href="{% url 'edit____singularmodname___' ___firstid___ object.id %}" class="btn btn-sm btn-primary"><b>Edit</b></a>
                                            &nbsp;&nbsp;&nbsp;
                                            <a href="{% url 'view____singularmodname___' ___firstid___ object.id %}" class="btn btn-sm btn-danger"><b>View</b></a>
                                            
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                          <td colspan="2" class="text-center">
                            <div class="row">
                                <div class="col col-md-12 text-center">
                                    <p>Are you sure you want to delete "{{ object.name }}"?</p>
                                    <form method="post">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-sm btn-danger">Confirm</button> 
                                        &nbsp;&nbsp;&nbsp;
                                        <a href="{% url 'list____pluralmodname___' ___firstid___ %}" class="btn btn-sm btn-warning">Cancel</a>
                                    </form>
                                </div>
                            </div>
                          </td>
                        </tr>
                      
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    </div>
</div>
</form>
<!-- End: Content -->
{% endblock content %}
"""

permanent_deletion_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% load mptt_tags %}
{% block content %}
{% include 'app_common/common_files/navbar.html' %}
{% include 'app_jivapms/mod_web/common_files/css.html' %}


<!-- Begin: Content -->
<div class="content-wrapper">
   {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
    
    {% include 'app_organization/mod_project/sidebar_menu.html' %}
    <form method="post">
    {% csrf_token %}
    <div class="contentbar mb-5" id="contentbar">
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>Permanent Deletion 
                                ___DISPMODNAMESINGULAR___ :: {{object}}</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___' ___firstid___ %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAMESINGULAR___(s)</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <div class="container-fluid-width">
                                <div class="row">
                                    <div class="col col-md-5">
                                        Permanently Deleting this record. Only Admins can recover.
                                    </div>
                                    <div class="col col-md-7">
                                        <div class="text-end">
                                            <a href="{% url 'edit____singularmodname___' ___firstid___ object.id %}" class="btn btn-sm btn-primary"><b>Edit</b></a>
                                            &nbsp;&nbsp;&nbsp;
                                            <a href="{% url 'view____singularmodname___' ___firstid___ object.id %}" class="btn btn-sm btn-danger"><b>View</b></a>
                                            
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                          <td colspan="2" class="text-center">
                            <div class="row">
                                <div class="col col-md-12 text-center">
                                    <p>Are you sure you want to <b>PERMANENTLY</b> delete "{{ object.name }}"?</p>
                                    <form method="post">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-sm btn-danger">Confirm</button> 
                                        &nbsp;&nbsp;&nbsp;
                                        <a href="{% url 'list____pluralmodname___' ___firstid___ %}" class="btn btn-sm btn-warning">Cancel</a>
                                    </form>
                                </div>
                            </div>
                          </td>
                        </tr>
                      
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    </div>
</div>
</form>
<!-- End: Content -->
{% endblock content %}
"""
view_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% load mptt_tags %}
{% block content %}
{% include 'app_common/common_files/navbar.html' %}
{% include 'app_jivapms/mod_web/common_files/css.html' %}


<!-- Begin: Content -->
<div class="content-wrapper">
   {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
    
    {% include 'app_organization/mod_project/sidebar_menu.html' %}
    <form method="post">
    {% csrf_token %}
    <div class="contentbar mb-5" id="contentbar">
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>View 
                                ___DISPMODNAME___ :: {{object}}</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___' ___firstid___ %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAME___</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th colspan="2">
                                <div class="container-fluid-width">
                                    <div class="row">
                                        <div class="col col-md-5">
                                            {{page_title}}:: {{object}}
                                        </div>
                                        <div class="col col-md-7">
                                            <div class="text-end">
                                                <a href="{% url 'edit____singularmodname___' ___firstid___ object.id %}" class="btn btn-sm btn-primary"><b>Edit</b></a>
                                                &nbsp;&nbsp;&nbsp;
                                                <a href="{% url 'delete____singularmodname___' ___firstid___ object.id %}" class="btn btn-sm btn-danger"><b>Delete</b></a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td width="15%">
                                <strong>___DISPMODNAMESINGULAR___</strong>
                            </td>
                            <td>
                                {% if object.name != None %}{{object.name}}{% endif %}
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Description</strong>
                            </td>
                            <td>
                                {% if object.description != None %}{{object.description}}{% endif %}
                            </td>
                        </tr>                       
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    </div>
</div>
</form>
<!-- End: Content -->
{% endblock content %}
"""


breadcrumb_html = """
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
<!-- Begin: Breadcrumb -->
<nav aria-label="breadcrumb" class="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        {% if org_id != None %}
            <li class="breadcrumb-item"><a href="{% url 'list_organizations' %}">Organizations</a></li>
            <li class="breadcrumb-item"><a href="{% url 'list_organizations' %}">{{org}}</a></li>
            {% if project != None %}
                <li class="breadcrumb-item"><a href="{% url 'list_projects' org_id %}">Projects</a></li>
                <li class="breadcrumb-item"><a href="{% url 'project_home' org_id project.id %}">{{project.id}}</a></li>
            {% endif %}
        {% endif %}
        <li class="breadcrumb-item active" aria-current="page">
            <a href=""></a>
        </li>
       
    </ol>
</nav>
<!-- End: Breadcrumb -->
"""

urls_py = """
from django.urls import path, include

from ___APPNAME___.mod____singularmodname___ import views____singularmodname___


urlpatterns = [
    # ___APPNAME___/___pluralmodname___: DB/Model: ___MODELNAME___
    path('list____pluralmodname___/<int:___firstid___>/', views____singularmodname___.list____pluralmodname___, name='list____pluralmodname___'),
    path('list_deleted____pluralmodname___/<int:___firstid___>/', views____singularmodname___.list_deleted____pluralmodname___, name='list_deleted____pluralmodname___'),
    path('create____singularmodname___/<int:___firstid___>/', views____singularmodname___.create____singularmodname___, name='create____singularmodname___'),
    path('edit____singularmodname___/<int:___firstid___>/<int:___secondid___>/', views____singularmodname___.edit____singularmodname___, name='edit____singularmodname___'),
    path('delete____singularmodname___/<int:___firstid___>/<int:___secondid___>/', views____singularmodname___.delete____singularmodname___, name='delete____singularmodname___'),
    path('permanent_deletion____singularmodname___/<int:___firstid___>/<int:___secondid___>/', views____singularmodname___.permanent_deletion____singularmodname___, name='permanent_deletion____singularmodname___'),
    path('restore____singularmodname___/<int:___firstid___>/<int:___secondid___>/', views____singularmodname___.restore____singularmodname___, name='restore____singularmodname___'),
    path('view____singularmodname___/<int:___firstid___>/<int:___secondid___>/', views____singularmodname___.view____singularmodname___, name='view____singularmodname___'),
    path('dashboard____singularmodname___/<int:___firstid___>/', views____singularmodname___.___singularmodname____dashboard, name='___singularmodname____dashboard'),
    path('settings____singularmodname___/<int:___firstid___>/', views____singularmodname___.___singularmodname____settings, name='___singularmodname____settings'),
]
"""


## models 
models_py = """
from ___APPNAME___.mod_app.all_model_imports import *
from ___firstappname___.mod___singularfirstmodname___.models___singularfirstmodname___ import *
from app_common.mod_common.models_common import *

class ___MODELNAME___(BaseModelImpl):
    ___firstidfkref___ = models.ForeignKey('___firstappname___.___FIRSTMODELNAME___', on_delete=models.CASCADE, 
                            related_name="___firstidfkref_______pluralmodname___", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author____pluralmodname___")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
"""
## views

list_objects_view_py = """
from ___APPNAME___.mod_app.all_view_imports import *
from ___APPNAME___.mod____singularmodname___.models____singularmodname___ import *
from ___APPNAME___.mod____singularmodname___.forms____singularmodname___ import *

from ___firstappname___.mod___singularfirstmodname___.models___singularfirstmodname___ import *

from app_common.mod_common.models_common import *

app_name = '___APPNAME___'
app_version = '___appversion___'

module_name = '___pluralmodname___'
module_path = f'___modulepath___'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list____pluralmodname___(request, ___firstid___):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ___MODELNAME___.objects.filter(name__icontains=search_query, 
                                            ___firstid___=___firstid___, **viewable_dict).order_by('position')
    else:
        tobjects = ___MODELNAME___.objects.filter(active=True, ___firstid___=___firstid___).order_by('position')
        deleted = ___MODELNAME___.objects.filter(active=False, deleted=False,
                                ___firstid___=___firstid___,
                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
             
        if 'selected_item' in request.POST:  # Correct the typo here
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  # Ensure item_id is converted to int if necessary
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list____pluralmodname___', ___firstid___=___firstid___)
            return redirect('list____pluralmodname___', ___firstid___=___firstid___)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list____pluralmodname___',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'___MODNAME___ List',
    }       
    template_file = f"{app_name}/{module_path}/list____pluralmodname___.html"
    return render(request, template_file, context)

"""


list_deleted_objects_view_py = """


# ============================================================= #
@login_required
def list_deleted____pluralmodname___(request, ___firstid___):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ___MODELNAME___.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            ___firstid___=___firstid___, **viewable_dict).order_by('position')
    else:
        tobjects = ___MODELNAME___.objects.filter(active=False, deleted=False, ___firstid___=___firstid___,
                                            **viewable_dict).order_by('position')        
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
     
        if 'selected_item' in request.POST:  # Correct the typo here
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  # Ensure item_id is converted to int if necessary
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(___MODELNAME___, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(___MODELNAME___, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list____pluralmodname___', ___firstid___=___firstid___)
                redirect('list____pluralmodname___', ___firstid___=___firstid___)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted____pluralmodname___',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'___MODNAME___ List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted____pluralmodname___.html"
    return render(request, template_file, context)

"""


create_object_view_py = """
# Create View
@login_required
def create____singularmodname___(request, ___firstid___):
    user = request.user
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    if request.method == 'POST':
        form = ___MODELNAME___Form(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.___firstid___ = ___firstid___
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list____pluralmodname___', ___firstid___=___firstid___)
    else:
        form = ___MODELNAME___Form()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create____singularmodname___',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,
        'form': form,
        'page_title': f'Create ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/create____singularmodname___.html"
    return render(request, template_file, context)


"""
view_object_view_py = """
@login_required
def view____singularmodname___(request, ___firstid___, ___secondid___):
    user = request.user
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    object = get_object_or_404(___MODELNAME___, pk=___secondid___, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view____singularmodname___',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,
        'object': object,
        'page_title': f'View ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/view____singularmodname___.html"
    return render(request, template_file, context)

"""
edit_object_view_py = """
# Edit
@login_required
def edit____singularmodname___(request, ___firstid___, ___secondid___):
    user = request.user
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    object = get_object_or_404(___MODELNAME___, pk=___secondid___, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ___MODELNAME___Form(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.___firstid___ = ___firstid___
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list____pluralmodname___', ___firstid___=___firstid___)
    else:
        form = ___MODELNAME___Form(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit____singularmodname___',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/edit____singularmodname___.html"
    return render(request, template_file, context)

"""
delete_object_view_py = """
@login_required
def delete____singularmodname___(request, ___firstid___, ___secondid___):
    user = request.user
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    object = get_object_or_404(___MODELNAME___, pk=___secondid___, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list____pluralmodname___', ___firstid___=___firstid___)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete____singularmodname___',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/delete____singularmodname___.html"
    return render(request, template_file, context)
"""
permanent_deletion_object_view_py = """
@login_required
def permanent_deletion____singularmodname___(request, ___firstid___, ___secondid___):
    user = request.user
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    object = get_object_or_404(___MODELNAME___, pk=___secondid___, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list____pluralmodname___', ___firstid___=___firstid___)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion____singularmodname___',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion____singularmodname___.html"
    return render(request, template_file, context)
"""
restore_object_view_py = """
@login_required
def restore____singularmodname___(request,  ___firstid___, ___secondid___):
    user = request.user
    object = get_object_or_404(___MODELNAME___, pk=___secondid___, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list____pluralmodname___', ___firstid___=___firstid___)
   
"""

# Dashboard view function
dashboard_view_py = """
@login_required
def ___singularmodname____dashboard(request, ___firstid___):
    user = request.user
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    
    # Get total counts
    total_count = ___MODELNAME___.objects.filter(___firstid___=___firstid___, **viewable_dict).count()
    active_count = ___MODELNAME___.objects.filter(___firstid___=___firstid___, active=True, **viewable_dict).count()
    archived_count = ___MODELNAME___.objects.filter(___firstid___=___firstid___, active=False, deleted=False, **viewable_dict).count()
    
    # Get recent items (created in last 30 days)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    recent_count = ___MODELNAME___.objects.filter(___firstid___=___firstid___, 
                                           created_at__gte=thirty_days_ago,
                                           **viewable_dict).count()
    
    # Get recent items for table display
    recent_items = ___MODELNAME___.objects.filter(___firstid___=___firstid___, active=True, 
                                           **viewable_dict).order_by('-created_at')[:10]
    
    # Prepare chart data
    # 1. Timeline data - Items created per month for the last 6 months
    six_months_ago = timezone.now() - timezone.timedelta(days=180)
    items_by_month = ___MODELNAME___.objects.filter(
        ___firstid___=___firstid___,
        created_at__gte=six_months_ago,
        **viewable_dict
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Format for Chart.js
    months = []
    counts = []
    
    # Get all months in the last 6 months period
    current_date = timezone.now().date().replace(day=1)
    date_list = []
    for i in range(6):
        new_date = current_date - timezone.timedelta(days=30*i)
        date_list.append(new_date)
    date_list.reverse()  # Oldest first
    
    # Format months and fill in zeroes for months with no data
    month_data = {item['month'].strftime('%Y-%m'): item['count'] for item in items_by_month}
    
    for date in date_list:
        month_key = date.strftime('%Y-%m')
        months.append(date.strftime('%b %Y'))
        counts.append(month_data.get(month_key, 0))
    
    # 2. Status distribution data
    status_labels = ['Active', 'Archived', 'Deleted']
    status_data = [
        active_count,
        archived_count,
        ___MODELNAME___.objects.filter(___firstid___=___firstid___, deleted=True, **viewable_dict).count()
    ]
    
    # Prepare stats data
    stats = {
        'total': total_count,
        'active': active_count,
        'recent': recent_count,
        'archived': archived_count
    }
    
    # Prepare chart data dictionary
    chart_data = {
        'timeline_labels': months,
        'timeline_data': counts,
        'status_labels': status_labels,
        'status_data': status_data
    }
    
    # Convert to JSON for template
    import json
    chart_data_json = {
        'timeline_labels': json.dumps(months),
        'timeline_data': json.dumps(counts),
        'status_labels': json.dumps(status_labels),
        'status_data': json.dumps(status_data)
    }
    
    # Send outputs info, template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': '___singularmodname____dashboard',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,
        'module_title': '___DISPMODNAME___',
        'user': user,
        'stats': stats,
        'recent_items': recent_items,
        'chart_data': chart_data_json,
        'page_title': '___DISPMODNAME___ Dashboard',
    }
    
    template_file = f"{app_name}/{module_path}/dashboard____singularmodname___.html"
    return render(request, template_file, context)
"""

# Settings view function
settings_view_py = """
@login_required
def ___singularmodname____settings(request, ___firstid___):
    user = request.user
    ___firstname___ = ___FIRSTMODELNAME___.objects.get(id=___firstid___, active=True, 
                                                **first_viewable_dict)
    ___ORGFIX1___
    
    # Default settings
    default_settings = {
        'default_view': 'list',
        'items_per_page': 25,
        'enable_notifications': False,
        'date_format': 'MM/DD/YYYY',
        'theme': 'light',
        'email_integration_enabled': False,
        'api_enabled': False,
        'calendar_integration_enabled': False,
        'caching_strategy': 'normal',
        'logging_level': 'error',
        'debug_mode': False
    }
    
    # Get user settings from database or session
    # For demonstration purposes, we'll use default settings
    # In a real application, you might load these from the database
    settings = default_settings
    
    # Handle form submissions
    if request.method == 'POST':
        # Determine which form was submitted based on request data
        if 'default_view' in request.POST:
            # General settings form
            settings['default_view'] = request.POST.get('default_view')
            settings['items_per_page'] = int(request.POST.get('items_per_page', 25))
            settings['enable_notifications'] = 'enable_notifications' in request.POST
            settings['date_format'] = request.POST.get('date_format')
            messages.success(request, 'General settings updated successfully.')
            
        elif 'theme' in request.POST:
            # Display settings form
            settings['theme'] = request.POST.get('theme')
            # Handle visible columns (would be stored as a list/array)
            messages.success(request, 'Display settings updated successfully.')
            
        elif 'default_role' in request.POST:
            # Permissions settings form
            settings['default_role'] = request.POST.get('default_role')
            messages.success(request, 'Permission settings updated successfully.')
            
        elif 'email_integration_enabled' in request.POST:
            # Integration settings form
            settings['email_integration_enabled'] = 'email_integration_enabled' in request.POST
            settings['email_template'] = request.POST.get('email_template')
            settings['api_enabled'] = 'api_enabled' in request.POST
            settings['calendar_integration_enabled'] = 'calendar_integration_enabled' in request.POST
            settings['calendar_provider'] = request.POST.get('calendar_provider')
            messages.success(request, 'Integration settings updated successfully.')
            
        elif 'caching_strategy' in request.POST:
            # Advanced settings form
            settings['caching_strategy'] = request.POST.get('caching_strategy')
            settings['logging_level'] = request.POST.get('logging_level')
            settings['debug_mode'] = 'debug_mode' in request.POST
            messages.success(request, 'Advanced settings updated successfully.')
        
        # Save settings to database or session
        # In a real application, this would save to a database
        # For this example, we'll just update our settings dictionary
        
        # Redirect to avoid form resubmission
        return redirect('___singularmodname____settings', ___firstid___=___firstid___)
    
    # Send outputs info, template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': '___singularmodname____settings',
        '___firstname___': ___firstname___,
        '___firstid___': ___firstid___,
        ___ORGPARAMFIX1___
        'module_path': module_path,
        'module_title': '___DISPMODNAME___',
        'user': user,
        'settings': settings,
        'page_title': '___DISPMODNAME___ Settings',
    }
    
    template_file = f"{app_name}/{module_path}/settings____singularmodname___.html"
    return render(request, template_file, context)
"""
###############################################################################

import inflect
import sys 
import os
from utils.utils import *
p = inflect.engine()


#####################################################################
# configuration
# example2: Model -> model use _views_with_org.py to propogate org
version = "v1"
app_name = "app_automate"
first_model = "Organization"
module_name = "content"
# the above is an example for reference, while we pickup from command line
if len(sys.argv) < 2:
    print("Usage: python CRUD_ONE_LEVEL.py  <projectname>.<app_name> <firstapp>.<first_model> <module_name:Content or ContentType> the connected")
    print("Example: python scriptname jiva.organization organization.organization project_workflow")
    print("\t\t means that project_workflow is connected with the organization model one level")
    print("\t\t this is after creating the project.app.mod from django")
    sys.exit(1)  # Exit the program indicating that there was an issue
script_name = os.path.splitext(os.path.basename(__file__))[0]
# Read arguments
project_app_input = sys.argv[1]
project_name = project_app_input.split(".")[0]
app_name = project_app_input.split(".")[1]
app_name = app_name.lower()
app_name = f"app_{app_name}"
input_model = sys.argv[2]
first_app_name = input_model.split(".")[0].lower()
first_app_name = f"app_{first_app_name}"
first_model = input_model.split(".")[1]
print(f">>> === first_app_name: {first_app_name} === <<<")
print(f">>> === first_model: {first_model} === <<<")

#first_model = sys.argv[2]
ref_module_name = sys.argv[3]

module_name = format_title_re(ref_module_name)
model_name = module_name.title() # Title Content / ContentType for ORM Model
model_name = model_name.replace("_", "")
db_app_name = module_name.lower()

second_id = module_name.lower() + "_id"
# module_path_prefix = app_name.split("_")[1]
# module_path = f"{module_path_prefix}/{module_name}"
module_path = f"mod_{module_name}"

### first model name processing
# >>>> first_id_fk_ref = process_word(first_model).lower() 
first_id_fk_ref = first_model.lower() 
first_id = first_model.lower() + "_id"

first_model_name_import = first_model if p.singular_noun(first_model) else p.plural(first_model)
first_model_name_import = first_model_name_import.lower()
singular_firstmodule_name = first_model.lower() if p.singular_noun(first_model) is False else p.singular_noun(first_model)
plural_firstmodule_name = first_model.lower() if p.singular_noun(first_model) else p.plural(first_model)

#first_app_name = f"app_{singular_firstmodule_name}".lower()


first_name = first_model.lower()
first_model_name = first_model.title()
first_model_name = first_model_name.replace("_", "")

print(f">>> === singularfirstmodname: {singular_firstmodule_name} === <<<")


org_fix_flag = False # needs to be true if not Organization
org_fix = ""
org_param_fix = ""

if org_fix_flag is True:
    org_fix = "org_id = ___firstname___.area.template.org_id\n    org =  Organization.objects.get(id=org_id, active=True)"
    org_param_fix = "'org': org,\n        'org_id': org_id,"






#######################################################################

display_module_name = module_name.replace('_', ' ').title()
#display_module_name_singular = p.singular_noun(display_module_name)
display_module_name_singular = display_module_name if p.singular_noun(display_module_name) is False else p.singular_noun(display_module_name)
#singular_module_name = p.singular_noun(module_name)
singular_module_name = module_name if p.singular_noun(module_name) is False else p.singular_noun(module_name)
plural_module_name = module_name if p.singular_noun(module_name) else p.plural(module_name)

lc_singular_module_name = singular_module_name.lower()
lc_plural_module_name = module_name.lower() if p.singular_noun(module_name) else p.plural(module_name)

print(f">>> === singular_module_name: {lc_singular_module_name} === <<<")
print(f">>> === plural_module_name: {lc_plural_module_name} === <<<")


############################################# END OF CODE #############################################
var_value_dict = {
    "___APPNAME___": app_name,
    "___MODNAME___": module_name.capitalize(),
    "___DISPMODNAME___": display_module_name,
    "___DISPMODNAMESINGULAR___": display_module_name_singular,
    "___singularmodname___": singular_module_name.lower(),
    "___pluralmodname___": lc_plural_module_name,
    "___UCsingularmodname___": singular_module_name.capitalize(),
    "___MODELNAME___": model_name,
    "___FIRSTMODELNAME___": first_model_name,
    "___dbappname___": db_app_name,
    "___firstid___": first_id,
    "___firstidfkref___": first_id_fk_ref,
    "___secondid___": second_id,
    "___appversion___": version,
    "___modulepath___": module_path,
    "___ORGFIX1___": org_fix,
    "___ORGPARAMFIX1___": org_param_fix,
    "___firstmodelnameimport___": first_model_name_import,
    "___firstname___": first_name,
    "___firstappname___": first_app_name,
    "__singularfirstmodname___": singular_firstmodule_name,
    "__pluralfirstmodname___": plural_firstmodule_name,
    "__pluralfirstmodnameuc___": plural_firstmodule_name.capitalize(),
    
}


# Dashboard template
dashboard_html_template = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras %}

{% block head_extra %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
    .dashboard-card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
    }
    .stat-card {
        padding: 15px;
        border-radius: 8px;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        height: 130px;
    }
    .stat-number {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .stat-title {
        font-size: 16px;
        text-transform: uppercase;
    }
    .bg-primary-gradient {
        background: linear-gradient(45deg, #4a6fdc, #6c8df5);
    }
    .bg-success-gradient {
        background: linear-gradient(45deg, #2e9b4f, #38c964);
    }
    .bg-warning-gradient {
        background: linear-gradient(45deg, #f2994a, #f5bc62);
    }
    .bg-info-gradient {
        background: linear-gradient(45deg, #3daec9, #57c6e0);
    }
    .chart-container {
        position: relative;
        margin: auto;
        height: 250px;
    }
    .section-title {
        font-size: 20px;
        margin-bottom: 15px;
        color: #333;
        font-weight: 600;
        padding-bottom: 5px;
        border-bottom: 2px solid #f0f0f0;
    }
    .quick-action-btn {
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background: #f9f9f9;
        text-align: center;
        transition: all 0.3s;
    }
    .quick-action-btn:hover {
        background: #f0f0f0;
        border-color: #d0d0d0;
    }
    .quick-action-btn i {
        font-size: 24px;
        margin-bottom: 8px;
        display: block;
    }
</style>
{% endblock %}

{% block content %}
{% include 'app_common/common_files/navbar.html' %}

<div class="content-wrapper">
    {% include 'app_organization/mod_project/sidebar_menu.html' %}

    <div class="contentbar" id="contentbar">
        <div class="container-fluid py-4">
            <!-- Header Section -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="dashboard-card">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h1 class="mb-0"><i class="bi bi-speedometer2 me-2"></i>___DISPMODNAME___ Dashboard</h1>
                                <p class="text-muted mb-0">Overview and statistics for your ___DISPMODNAME___</p>
                            </div>
                            <a href="{% url 'list____pluralmodname___' ___firstid___ %}" class="btn btn-outline-primary">
                                <i class="bi bi-list"></i> View All ___DISPMODNAME___
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Key Stats Cards -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="stat-card bg-primary-gradient">
                        <div class="stat-number">{{ stats.total }}</div>
                        <div class="stat-title">Total ___DISPMODNAME___</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card bg-success-gradient">
                        <div class="stat-number">{{ stats.active }}</div>
                        <div class="stat-title">Active</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card bg-warning-gradient">
                        <div class="stat-number">{{ stats.recent }}</div>
                        <div class="stat-title">Recent (30d)</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card bg-info-gradient">
                        <div class="stat-number">{{ stats.archived }}</div>
                        <div class="stat-title">Archived</div>
                    </div>
                </div>
            </div>
            
            <!-- Quick Actions Section -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="dashboard-card">
                        <h3 class="section-title">Quick Actions</h3>
                        <div class="row">
                            <div class="col-md-3 col-sm-6 mb-3">
                                <a href="{% url 'create____singularmodname___' ___firstid___ %}" class="quick-action-btn d-block text-decoration-none">
                                    <i class="bi bi-plus-square text-success"></i>
                                    <span>Create New</span>
                                </a>
                            </div>
                            <div class="col-md-3 col-sm-6 mb-3">
                                <a href="{% url 'list____pluralmodname___' ___firstid___ %}" class="quick-action-btn d-block text-decoration-none">
                                    <i class="bi bi-list-ul text-primary"></i>
                                    <span>View All</span>
                                </a>
                            </div>
                            <div class="col-md-3 col-sm-6 mb-3">
                                <a href="{% url 'list_deleted____pluralmodname___' ___firstid___ %}" class="quick-action-btn d-block text-decoration-none">
                                    <i class="bi bi-archive text-warning"></i>
                                    <span>View Archived</span>
                                </a>
                            </div>
                            <div class="col-md-3 col-sm-6 mb-3">
                                <a href="{% url '___singularmodname____settings' ___firstid___ %}" class="quick-action-btn d-block text-decoration-none">
                                    <i class="bi bi-gear text-secondary"></i>
                                    <span>Settings</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Section -->
            <div class="row mb-4">
                <!-- Creation Over Time -->
                <div class="col-md-6">
                    <div class="dashboard-card">
                        <h3 class="section-title">Creation Timeline</h3>
                        <div class="chart-container" style="position: relative; height:250px;">
                            <canvas id="creationChart"></canvas>
                        </div>
                    </div>
                </div>
                
                <!-- Status Distribution -->
                <div class="col-md-6">
                    <div class="dashboard-card">
                        <h3 class="section-title">Status Distribution</h3>
                        <div class="chart-container" style="position: relative; height:250px;">
                            <canvas id="statusChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Recent Items Table -->
            <div class="row">
                <div class="col-12">
                    <div class="dashboard-card">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h3 class="section-title mb-0">Recent ___DISPMODNAME___</h3>
                            <a href="{% url 'create____singularmodname___' ___firstid___ %}" class="btn btn-sm btn-success">
                                <i class="bi bi-plus-lg"></i> Create New
                            </a>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Name</th>
                                        <th>Description</th>
                                        <th>Created</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for item in recent_items %}
                                    <tr>
                                        <td>{{ forloop.counter }}</td>
                                        <td><strong>{{ item.name }}</strong></td>
                                        <td>{{ item.description|truncatechars:50 }}</td>
                                        <td>{{ item.created_at|date:"M d, Y" }}</td>
                                        <td>
                                            <a href="{% url 'view____singularmodname___' ___firstid___ item.id %}" class="btn btn-sm btn-outline-primary">
                                                <i class="bi bi-eye"></i>
                                            </a>
                                            <a href="{% url 'edit____singularmodname___' ___firstid___ item.id %}" class="btn btn-sm btn-outline-warning">
                                                <i class="bi bi-pencil"></i>
                                            </a>
                                        </td>
                                    </tr>
                                    {% empty %}
                                    <tr>
                                        <td colspan="5" class="text-center py-3">
                                            <p class="text-muted mb-0">No items found</p>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

{% block scripts %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Chart colors
    const colors = [
        'rgba(74, 111, 220, 0.8)',
        'rgba(56, 201, 100, 0.8)',
        'rgba(245, 188, 98, 0.8)',
        'rgba(87, 198, 224, 0.8)',
        'rgba(231, 76, 60, 0.8)',
    ];
    
    // Creation Timeline Chart
    const creationCtx = document.getElementById('creationChart').getContext('2d');
    new Chart(creationCtx, {
        type: 'line',
        data: {
            labels: {{ chart_data.timeline_labels|default:'["Jan", "Feb", "Mar", "Apr", "May", "Jun"]'|safe }},
            datasets: [{
                label: 'New ___DISPMODNAME___',
                data: {{ chart_data.timeline_data|default:'[5, 8, 12, 7, 15, 10]'|safe }},
                borderColor: colors[0],
                backgroundColor: colors[0].replace('0.8', '0.1'),
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
    
    // Status Distribution Chart
    const statusCtx = document.getElementById('statusChart').getContext('2d');
    new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: {{ chart_data.status_labels|default:'["Active", "Archived", "Draft"]'|safe }},
            datasets: [{
                data: {{ chart_data.status_data|default:'[65, 25, 10]'|safe }},
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.8', '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
});
</script>
{% endblock %}

{% endblock content %}
"""

# Settings template
settings_html_template = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras %}

{% block head_extra %}
<style>
    .settings-section {
        margin-bottom: 30px;
    }
    
    .settings-header {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .settings-card {
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .nav-pills .nav-link.active {
        background-color: #4a6fdc;
    }
    
    .nav-pills .nav-link {
        color: #6c757d;
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 5px;
        transition: all 0.2s;
    }
    
    .nav-pills .nav-link:hover {
        background-color: rgba(74, 111, 220, 0.1);
    }
    
    .nav-pills .nav-link i {
        margin-right: 10px;
    }
</style>
{% endblock %}

{% block content %}
{% include 'app_common/common_files/navbar.html' %}

<div class="content-wrapper">
    {% include 'app_organization/mod_project/sidebar_menu.html' %}

    <div class="contentbar" id="contentbar">
        <div class="container-fluid py-4">
            <!-- Header Section -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="settings-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h1 class="mb-0"><i class="bi bi-gear me-2"></i>___DISPMODNAME___ Settings</h1>
                                <p class="text-muted mb-0">Configure your ___DISPMODNAME___ preferences and options</p>
                            </div>
                            <div>
                                <a href="{% url 'list___pluralmodname___' ___firstid___ %}" class="btn btn-outline-primary me-2">
                                    <i class="bi bi-list"></i> View All
                                </a>
                                <a href="{% url '___singularmodname____dashboard' ___firstid___ %}" class="btn btn-outline-info">
                                    <i class="bi bi-speedometer2"></i> Dashboard
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <!-- Settings Navigation -->
                <div class="col-md-3 mb-4">
                    <div class="settings-card">
                        <h5 class="mb-3">Settings Menu</h5>
                        <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                            <button class="nav-link active" id="v-pills-general-tab" data-bs-toggle="pill" data-bs-target="#v-pills-general" type="button" role="tab" aria-controls="v-pills-general" aria-selected="true">
                                <i class="bi bi-sliders"></i> General
                            </button>
                            <button class="nav-link" id="v-pills-display-tab" data-bs-toggle="pill" data-bs-target="#v-pills-display" type="button" role="tab" aria-controls="v-pills-display" aria-selected="false">
                                <i class="bi bi-grid"></i> Display
                            </button>
                            <button class="nav-link" id="v-pills-permissions-tab" data-bs-toggle="pill" data-bs-target="#v-pills-permissions" type="button" role="tab" aria-controls="v-pills-permissions" aria-selected="false">
                                <i class="bi bi-shield-lock"></i> Permissions
                            </button>
                            <button class="nav-link" id="v-pills-integrations-tab" data-bs-toggle="pill" data-bs-target="#v-pills-integrations" type="button" role="tab" aria-controls="v-pills-integrations" aria-selected="false">
                                <i class="bi bi-link-45deg"></i> Integrations
                            </button>
                            <button class="nav-link" id="v-pills-advanced-tab" data-bs-toggle="pill" data-bs-target="#v-pills-advanced" type="button" role="tab" aria-controls="v-pills-advanced" aria-selected="false">
                                <i class="bi bi-gear-wide-connected"></i> Advanced
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Settings Content -->
                <div class="col-md-9">
                    <div class="settings-card">
                        <div class="tab-content" id="v-pills-tabContent">
                            <!-- General Settings -->
                            <div class="tab-pane fade show active" id="v-pills-general" role="tabpanel" aria-labelledby="v-pills-general-tab">
                                <h4 class="mb-4">General Settings</h4>
                                <form method="post" action="">
                                    {% csrf_token %}
                                    <div class="mb-3">
                                        <label for="settingDefaultView" class="form-label">Default View</label>
                                        <select class="form-select" id="settingDefaultView" name="default_view">
                                            <option value="list" {% if settings.default_view == 'list' %}selected{% endif %}>List View</option>
                                            <option value="grid" {% if settings.default_view == 'grid' %}selected{% endif %}>Grid View</option>
                                            <option value="kanban" {% if settings.default_view == 'kanban' %}selected{% endif %}>Kanban View</option>
                                        </select>
                                        <div class="form-text">Select the default view mode for ___DISPMODNAME___.</div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="settingItemsPerPage" class="form-label">Items Per Page</label>
                                        <input type="number" class="form-control" id="settingItemsPerPage" name="items_per_page" value="{{ settings.items_per_page|default:'25' }}" min="5" max="100">
                                        <div class="form-text">Number of items to display per page.</div>
                                    </div>
                                    
                                    <div class="mb-3 form-check">
                                        <input type="checkbox" class="form-check-input" id="settingEnableNotifications" name="enable_notifications" {% if settings.enable_notifications %}checked{% endif %}>
                                        <label class="form-check-label" for="settingEnableNotifications">Enable Notifications</label>
                                        <div class="form-text">Get notifications for changes to ___DISPMODNAME___.</div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="settingDateFormat" class="form-label">Date Format</label>
                                        <select class="form-select" id="settingDateFormat" name="date_format">
                                            <option value="MM/DD/YYYY" {% if settings.date_format == 'MM/DD/YYYY' %}selected{% endif %}>MM/DD/YYYY</option>
                                            <option value="DD/MM/YYYY" {% if settings.date_format == 'DD/MM/YYYY' %}selected{% endif %}>DD/MM/YYYY</option>
                                            <option value="YYYY-MM-DD" {% if settings.date_format == 'YYYY-MM-DD' %}selected{% endif %}>YYYY-MM-DD</option>
                                        </select>
                                        <div class="form-text">Select your preferred date format.</div>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-primary">Save Settings</button>
                                </form>
                            </div>
                            
                            <!-- Display Settings -->
                            <div class="tab-pane fade" id="v-pills-display" role="tabpanel" aria-labelledby="v-pills-display-tab">
                                <h4 class="mb-4">Display Settings</h4>
                                <form method="post" action="">
                                    {% csrf_token %}
                                    <div class="mb-3">
                                        <label for="settingTheme" class="form-label">Theme</label>
                                        <select class="form-select" id="settingTheme" name="theme">
                                            <option value="light" {% if settings.theme == 'light' %}selected{% endif %}>Light</option>
                                            <option value="dark" {% if settings.theme == 'dark' %}selected{% endif %}>Dark</option>
                                            <option value="system" {% if settings.theme == 'system' %}selected{% endif %}>System Default</option>
                                        </select>
                                        <div class="form-text">Select your preferred theme.</div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="form-label">Visible Columns</label>
                                        <div class="row">
                                            <div class="col-md-4">
                                                <div class="form-check mb-2">
                                                    <input class="form-check-input" type="checkbox" id="colName" name="visible_columns[]" value="name" checked disabled>
                                                    <label class="form-check-label" for="colName">Name</label>
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="form-check mb-2">
                                                    <input class="form-check-input" type="checkbox" id="colDescription" name="visible_columns[]" value="description" checked>
                                                    <label class="form-check-label" for="colDescription">Description</label>
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="form-check mb-2">
                                                    <input class="form-check-input" type="checkbox" id="colCreatedAt" name="visible_columns[]" value="created_at" checked>
                                                    <label class="form-check-label" for="colCreatedAt">Created At</label>
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="form-check mb-2">
                                                    <input class="form-check-input" type="checkbox" id="colUpdatedAt" name="visible_columns[]" value="updated_at">
                                                    <label class="form-check-label" for="colUpdatedAt">Updated At</label>
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="form-check mb-2">
                                                    <input class="form-check-input" type="checkbox" id="colAuthor" name="visible_columns[]" value="author">
                                                    <label class="form-check-label" for="colAuthor">Author</label>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="form-text">Select which columns to display in the list view.</div>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-primary">Save Display Settings</button>
                                </form>
                            </div>
                            
                            <!-- Permissions Settings -->
                            <div class="tab-pane fade" id="v-pills-permissions" role="tabpanel" aria-labelledby="v-pills-permissions-tab">
                                <h4 class="mb-4">Permissions Settings</h4>
                                <form method="post" action="">
                                    {% csrf_token %}
                                    <div class="table-responsive mb-4">
                                        <table class="table table-bordered">
                                            <thead class="table-light">
                                                <tr>
                                                    <th>Role</th>
                                                    <th>View</th>
                                                    <th>Create</th>
                                                    <th>Edit</th>
                                                    <th>Delete</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td>Admin</td>
                                                    <td><input type="checkbox" name="perm_admin_view" checked disabled></td>
                                                    <td><input type="checkbox" name="perm_admin_create" checked disabled></td>
                                                    <td><input type="checkbox" name="perm_admin_edit" checked disabled></td>
                                                    <td><input type="checkbox" name="perm_admin_delete" checked disabled></td>
                                                </tr>
                                                <tr>
                                                    <td>Manager</td>
                                                    <td><input type="checkbox" name="perm_manager_view" checked></td>
                                                    <td><input type="checkbox" name="perm_manager_create" checked></td>
                                                    <td><input type="checkbox" name="perm_manager_edit" checked></td>
                                                    <td><input type="checkbox" name="perm_manager_delete"></td>
                                                </tr>
                                                <tr>
                                                    <td>User</td>
                                                    <td><input type="checkbox" name="perm_user_view" checked></td>
                                                    <td><input type="checkbox" name="perm_user_create"></td>
                                                    <td><input type="checkbox" name="perm_user_edit"></td>
                                                    <td><input type="checkbox" name="perm_user_delete"></td>
                                                </tr>
                                                <tr>
                                                    <td>Guest</td>
                                                    <td><input type="checkbox" name="perm_guest_view"></td>
                                                    <td><input type="checkbox" name="perm_guest_create" disabled></td>
                                                    <td><input type="checkbox" name="perm_guest_edit" disabled></td>
                                                    <td><input type="checkbox" name="perm_guest_delete" disabled></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="settingDefaultRole" class="form-label">Default Role for New Users</label>
                                        <select class="form-select" id="settingDefaultRole" name="default_role">
                                            <option value="user" {% if settings.default_role == 'user' %}selected{% endif %}>User</option>
                                            <option value="guest" {% if settings.default_role == 'guest' %}selected{% endif %}>Guest</option>
                                        </select>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-primary">Save Permissions</button>
                                </form>
                            </div>
                            
                            <!-- Integrations Settings -->
                            <div class="tab-pane fade" id="v-pills-integrations" role="tabpanel" aria-labelledby="v-pills-integrations-tab">
                                <h4 class="mb-4">Integration Settings</h4>
                                <form method="post" action="">
                                    {% csrf_token %}
                                    <div class="card mb-3">
                                        <div class="card-body">
                                            <div class="d-flex justify-content-between align-items-center mb-3">
                                                <div>
                                                    <h5 class="card-title mb-0">Email Notifications</h5>
                                                    <p class="text-muted mb-0">Configure email notifications for ___DISPMODNAME___</p>
                                                </div>
                                                <div class="form-check form-switch">
                                                    <input class="form-check-input" type="checkbox" id="emailIntegration" name="email_integration_enabled" {% if settings.email_integration_enabled %}checked{% endif %}>
                                                </div>
                                            </div>
                                            <div class="mb-3">
                                                <label for="emailTemplate" class="form-label">Email Template</label>
                                                <select class="form-select" id="emailTemplate" name="email_template">
                                                    <option value="default" {% if settings.email_template == 'default' %}selected{% endif %}>Default Template</option>
                                                    <option value="minimal" {% if settings.email_template == 'minimal' %}selected{% endif %}>Minimal</option>
                                                    <option value="detailed" {% if settings.email_template == 'detailed' %}selected{% endif %}>Detailed</option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="card mb-3">
                                        <div class="card-body">
                                            <div class="d-flex justify-content-between align-items-center mb-3">
                                                <div>
                                                    <h5 class="card-title mb-0">API Access</h5>
                                                    <p class="text-muted mb-0">Configure API access for ___DISPMODNAME___</p>
                                                </div>
                                                <div class="form-check form-switch">
                                                    <input class="form-check-input" type="checkbox" id="apiAccess" name="api_enabled" {% if settings.api_enabled %}checked{% endif %}>
                                                </div>
                                            </div>
                                            <div class="mb-3">
                                                <label for="apiKey" class="form-label">API Key</label>
                                                <div class="input-group">
                                                    <input type="text" class="form-control" id="apiKey" value="{{ settings.api_key|default:'••••••••••••••••' }}" readonly>
                                                    <button class="btn btn-outline-secondary" type="button">Regenerate</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-primary">Save Integration Settings</button>
                                </form>
                            </div>
                            
                            <!-- Advanced Settings -->
                            <div class="tab-pane fade" id="v-pills-advanced" role="tabpanel" aria-labelledby="v-pills-advanced-tab">
                                <h4 class="mb-4">Advanced Settings</h4>
                                <div class="alert alert-warning" role="alert">
                                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                                    Warning: Changes to these settings may affect system behavior.
                                </div>
                                
                                <form method="post" action="">
                                    {% csrf_token %}
                                    <div class="mb-3">
                                        <label for="settingCaching" class="form-label">Caching Strategy</label>
                                        <select class="form-select" id="settingCaching" name="caching_strategy">
                                            <option value="none" {% if settings.caching_strategy == 'none' %}selected{% endif %}>No Caching</option>
                                            <option value="normal" {% if settings.caching_strategy == 'normal' %}selected{% endif %}>Normal (5 minutes)</option>
                                            <option value="aggressive" {% if settings.caching_strategy == 'aggressive' %}selected{% endif %}>Aggressive (30 minutes)</option>
                                        </select>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="settingLogging" class="form-label">Logging Level</label>
                                        <select class="form-select" id="settingLogging" name="logging_level">
                                            <option value="error" {% if settings.logging_level == 'error' %}selected{% endif %}>Error Only</option>
                                            <option value="warning" {% if settings.logging_level == 'warning' %}selected{% endif %}>Warning & Error</option>
                                            <option value="info" {% if settings.logging_level == 'info' %}selected{% endif %}>Info, Warning & Error</option>
                                            <option value="debug" {% if settings.logging_level == 'debug' %}selected{% endif %}>Debug (Verbose)</option>
                                        </select>
                                    </div>
                                    
                                    <div class="mb-3 form-check">
                                        <input type="checkbox" class="form-check-input" id="settingDebugMode" name="debug_mode" {% if settings.debug_mode %}checked{% endif %}>
                                        <label class="form-check-label" for="settingDebugMode">Enable Debug Mode</label>
                                        <div class="form-text text-warning">This may expose sensitive information. Use with caution.</div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="form-label">Advanced Operations</label>
                                        <div class="d-grid gap-2">
                                            <button type="button" class="btn btn-outline-warning">Rebuild Indexes</button>
                                            <button type="button" class="btn btn-outline-warning">Clear Cache</button>
                                            <button type="button" class="btn btn-outline-danger">Reset All Settings</button>
                                        </div>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-primary">Save Advanced Settings</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
"""

# Custom base template
custom_base_html = """
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}JIVA PMS{% endblock %}</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- jQuery UI -->
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.13.1/themes/base/jquery-ui.css">
    <!-- Custom CSS -->
    <style>
        :root {
            --primary-color: #4a6fdc;
            --secondary-color: #6c8df5;
            --success-color: #38c964;
            --info-color: #57c6e0;
            --warning-color: #f5bc62;
            --danger-color: #e74c3c;
            --light-color: #f8f9fa;
            --dark-color: #343a40;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #f8f9fa;
            color: #333;
        }
        
        .navbar {
            background-color: white;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        }
        
        .sidebar {
            background-color: white;
            min-height: calc(100vh - 56px);
            width: 250px;
            position: fixed;
            top: 56px;
            left: 0;
            box-shadow: 2px 0 15px rgba(0,0,0,0.05);
            transition: all 0.3s;
            z-index: 100;
        }
        
        .sidebar-collapsed {
            margin-left: -250px;
        }
        
        .content-wrapper {
            margin-left: 250px;
            padding: 20px;
            transition: all 0.3s;
        }
        
        .content-expanded {
            margin-left: 0;
        }
        
        .contentbar {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            padding: 20px;
        }
        
        .card {
            border: none;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .btn {
            border-radius: 5px;
            padding: 8px 15px;
            font-weight: 500;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-primary:hover {
            background-color: var(--secondary-color);
            border-color: var(--secondary-color);
        }
        
        .table {
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .table thead th {
            background-color: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
            font-weight: 600;
        }
        
        .breadcrumb {
            background-color: transparent;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        
        .nav-link {
            color: #6c757d;
            font-weight: 500;
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 5px;
            transition: all 0.2s;
        }
        
        .nav-link:hover, .nav-link.active {
            color: var(--primary-color);
            background-color: rgba(74, 111, 220, 0.1);
        }
        
        .nav-link i {
            margin-right: 10px;
        }
    </style>
    {% block head_extra %}{% endblock %}
</head>
<body>
    <div id="app">
        {% block content %}{% endblock %}
    </div>
    
    <!-- jQuery & jQuery UI -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.13.1/jquery-ui.min.js"></script>
    
    <!-- Bootstrap 5 JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JavaScript -->
    <script>
        $(document).ready(function() {
            // Toggle sidebar
            $('#sidebarToggle').on('click', function() {
                $('.sidebar').toggleClass('sidebar-collapsed');
                $('.content-wrapper').toggleClass('content-expanded');
            });
            
            // Initialize tooltips
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        });
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>
"""

html_var_list = [
    list_objects_html_single_level,
    list_deleted_objects_html_single_level,
    create_object_html_single_level,
    edit_object_html_single_level,
    delete_object_html_single_level,
    permanent_deletion_object_html_single_level,
    view_object_html_single_level,
    breadcrumb_html,
    dashboard_html_template,
    settings_html_template,
    custom_base_html
]

views_var_list = [
    list_objects_view_py,
    list_deleted_objects_view_py,
    create_object_view_py,
    edit_object_view_py,
    delete_object_view_py,
    permanent_deletion_object_view_py,
    restore_object_view_py,
    view_object_view_py,
    dashboard_view_py,
    settings_view_py
]

urls_var_list = [
    urls_py,
]

forms_var_list = [
    forms_py
]

models_var_list = [
    models_py,
]

html_files_list = [
    f"list_{lc_plural_module_name}.html",
    f"list_deleted_{lc_plural_module_name}.html",
    f"create_{lc_singular_module_name}.html",
    f"edit_{lc_singular_module_name}.html",
    f"delete_{lc_singular_module_name}.html",
    f"permanent_deletion_{lc_singular_module_name}.html",
    f"view_{lc_singular_module_name}.html",
    f"breadcrumb_{lc_plural_module_name}.html",
    f"dashboard_{lc_singular_module_name}.html",
    f"settings_{lc_singular_module_name}.html",
    f"base.html"
]
views_files_list = [f"views_{lc_singular_module_name}.py"]
urls_files_list = [f"urls_{lc_singular_module_name}.py"]
forms_files_list = [f"forms_{lc_singular_module_name}.py"]
models_files_list = [f"models_{lc_singular_module_name}.py"]
# File processing functions

def replace_all_vars_with_values(var_value_dict, file_data):
    for var, value in var_value_dict.items():
        file_data = file_data.replace(var, value)
    return file_data

def write_file(file_name, file_data):
    open(file_name, "w").write(file_data)
def process_file_str(file_str, var_value_dict):
    file_str = replace_all_vars_with_values(var_value_dict, file_str)
    return file_str

# Define dictionaries to hold file lists and variable lists for each module
file_lists = {
    "html": html_files_list,
    "views": views_files_list,
    "urls": urls_files_list,
    "forms": forms_files_list,
    "models": models_files_list,
}

var_lists = {
    "html": html_var_list,
    "views": views_var_list,
    "urls": urls_var_list,
    "forms": forms_var_list,
    "models": models_var_list,
}

process_modules = ["html", "views", "urls", "forms", "models"]
# outcome folder
outcome = f"../outcome/{script_name}"

if not os.path.exists(outcome):
    os.makedirs(outcome)
    os.makedirs(f"{outcome}/python")
    os.makedirs(f"{outcome}/html")
else:
    shutil.rmtree(outcome)
    os.makedirs(outcome)
    os.makedirs(f"{outcome}/python")
    os.makedirs(f"{outcome}/html")
    print(f">>> === {outcome} cleaned, dir ready === <<<")

for module in process_modules:
    # Access the appropriate lists from the dictionaries
    current_files_list = file_lists[module]
    current_var_list = var_lists[module]

    # Special handling for views module
    if module == "views":
        # Assume lc_plural_module_name is defined somewhere globally or passed into this context
        view_file_name = f"{outcome}/python/views_{lc_singular_module_name}.py"
        with open(view_file_name, "w") as file:
            file.write("")
        with open(view_file_name, "a+") as file:
            # Process each view content part with variable replacements before writing
            views_content = [
                list_objects_view_py,
                list_deleted_objects_view_py,
                create_object_view_py,
                edit_object_view_py,
                delete_object_view_py,
                permanent_deletion_object_view_py,
                restore_object_view_py,
                view_object_view_py,
                dashboard_view_py,
                settings_view_py
            ]
            for content in views_content:
                processed_content = process_file_str(content, var_value_dict)
                file.write(processed_content)
                file.write("\n")  # Optionally add a newline for better readability
    else:
        # Iterate over each html_var and corresponding html_file
        for html_file, html_var in zip(current_files_list, current_var_list):
            print(f">>> === Processing File: {html_file} === <<<")

            # Process the html_var with multiple replacements
            processed_html = process_file_str(html_var, var_value_dict)
            
            html_dir = f"{outcome}/html/{module_name}"
            os.makedirs(html_dir) if not os.path.exists(html_dir) else None
            # Print the processed HTML for debugging
            print(f">>> === Processed Content for {html_file}: === <<<\n{processed_html}")
            html_file = f"{html_dir}/{html_file}" if html_file.endswith(".html") else f"{outcome}/python/{html_file}"
            # Write the processed content to the corresponding HTML file
            with open(html_file, "w") as file:
                file.write(processed_html)

# Special handling for urls module
# dest_dir = f"../../app_automate/templates/app_automate/{module_path_prefix}/{module_name}"
# copy_files(html_dir, dest_dir, html_files_list)


# Special handling for urls module
project_dir = f"../../dev_env/project_area/env_{project_name}/{project_name}"
app_dirname = f"{app_name}"
dest_dir = f"{project_dir}/{app_dirname}/templates/{app_dirname}/mod_{module_name}"
copy_files(html_dir, dest_dir, html_files_list)

# copy the python files
src_python_files = f"{outcome}/python"
des_python_dir = f"{project_dir}/{app_dirname}/mod_{module_name}"
copy_directory_contents(src_python_files, des_python_dir)