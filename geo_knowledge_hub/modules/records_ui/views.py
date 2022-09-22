# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 GEO Secretariat.
#
# geo-knowledge-hub is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""GEO Knowledge Hub Deposit (page) views."""

from flask import render_template
from flask_login import login_required
from geo_config.security.permissions import need_permission
from invenio_app_rdm.records_ui.views.decorators import pass_draft_community
from invenio_app_rdm.records_ui.views.deposits import get_search_url, new_record

from geo_knowledge_hub.modules.base.serializers.ui import UIJSONSerializer

from .toolbox.config import get_form_config
from .toolbox.decorators import pass_draft, pass_draft_files

#
# Creation routes
#


@login_required
@need_permission("geo-provider-access")
@pass_draft_community
def geo_package_deposit_create(community=None):
    """Deposit page to create packages."""
    return render_template(
        "invenio_app_rdm/records/deposit.html",
        forms_config=get_form_config(createUrl=("/api/packages")),
        searchbar_config=dict(searchUrl=get_search_url()),
        record=new_record(),
        files=dict(default_preview=None, entries=[], links={}),
        preselectedCommunity=community,
    )


@login_required
@need_permission("geo-provider-access")
@pass_draft_community
def geo_record_deposit_create(community=None):
    """Deposit page to create resources."""
    return render_template(
        "invenio_app_rdm/records/deposit.html",
        forms_config=get_form_config(createUrl=("/api/records")),
        searchbar_config=dict(searchUrl=get_search_url()),
        record=new_record(),
        files=dict(default_preview=None, entries=[], links={}),
        preselectedCommunity=community,
    )


#
# Edition routes
#


@login_required
@need_permission("geo-provider-access")
@pass_draft(record_type="package")
@pass_draft_files(record_type="package")
def geo_package_deposit_edit(draft=None, draft_files=None, pid_value=None):
    """Edit an existing package deposit."""
    record = UIJSONSerializer().dump_obj(draft.to_dict())

    return render_template(
        "invenio_app_rdm/records/deposit.html",
        forms_config=get_form_config(apiUrl=f"/api/packages/{pid_value}/draft"),
        record=record,
        files=draft_files.to_dict(),
        searchbar_config=dict(searchUrl=get_search_url()),
        permissions=draft.has_permissions_to(["new_version"]),
    )


@login_required
@need_permission("geo-provider-access")
@pass_draft(record_type="resource")
@pass_draft_files(record_type="resource")
def geo_record_deposit_edit(draft=None, draft_files=None, pid_value=None):
    """Edit an existing record resource deposit."""
    record = UIJSONSerializer().dump_obj(draft.to_dict())

    return render_template(
        "invenio_app_rdm/records/deposit.html",
        forms_config=get_form_config(apiUrl=f"/api/records/{pid_value}/draft"),
        record=record,
        files=draft_files.to_dict(),
        searchbar_config=dict(searchUrl=get_search_url()),
        permissions=draft.has_permissions_to(["new_version"]),
    )