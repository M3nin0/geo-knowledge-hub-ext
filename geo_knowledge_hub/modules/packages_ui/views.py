# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 GEO Secretariat.
#
# geo-knowledge-hub is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""GEO Knowledge Hub Deposit (page) views."""

from flask import g, render_template
from flask_login import login_required
from geo_config.security.permissions import need_permission
from invenio_app_rdm.records_ui.views.decorators import (
    pass_draft_community,
    pass_is_preview,
)
from invenio_app_rdm.records_ui.views.deposits import get_search_url, new_record

from geo_knowledge_hub.modules.base.config import get_form_config
from geo_knowledge_hub.modules.base.decorators import (
    pass_draft,
    pass_draft_files,
    pass_file_item,
    pass_file_metadata,
    pass_record_files,
    pass_record_or_draft,
)
from geo_knowledge_hub.modules.base.serializers.ui import UIJSONSerializer

from ..base import records as record_utilities
from .toolbox import relationship as relationship_utilities


#
# Record Landing page views
#
@pass_is_preview
@pass_record_or_draft(record_type="package", expand=True)
@pass_record_files(record_type="package")
def geo_package_detail(record=None, files=None, pid_value=None, is_preview=False):
    """Record detail page (aka landing page)."""
    # Base definitions
    identity = g.identity

    files_data = None if files is None else files.to_dict()

    record_data = record.to_dict()
    record_ui = UIJSONSerializer().dump_obj(record_data)

    # General record properties
    record_is_draft = record_ui.get("is_draft")

    # Extract package resources metadata
    user_stories = []
    related_records_metadata = []

    related_records_metadata = relationship_utilities.get_related_records_metadata(
        identity, record
    )

    if related_records_metadata:
        # If records are associated with the package, we prepare
        # the metadata to be used on the front end and extract which
        # record is a user story.

        # Dump the loaded record
        related_records_metadata = record_utilities.serializer_dump_records(
            related_records_metadata
        )

        # Extract user stories
        related_records_metadata, user_stories = record_utilities.extract_user_stories(
            related_records_metadata
        )

    # Extract extra tags (e.g., GEO Work Programme Activity, Target users) from record
    (
        engagement_priorities,
        programme_activity,
        record_tags,
    ) = record_utilities.extract_extra_record_tags(identity, record_ui)

    return render_template(
        "geo_knowledge_hub/details/detail.html",
        # Invenio App RDM template variables
        record=record_ui,
        files=files_data,
        permissions=record.has_permissions_to(
            ["edit", "new_version", "manage", "update_draft", "read_files", "review"]
        ),
        is_draft=record_is_draft,
        is_preview=is_preview,
        # GEO Knowledge Hub template variables
        is_knowledge_package=True,
        user_stories=user_stories,
        record_topics=record_tags,
        programme_activity=programme_activity,
        related_records_information=related_records_metadata,
        related_engagement_priorities=engagement_priorities,
    )


#
# Deposit views
#
@login_required
@need_permission("geo-provider-access")
@pass_draft_community
def geo_package_deposit_create(community=None):
    """Deposit page to create packages."""
    return render_template(
        "geo_knowledge_hub/packages/deposit/index.html",
        forms_package_config=get_form_config(createUrl="/api/packages"),
        forms_record_config=get_form_config(createUrl="/api/records"),
        searchbar_config=dict(searchUrl=get_search_url()),
        record=new_record(),
        record_template=new_record(),
        files=dict(default_preview=None, entries=[], links={}),
        preselectedCommunity=community,
        # `Package resources' endpoint` is used to search resources inside the package.
        # For the "creation" interface, this is generated automatically after the package
        # creation.
        forms_package_records_endpoint=None,
    )


@login_required
@need_permission("geo-provider-access")
@pass_draft(record_type="package", expand=True)
@pass_draft_files(record_type="package")
def geo_package_deposit_edit(draft=None, draft_files=None, pid_value=None):
    """Edit an existing package deposit."""
    record = UIJSONSerializer().dump_obj(draft.to_dict())

    return render_template(
        "geo_knowledge_hub/packages/deposit/index.html",
        forms_package_config=get_form_config(
            apiUrl=f"/api/packages/{pid_value}/draft", createUrl=f"/api/packages"
        ),
        forms_record_config=get_form_config(createUrl="/api/records"),
        record=record,
        record_template=new_record(),
        files=draft_files.to_dict(),
        permissions=draft.has_permissions_to(["new_version"]),
        # `Package resources' endpoint` is used to search resources inside the package.
        forms_package_records_endpoint=f"/api/packages/{pid_value}/draft/resources",
    )


#
# Export views
#
@pass_is_preview
@pass_record_or_draft("package", expand=False)
def record_export(
    pid_value, record, export_format=None, permissions=None, is_preview=False
):
    """Export page view."""
    return record_utilities.record_export(pid_value, record, export_format)


#
# File views
#
@pass_is_preview
@pass_record_or_draft("package")
@pass_file_metadata("package")
def record_file_preview(
    pid_value,
    record=None,
    pid_type="recid",
    file_metadata=None,
    is_preview=False,
    **kwargs,
):
    """Render a preview of the specified file."""
    base_url = "geokhub_packages_ui_bp.record_file_download"

    return record_utilities.record_file_preview(
        base_url, pid_value, record, pid_type, file_metadata, is_preview, **kwargs
    )


@pass_is_preview
@pass_file_item("package")
def record_file_download(pid_value, file_item=None, is_preview=False, **kwargs):
    """Download a file from a record."""
    return record_utilities.record_file_download(
        pid_value, file_item, is_preview, **kwargs
    )
