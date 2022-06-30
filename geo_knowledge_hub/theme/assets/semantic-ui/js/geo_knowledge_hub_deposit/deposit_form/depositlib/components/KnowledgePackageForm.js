/*
 * This file is part of GEO Knowledge Hub.
 * Copyright (C) 2021-2022 GEO Secretariat.
 *
 * GEO Knowledge Hub is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React from "react";
import {connect} from "react-redux";

import _isEmpty from "lodash/isEmpty";

import {BaseDepositForm} from "./BaseDepositForm";
import {FullDepositForm} from "./FullDepositForm";

import {KNOWLEDGE_PACKAGE_ID} from "../resources/types";

import {geoGlobalContext} from "../../configStore";
import {ACTION_SAVE_KNOWLEDGE_PACKAGE} from "../state/types";

import {KnowledgePackageDepositController} from "../controllers";

export class KnowledgePackageFormComponent extends BaseDepositForm {
  constructor(props) {
    super(props);
  }

  render() {
    // defining if the next is activated
    const {isRecordPublished} = this.props;

    // defining the knowledge package on the redux store
    const {knowledgePackage, saveKnowledgePackage} = this.props;
    if (isRecordPublished && _isEmpty(knowledgePackage)) {
      saveKnowledgePackage(this.depositConfigHandler.props.record);
    }

    return (
      <FullDepositForm
        resourceType={KNOWLEDGE_PACKAGE_ID}
        isRecordPublished={isRecordPublished}
        sidebarMenuRef={this.props.sidebarMenuRef}
        controller={KnowledgePackageDepositController}
        depositConfigHandler={this.depositConfigHandler}
        libraryVocabulariesHandler={this.libraryVocabulariesHandler}
      ></FullDepositForm>
    );
  }
}

// redux store config
const mapStateToProps = (state) => ({
  knowledgePackage: state.knowledgePackage,
});

const mapDispatchToProps = (dispatch) => ({
  saveKnowledgePackage: (knowledgePackage) =>
    dispatch({
      type: ACTION_SAVE_KNOWLEDGE_PACKAGE,
      payload: {
        knowledgePackage: knowledgePackage,
      },
    }),
});

export const KnowledgePackageForm = connect(
  mapStateToProps,
  mapDispatchToProps,
  null,
  {context: geoGlobalContext}
)(KnowledgePackageFormComponent);
