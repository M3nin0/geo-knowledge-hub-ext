# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 GEO Secretariat.
#
# geo-knowledge-hub is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from flask import Blueprint

from . import views


def init_bp(app):
    bp = Blueprint("geo_deposit_bp", __name__, template_folder="theme/templates")

    # registration
    bp.add_url_rule("/uploads", "geo_deposit_search", views.geo_deposit_search)
    bp.add_url_rule("/uploads/new", "geo_deposit_create", views.geo_deposit_create)
    bp.add_url_rule("/uploads/<pid_value>", "geo_deposit_edit", views.geo_deposit_edit)
    bp.add_url_rule("/records/<pid_value>", "geo_record_detail", views.geo_record_detail)

    return bp


__all__ = (
    "init_bp"
)
