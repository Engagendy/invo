const state = {
  jobId: null,
  pollTimer: null,
  options: null,
  authToken: localStorage.getItem("ultra_force_token") || "",
  currentUser: null,
  projects: [],
  selectedProjectId: null,
  currentView: "home",
  projectTab: "overview",
  documents: [],
  documentsTableRows: [],
  documentsTablePagination: { page: 1, page_size: 15, total: 0, total_pages: 1 },
  historyTableRows: [],
  historyTablePagination: { page: 1, page_size: 10, total: 0, total_pages: 1 },
  resourcesRows: [],
  resourcesPagination: { page: 1, page_size: 12, total: 0, total_pages: 1 },
  resourceKindOptions: [],
  globalSearchQuery: "",
  globalSearchKindFilter: "",
  globalSearchStatusFilter: "",
  globalSearchConfidenceFilter: "",
  globalSearchPage: 1,
  globalSearchRows: [],
  globalSearchPagination: { page: 1, page_size: 12, total: 0, total_pages: 1 },
  globalSearchSelectedId: 0,
  globalSearchKindOptions: [],
  savedSearches: [],
  evidenceSearch: "",
  evidenceAttachmentFilter: "",
  evidencePage: 1,
  evidenceSelectedId: 0,
  evidenceSelectedIds: new Set(),
  evidenceAttachments: [],
  evidenceAttachmentCounts: {},
  pendingEvidenceAttachmentPath: "",
  evidenceSelectedAttachmentId: 0,
  evidencePreviewPath: "",
  evidencePreviewLabel: "",
  reviewComments: [],
  activityEvents: [],
  projectMembers: [],
  companies: [],
  companySettings: null,
  companyAccountingRules: [],
  companiesDirectorySearch: "",
  companiesDirectorySort: "name_asc",
  companiesDirectoryPage: 1,
  companyRulesSearch: "",
  companyRulesSourceFilter: "",
  companyRulesSort: "keyword_asc",
  companyRulesPage: 1,
  companiesPane: "overview",
  companyPaneLoaded: {},
  companyRenderSuspendCount: 0,
  companyRenderPending: false,
  companyProjectsSearch: "",
  companyProjectsStatusFilter: "",
  supplierParties: [],
  customerParties: [],
  suppliersSearch: "",
  suppliersSort: "name_asc",
  suppliersPage: 1,
  customersSearch: "",
  customersSort: "name_asc",
  customersPage: 1,
  projectCodeDimensions: [],
  costCenterDimensions: [],
  costCodeDimensions: [],
  apSummary: null,
  arSummary: null,
  apDocsSearch: "",
  arDocsSearch: "",
  apDocsRows: [],
  arDocsRows: [],
  apDocsPagination: { page: 1, page_size: 10, total: 0, total_pages: 1 },
  arDocsPagination: { page: 1, page_size: 10, total: 0, total_pages: 1 },
  companyAllocationType: "payable",
  companyAllocationWorkspace: null,
  jobCostingSummary: null,
  companyBillingEvents: [],
  companyPurchaseOrders: [],
  procurementSummary: null,
  procurementExceptions: null,
  procurementExceptionReviewFilter: "",
  procurementExceptionMineOnly: false,
  companyReceipts: [],
  companyActivityEvents: [],
  closeSummary: null,
  accountingAccounts: [],
  accountingPeriods: [],
  accountingPeriodsPage: 1,
  accountingPeriodsSearch: "",
  accountingPeriodsStatusFilter: "",
  accountingPeriodsSort: "start_desc",
  journalDrafts: [],
  journalDraftSummary: { draft_count: 0, posted_amount: 0 },
  journalDraftsPage: 1,
  journalDraftsSearch: "",
  journalDraftsStatusFilter: "",
  journalDraftsSort: "date_desc",
  journalEntries: [],
  journalEntriesPage: 1,
  journalEntriesSearch: "",
  journalEntriesStatusFilter: "",
  journalEntriesSort: "date_desc",
  trialBalanceRows: [],
  ledgerAccountCode: "",
  ledgerProjectFilter: "",
  ledgerCostCenterFilter: "",
  ledgerRows: [],
  ledgerSummary: { count: 0, ending_balance: 0 },
  ledgerPage: 1,
  ledgerSearch: "",
  ledgerSort: "date_desc",
  accountingExportPreset: "ultra_force",
  accountingExportPresets: [],
  selectedHistoryIds: new Set(),
  editingDocumentId: null,
  historySearch: "",
  historyTypeFilter: "",
  historyCompanyFilter: "",
  historyConfidenceFilter: "",
  documentsSearch: "",
  documentsKindFilter: "",
  documentsTypeFilter: "",
  documentsConfidenceFilter: "",
  documentsMatchFilter: "",
  resourcesSearch: "",
  resourcesKindFilter: "",
  resourcesPage: 1,
  selectedResourceKey: "",
  resourceDetailPage: 1,
  resourceDetail: null,
  resourceDetailRows: [],
  resourceDetailPagination: { page: 1, page_size: 12, total: 0, total_pages: 1 },
  resourceDiagnostics: null,
  resourceActivity: [],
  reconciliationSearch: "",
  reconciliationStatusFilter: "attention",
  reconciliationBankFilter: "",
  reconciliationSort: "priority",
  reconciliationPage: 1,
  reconciliationSelectedId: 0,
  reconciliationSessionDecisions: {},
  reconciliationRows: [],
  reconciliationPagination: { page: 1, page_size: 12, total: 0, total_pages: 1 },
  reconciliationSummary: { needs_review_count: 0, missing_amount: 0, reviewed_count: 0 },
  reconciliationBankOptions: [],
  reviewQueueSearch: "",
  reviewQueueTypeFilter: "",
  reviewQueueSourceFilter: "",
  reviewQueuePage: 1,
  reviewQueueSelectedKey: "",
  reviewQueueRows: [],
  reviewQueuePagination: { page: 1, page_size: 12, total: 0, total_pages: 1 },
  reviewQueueSummary: { total: 0, low_confidence: 0, duplicates: 0, parsing: 0 },
  reviewQueueSourceOptions: [],
  exceptionsSearch: "",
  exceptionsTypeFilter: "",
  exceptionsPage: 1,
  exceptionsRows: [],
  exceptionsPagination: { page: 1, page_size: 12, total: 0, total_pages: 1 },
  exceptionsSummary: { total: 0, installments: 0, refund_pairs: 0, split_groups: 0, duplicates: 0, mismatches: 0 },
  exceptionsSelectedKey: "",
  feedbackInsights: null,
  vendorSearch: "",
  vendorsPage: 1,
  selectedVendorKey: "",
  vendorAliases: {},
  projectRules: [],
  tagsSearch: "",
  tagsSourceFilter: "",
  selectedTagRecordId: 0,
  recordTags: {},
  dashboardSearch: "",
  dashboardDateFrom: "",
  dashboardDateTo: "",
  dashboardDirectionFilter: "",
  dashboardMatchFilter: "",
  dashboardBankFilter: "",
  dashboardAnalytics: null,
  dashboardBankOptions: [],
  dashboardDrilldownTitle: "Drill Down",
  dashboardDrilldownSubtitle: "Click any dashboard item to inspect the underlying bank rows.",
  dashboardDrilldownRows: [],
  dashboardDrilldownMode: "all",
  dashboardDrilldownValue: "",
  dashboardDrilldownPagination: { page: 1, page_size: 25, total: 0, total_pages: 1 },
  dashboardDrilldownSearch: "",
  dashboardDrilldownDirection: "",
  dashboardDrilldownMatch: "",
  documentsPage: 1,
  dashboardDrilldownPage: 1,
  historyPage: 1,
  models: [],
  modelRefreshTimer: null,
  loadedProjectTabs: {},
  debounceTimers: {},
};

const HISTORY_PAGE_SIZE = 10;
const DOCUMENTS_PAGE_SIZE = 15;
const RESOURCES_PAGE_SIZE = 12;
const RESOURCE_DETAIL_PAGE_SIZE = 12;
const RECONCILIATION_PAGE_SIZE = 12;
const REVIEW_QUEUE_PAGE_SIZE = 12;
const VENDORS_PAGE_SIZE = 12;
const DASHBOARD_DRILLDOWN_PAGE_SIZE = 25;
const GLOBAL_SEARCH_PAGE_SIZE = 12;
let linkedPreviewDocument = null;

const el = (id) => document.getElementById(id);

function authHeaders() {
  return state.authToken ? { "X-Auth-Token": state.authToken } : {};
}

function setStatus(value) {
  el("jobStatus").textContent = value;
}

function debounce(key, delay, callback) {
  if (state.debounceTimers[key]) {
    clearTimeout(state.debounceTimers[key]);
  }
  state.debounceTimers[key] = setTimeout(() => {
    delete state.debounceTimers[key];
    callback();
  }, delay);
}

function showSweetAlert(title, text, kind = "info") {
  const backdrop = el("sweetAlert");
  const icon = el("sweetAlertIcon");
  const cancel = el("sweetAlertCancel");
  const confirm = el("sweetAlertConfirm");
  el("sweetAlertTitle").textContent = title;
  el("sweetAlertText").textContent = text;
  cancel.classList.add("hidden");
  cancel.onclick = null;
  confirm.textContent = "OK";
  confirm.onclick = hideSweetAlert;
  icon.textContent = kind === "error" ? "!" : kind === "success" ? "✓" : "i";
  icon.style.background =
    kind === "error"
      ? "linear-gradient(135deg, #c24a34, #8d2817)"
      : kind === "success"
        ? "linear-gradient(135deg, #34835a, #22553a)"
        : "linear-gradient(135deg, #a54e2d, #7f2e14)";
  backdrop.classList.remove("hidden");
}

function accountByCode(code) {
  const value = String(code || "").trim();
  if (!value) return null;
  return (state.accountingAccounts || []).find((item) => String(item.code || "").trim() === value) || null;
}

function accountLabel(code, fallback = "-") {
  const value = String(code || "").trim();
  if (!value) return fallback;
  const account = accountByCode(value);
  return account?.name ? `${value} · ${account.name}` : value;
}

function accountFlowLabel(primaryCode, offsetCode) {
  const primary = accountLabel(primaryCode, "-");
  const offset = String(offsetCode || "").trim();
  return offset ? `${primary} -> ${accountLabel(offset, offset)}` : primary;
}

function hideSweetAlert() {
  el("sweetAlert").classList.add("hidden");
}

function showLoading(title, text) {
  el("loadingTitle").textContent = title;
  el("loadingText").textContent = text;
  el("loadingOverlay").classList.remove("hidden");
}

function hideLoading() {
  el("loadingOverlay").classList.add("hidden");
}

function showRunProgress(title, text) {
  el("runProgressTitle").textContent = title;
  el("runProgressText").textContent = text;
  el("runProgressPanel").classList.remove("hidden");
}

function hideRunProgress() {
  el("runProgressPanel").classList.add("hidden");
}

function openEditResultModal(document) {
  state.editingDocumentId = document.id;
  el("editDocType").value = document.doc_type || "";
  el("editDocDate").value = /^\d{4}-\d{2}-\d{2}$/.test(document.date || "") ? document.date : "";
  el("editDocNumber").value = document.number || "";
  el("editDocCompany").value = document.company_name || "";
  el("editDocAmount").value = document.amount || "";
  el("editDocCurrency").value = document.currency || "";
  setEditPreviewMode("output", document);
  el("editResultModal").classList.remove("hidden");
}

function closeEditResultModal() {
  state.editingDocumentId = null;
  el("editResultModal").classList.add("hidden");
}

function filePreviewHref(path) {
  return path
    ? `/api/file?path=${encodeURIComponent(path)}&token=${encodeURIComponent(state.authToken)}`
    : "";
}

function vendorAliasStorageKey() {
  return `ultra_force_vendor_aliases_${state.selectedProjectId || "none"}`;
}

function loadVendorAliases() {
  state.vendorAliases = {};
}

function saveVendorAliases() {
  return null;
}

function projectRulesStorageKey() {
  return `ultra_force_project_rules_${state.selectedProjectId || "none"}`;
}

function recordTagsStorageKey() {
  return `ultra_force_record_tags_${state.selectedProjectId || "none"}`;
}

function loadProjectRules() {
  state.projectRules = [];
}

function saveProjectRules() {
  return null;
}

function loadRecordTags() {
  state.recordTags = {};
}

function saveRecordTags() {
  return null;
}

function resolveLinkedDocument(record) {
  return state.documents.find((item) =>
    item.id !== record?.id
    && (item.source_type || "") === (record?.matched_record_source_type || "")
    && (item.company_name || "") === (record?.matched_record_company_name || "")
    && (item.number || "") === (record?.matched_record_number || "")
    && (item.amount || "") === (record?.matched_record_amount || "")
    && (
      (item.source_timestamp || "") === (record?.matched_record_source_timestamp || "")
      || (item.date || "") === (record?.matched_record_date || "")
      || (item.source_file || "") === (record?.matched_record_source_file || "")
      || (item.output_file || "") === (record?.matched_record_output_file || "")
    )
  ) || null;
}

function findRecordById(recordId) {
  const numericId = Number(recordId);
  const collections = [
    state.documents || [],
    state.dashboardDetailRows || [],
    state.reconciliationRows || [],
    state.globalSearchRows || [],
    state.resourceDetailRows || [],
    state.reviewQueueRows || [],
  ];
  for (const collection of collections) {
    const found = collection.find((item) => Number(item.id) === numericId);
    if (found) return found;
  }
  return null;
}

function confidenceBreakdownText(record) {
  const fields = record?.confidence_breakdown?.fields || {};
  const overall = record?.confidence_breakdown?.overall;
  const label = record?.confidence_breakdown?.label;
  const fieldText = Object.keys(fields).length
    ? `date ${fields.date ?? "-"}, vendor ${fields.vendor ?? "-"}, amount ${fields.amount ?? "-"}, reference ${fields.reference ?? "-"}, ocr ${fields.ocr ?? "-"}`
    : "";
  if (fieldText && Number.isFinite(Number(overall))) {
    return `Overall ${overall} (${label || "-"}) | ${fieldText}`;
  }
  if (fieldText) return fieldText;
  if (Number.isFinite(Number(overall))) return `Overall ${overall} (${label || "-"})`;
  return "No confidence breakdown available.";
}

function provenanceText(record) {
  const provenance = record?.provenance || {};
  const parts = [
    provenance.source_type || record?.source_type || "-",
    provenance.source_origin || record?.source_origin || "-",
    provenance.source_file || record?.source_file || "-",
    provenance.sheet_name || provenance.source_timestamp || record?.source_timestamp || record?.date || "-",
  ];
  if (provenance.processed_at) {
    parts.push(`processed ${formatDateTime(provenance.processed_at)}`);
  }
  if (provenance.review_updated_at) {
    parts.push(`reviewed ${formatDateTime(provenance.review_updated_at)}`);
  }
  return parts.join(" • ");
}

function warningsAndConfidenceText(record) {
  const warnings = parserWarningsForRecord(record);
  const warningText = warnings.length ? warnings.join(" • ") : "No parser warnings.";
  return `${warningText} | ${confidenceBreakdownText(record)}`;
}

function attachmentTypeLabel(value) {
  const labels = {
    receipt: "Receipt",
    invoice: "Invoice",
    screenshot: "Screenshot",
    bank_statement: "Bank Statement",
    delivery_note: "Delivery Note",
    contract: "Contract",
    supporting_document: "Supporting Document",
    other: "Other",
  };
  return labels[value] || value || "Attachment";
}

function attachmentToneClass(value) {
  const tones = {
    receipt: "bg-[rgba(57,112,92,0.12)] text-[#275b4a]",
    invoice: "bg-[rgba(42,99,167,0.12)] text-[#1f4b7d]",
    screenshot: "bg-[rgba(165,78,45,0.1)] text-emberdark",
    bank_statement: "bg-[rgba(99,102,241,0.12)] text-[#4147a8]",
    delivery_note: "bg-[rgba(217,119,6,0.12)] text-[#9a5b00]",
    contract: "bg-[rgba(107,114,128,0.14)] text-[#5c6470]",
    supporting_document: "bg-[rgba(122,89,55,0.1)] text-[#6b472d]",
    other: "bg-[rgba(107,114,128,0.14)] text-[#5c6470]",
  };
  return tones[value] || tones.supporting_document;
}

function setEvidencePreview(path, label = "") {
  const href = filePreviewHref(path);
  state.evidencePreviewPath = path || "";
  state.evidencePreviewLabel = label || path || "No file selected.";
  el("evidencePreviewLabel").textContent = state.evidencePreviewLabel;
  el("evidencePreviewLabel").title = state.evidencePreviewLabel;
  el("evidencePreviewOpenLink").href = href || "#";
  el("evidencePreviewOpenLink").style.pointerEvents = href ? "auto" : "none";
  el("evidencePreviewOpenLink").style.opacity = href ? "1" : "0.45";
  el("evidencePreviewFrame").src = href || "about:blank";
}

function linkedRecordSnapshot(record) {
  return {
    source_type: record?.matched_record_source_type || "",
    source_origin: record?.matched_record_source_type || "",
    source_file: record?.matched_record_source_file || "",
    source_timestamp: record?.matched_record_source_timestamp || "",
    date: record?.matched_record_date || "",
    number: record?.matched_record_number || "",
    company_name: record?.matched_record_company_name || "",
    amount: record?.matched_record_amount || "",
    transaction_direction: record?.matched_record_transaction_direction || "",
    match_basis: record?.match_basis || "",
    explainability: {
      status: record?.match_status === "matched" ? "linked_to_bank" : record?.match_status || "linked_to_bank",
      match_reasons: (record?.match_basis || "").split(/[|;]/).map((item) => item.trim()).filter(Boolean),
      match_factors: [],
      review_note: "",
    },
    parser_warnings: [],
    confidence_breakdown: {},
    provenance: {
      source_type: record?.matched_record_source_type || "",
      source_origin: record?.matched_record_source_type || "",
      source_file: record?.matched_record_source_file || "",
      source_timestamp: record?.matched_record_source_timestamp || record?.matched_record_date || "",
      sheet_name: record?.matched_record_source_type === "sheet" ? (record?.matched_record_source_timestamp || "") : "",
    },
  };
}

function setLinkedPreviewMode(mode) {
  const path = linkedPreviewDocument?.output_path || "";
  const href = filePreviewHref(path);
  el("linkedPreviewOpenLink").href = href || "#";
  el("linkedPreviewOpenLink").style.pointerEvents = href ? "auto" : "none";
  el("linkedPreviewOpenLink").style.opacity = href ? "1" : "0.45";
  el("linkedPreviewFileLabel").textContent = path || "No linked file available for preview.";
  el("linkedPreviewFileLabel").parentElement.title = path || "";
  el("linkedPreviewFrame").src = href || "about:blank";
}

function openLinkedRecordModal(record) {
  linkedPreviewDocument = resolveLinkedDocument(record);
  const linkedRecord = linkedPreviewDocument || linkedRecordSnapshot(record);
  el("linkedRecordType").textContent = linkedRecord?.source_type || record?.matched_record_source_type || "-";
  el("linkedRecordSource").textContent = linkedRecord?.source_timestamp || record?.matched_record_source_timestamp || linkedRecord?.source_file || record?.matched_record_source_file || linkedRecord?.date || record?.matched_record_date || "-";
  el("linkedRecordCompany").textContent = canonicalVendorName(linkedRecord?.company_name || record?.matched_record_company_name) || "-";
  el("linkedRecordNumber").textContent = linkedRecord?.number || record?.matched_record_number || "-";
  el("linkedRecordAmount").textContent = linkedRecord?.amount || record?.matched_record_amount || "-";
  el("linkedRecordDirection").textContent = linkedRecord?.transaction_direction || record?.matched_record_transaction_direction || "-";
  el("linkedRecordBasis").textContent = linkedRecord?.match_basis || record?.match_basis || "-";
  el("linkedRecordExplainability").textContent = explainRecord(linkedRecord || record);
  el("linkedRecordWarnings").textContent = warningsAndConfidenceText(linkedRecord || record);
  el("linkedRecordTrace").textContent = provenanceText(linkedRecord || record);
  setLinkedPreviewMode("output");
  el("linkedRecordModal").classList.remove("hidden");
}

function closeLinkedRecordModal() {
  linkedPreviewDocument = null;
  el("linkedPreviewFrame").src = "about:blank";
  el("linkedRecordModal").classList.add("hidden");
}

function setEditPreviewMode(mode, docRecord = null) {
  const currentDocument =
    docRecord || state.documents.find((item) => item.id === state.editingDocumentId) || null;
  const modeToPath = {
    output: currentDocument?.output_path || "",
    enhanced: currentDocument?.enhanced_output_path || "",
  };
  const safeMode = mode === "enhanced" ? "enhanced" : "output";
  const path = modeToPath[safeMode] || modeToPath.output || modeToPath.enhanced || "";
  const href = filePreviewHref(path);

  window.document.querySelectorAll(".preview-mode-button").forEach((button) => {
    button.classList.toggle("active", button.id === `preview${safeMode.charAt(0).toUpperCase()}${safeMode.slice(1)}Button`);
  });
  el("previewOpenLink").href = href || "#";
  el("previewOpenLink").style.pointerEvents = href ? "auto" : "none";
  el("previewOpenLink").style.opacity = href ? "1" : "0.45";
  el("previewFileLabel").textContent = path || "No generated file available for this preview.";
  el("previewFileLabel").parentElement.title = path || "";
  el("editPreviewFrame").src = href || "about:blank";
}

function confirmSweetAlert(title, text, confirmLabel = "Delete") {
  return new Promise((resolve) => {
    const backdrop = el("sweetAlert");
    const icon = el("sweetAlertIcon");
    const cancel = el("sweetAlertCancel");
    const confirm = el("sweetAlertConfirm");

    el("sweetAlertTitle").textContent = title;
    el("sweetAlertText").textContent = text;
    icon.textContent = "!";
    icon.style.background = "linear-gradient(135deg, #c24a34, #8d2817)";
    cancel.classList.remove("hidden");
    confirm.textContent = confirmLabel;

    const cleanup = () => {
      cancel.onclick = null;
      confirm.onclick = null;
      hideSweetAlert();
    };

    cancel.onclick = () => {
      cleanup();
      resolve(false);
    };
    confirm.onclick = () => {
      cleanup();
      resolve(true);
    };
    backdrop.classList.remove("hidden");
  });
}

function fields() {
  const fallbackProjectLabel = el("projectRecordName")?.value.trim() || "ULTRA FORCE";
  return {
    source_dir: el("sourceDir").value.trim(),
    output_dir: el("outputDir").value.trim(),
    debug_image_dir: el("debugImageDir").value.trim(),
    archive_source_dir: el("archiveSourceDir").value.trim(),
    project_name: el("projectName").value.trim() || fallbackProjectLabel,
    ocr_backend: el("ocrBackend").value,
    handwriting_backend: el("handwritingBackend").value,
    trocr_model: el("trocrModel").value,
    ocr_profile: el("ocrProfile").value,
    export_image_mode: el("exportImageMode").value,
    naming_pattern: el("namingPattern").value.trim(),
    lang: el("lang").value.trim(),
    dpi: Number(el("dpi").value),
    single_item_per_page: el("singleItemPerPage").checked,
    save_text: el("saveText").checked,
    use_angle_cls: el("useAngleCls").checked,
    move_processed_source: el("moveProcessedSource").checked,
    video_sample_seconds: Number(el("videoSampleSeconds").value),
    video_max_frames: Number(el("videoMaxFrames").value),
    excel_name: el("excelName").value.trim(),
  };
}

function emptyProjectSettings() {
  return {
    source_dir: "",
    output_dir: "",
    debug_image_dir: "",
    archive_source_dir: "",
    project_name: "ULTRA FORCE",
    ocr_backend: "normal",
    handwriting_backend: "none",
    trocr_model: "microsoft/trocr-base-handwritten",
    ocr_profile: "mixed",
    export_image_mode: "original",
    naming_pattern: "{doc_type}_{date}_{number}_{company_name}_{amount_aed}_{project_name}",
    lang: "en",
    dpi: 300,
    single_item_per_page: true,
    save_text: true,
    use_angle_cls: true,
    move_processed_source: false,
    video_sample_seconds: 2,
    video_max_frames: 120,
    excel_name: "document_summary.xlsx",
  };
}

function getSelectedProject() {
  return state.projects.find((project) => project.id === state.selectedProjectId) || null;
}

function selectedProjectAccessRole() {
  return (getSelectedProject()?.access_role || "owner").toLowerCase();
}

function projectRoleRank(role) {
  if (role === "owner") return 40;
  if (role === "admin") return 30;
  if (role === "reviewer") return 20;
  return 10;
}

function canManageProjectSettings() {
  return projectRoleRank(selectedProjectAccessRole()) >= projectRoleRank("admin");
}

function canManageProjectMembers() {
  return projectRoleRank(selectedProjectAccessRole()) >= projectRoleRank("admin");
}

function canDeleteSelectedProject() {
  return selectedProjectAccessRole() === "owner";
}

function applySettings(settings) {
  const merged = { ...emptyProjectSettings(), ...settings };
  el("sourceDir").value = merged.source_dir || "";
  el("outputDir").value = merged.output_dir || "";
  el("debugImageDir").value = merged.debug_image_dir || "";
  el("archiveSourceDir").value = merged.archive_source_dir || "";
  el("projectName").value = merged.project_name || "ULTRA FORCE";
  el("ocrBackend").value = merged.ocr_backend;
  el("handwritingBackend").value = merged.handwriting_backend;
  el("trocrModel").value = merged.trocr_model;
  el("ocrProfile").value = merged.ocr_profile;
  el("exportImageMode").value = merged.export_image_mode;
  el("namingPattern").value = merged.naming_pattern;
  el("lang").value = merged.lang;
  el("dpi").value = merged.dpi;
  el("singleItemPerPage").checked = merged.single_item_per_page;
  el("saveText").checked = merged.save_text;
  el("useAngleCls").checked = merged.use_angle_cls;
  el("moveProcessedSource").checked = merged.move_processed_source;
  el("videoSampleSeconds").value = merged.video_sample_seconds;
  el("videoMaxFrames").value = merged.video_max_frames;
  el("excelName").value = merged.excel_name;
  updateNamingPreview();
}

function populateSelect(node, values) {
  node.innerHTML = "";
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    node.appendChild(option);
  });
}

function companyPaneCacheKey(pane = state.companiesPane) {
  const companyId = Number(state.currentUser?.company_id || state.companySettings?.id || 0);
  return `${companyId}:${pane || "overview"}`;
}

function invalidateCompanyPaneCache() {
  state.companyPaneLoaded = {};
}

function markCompanyPaneLoaded(pane = state.companiesPane) {
  state.companyPaneLoaded[companyPaneCacheKey(pane)] = true;
}

function isCompanyPaneLoaded(pane = state.companiesPane) {
  return Boolean(state.companyPaneLoaded[companyPaneCacheKey(pane)]);
}

function requestCompaniesRender() {
  if (state.companyRenderSuspendCount > 0) {
    state.companyRenderPending = true;
    return;
  }
  renderCompaniesWorkspace();
}

async function runCompanyRenderBatch(task) {
  state.companyRenderSuspendCount += 1;
  try {
    return await task();
  } finally {
    state.companyRenderSuspendCount = Math.max(0, state.companyRenderSuspendCount - 1);
    if (state.companyRenderSuspendCount === 0 && state.companyRenderPending) {
      state.companyRenderPending = false;
      renderCompaniesWorkspace();
    }
  }
}

async function loadCompanyBaseData() {
  await Promise.all([
    loadCompanies(),
    loadCompanySettings(),
    loadCompanyAccountingRules(),
    loadProjects(),
    loadCompanyDimensions(),
    loadCompanyParties(),
  ]);
}

async function ensureCompanyPaneData(pane = state.companiesPane, force = false) {
  if (!state.authToken) return;
  if (!force && isCompanyPaneLoaded(pane)) return;
  await runCompanyRenderBatch(async () => {
    if (pane === "finance") {
      await Promise.all([
        loadCompanyAging(),
        loadCompanyProcurementSummary(),
        loadCompanyProcurementExceptions(),
        loadCompanyReceipts(),
        loadCompanyApDocuments(),
        loadCompanyArDocuments(),
        loadCompanyAllocationWorkspace(),
      ]);
    } else if (pane === "costing") {
      await Promise.all([
        loadCompanyJobCostingSummary(),
        loadCompanyBillingEvents(),
        loadCompanyPurchaseOrders(),
        loadCompanyReceipts(),
      ]);
    } else if (pane === "activity") {
      await loadCompanyActivity();
    }
  });
  markCompanyPaneLoaded(pane);
}

function switchView(name) {
  state.currentView = name;
  const mapping = {
    home: "homeView",
    accounting: "accountingView",
    companies: "companiesView",
    system: "systemView",
    projectEditor: "projectEditorView",
    projectDetail: "projectDetailView",
  };
  Object.values(mapping).forEach((id) => el(id).classList.add("hidden"));
  el(mapping[name]).classList.remove("hidden");

  document.querySelectorAll(".nav-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.viewTarget === name);
  });
  if (name === "accounting") {
    renderCompaniesWorkspace();
    loadCompanySettings();
    loadCompanyDimensions();
    loadAccountingFoundation();
  } else if (name === "companies") {
    renderCompaniesWorkspace();
    runCompanyRenderBatch(async () => {
      await loadCompanyBaseData();
      await ensureCompanyPaneData(state.companiesPane, true);
    });
  }
}

function switchProjectTab(name) {
  state.projectTab = name;
  document.querySelectorAll(".project-tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.projectTab === name);
  });
  document.querySelectorAll(".project-tab-view").forEach((view) => {
    view.classList.add("hidden");
  });
  el(`projectTab${name.charAt(0).toUpperCase()}${name.slice(1)}`).classList.remove("hidden");
  loadProjectTabData(name);
}

function projectTabCacheKey(name) {
  return state.selectedProjectId ? `${state.selectedProjectId}:${name}` : "";
}

function resetLoadedProjectTabs() {
  state.loadedProjectTabs = {};
}

function invalidateProjectTabs(names = []) {
  if (!state.selectedProjectId) return;
  if (!names.length) {
    resetLoadedProjectTabs();
    return;
  }
  names.forEach((name) => {
    delete state.loadedProjectTabs[`${state.selectedProjectId}:${name}`];
  });
}

async function loadProjectTabData(name, force = false) {
  if (!state.selectedProjectId) return;
  const key = projectTabCacheKey(name);
  if (!force && key && state.loadedProjectTabs[key]) {
    return;
  }
  if (name === "overview") {
    await Promise.all([loadDashboardAnalytics(true), loadCloseSummary(), loadExceptions()]);
  } else if (name === "reconciliation") {
    await loadReconciliationQueue();
  } else if (name === "review") {
    await loadReviewQueue();
  } else if (name === "exceptions") {
    await loadExceptions();
  } else if (name === "feedback") {
    await loadFeedbackInsights();
  } else if (name === "vendors") {
    await loadVendorAliasesRemote();
  } else if (name === "rules") {
    await loadProjectRulesRemote();
  } else if (name === "search") {
    await Promise.all([loadGlobalSearch(), loadSavedSearches()]);
  } else if (name === "evidence") {
    await loadEvidenceAttachmentCounts();
  } else if (name === "activity") {
    await loadActivityFeed();
  } else if (name === "members") {
    await loadProjectMembers();
  } else if (name === "close") {
    await loadCloseSummary();
  } else if (name === "results") {
    await loadHistoryTable();
  } else if (name === "resources") {
    await loadResourcesTable();
  } else if (name === "documents") {
    await loadDocumentsTable();
  }
  if (key) {
    state.loadedProjectTabs[key] = true;
  }
}

function showAuthView() {
  el("authView").classList.remove("hidden");
  el("appView").classList.add("hidden");
}

function showAppView() {
  el("authView").classList.add("hidden");
  el("appView").classList.remove("hidden");
}

function updateNamingPreview() {
  const data = fields();
  const replacements = {
    "{doc_type}": "Invoice",
    "{date}": "2026-04-05",
    "{number}": "INV-1023",
    "{company_name}": "ACMETrading",
    "{amount}": "125.00",
    "{amount_aed}": "125.00AED",
    "{project_name}": data.project_name || "ULTRA FORCE",
  };
  let preview = data.naming_pattern || "";
  Object.entries(replacements).forEach(([token, value]) => {
    preview = preview.replaceAll(token, value);
  });
  el("namingPreview").textContent = preview.endsWith(".pdf") ? preview : `${preview}.pdf`;
}

function renderRuntime(runtime) {
  const aiDeps = Object.entries(runtime.ai_backend_dependencies)
    .map(([key, value]) => `${key}: ${value ? "ok" : "missing"}`)
    .join("\n");
  const trocrDeps = Object.entries(runtime.trocr_dependencies)
    .map(([key, value]) => `${key}: ${value ? "ok" : "missing"}`)
    .join("\n");
  const aiModels = Object.entries(runtime.ai_backend_models)
    .map(([key, value]) => `${key}: ${value ? "cached" : "missing"}`)
    .join("\n");
  el("runtimeStatus").textContent =
    `Python: ${runtime.python_version}\n` +
    `Normal backend: ${runtime.normal_backend_ready ? "ready" : "missing deps"}\n` +
    `AI backend: ${runtime.ai_backend_ready ? "ready" : "needs setup"}\n` +
    `AI supported python: ${runtime.ai_backend_supported_python}\n` +
    `App root: ${runtime.app_root}\n` +
    `Data root: ${runtime.data_root}\n` +
    `\nAI dependencies\n${aiDeps}\n` +
    `\nAI models\n${aiModels}\n` +
    `\nTrOCR\n${trocrDeps}` +
    (runtime.messages?.length ? `\n\nActions\n${runtime.messages.map((item) => `- ${item}`).join("\n")}` : "");
}

function renderModels() {
  const container = el("modelManager");
  container.innerHTML = "";
  state.models.forEach((model) => {
    const card = document.createElement("div");
    card.className = "rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] p-5";
    const installed = model.installed === "true";
    const removable = model.removable === "true";
    const downloading = model.status === "downloading";
    card.innerHTML = `
      <div class="flex items-start justify-between gap-3">
        <div>
          <div class="text-xs uppercase tracking-[0.14em] text-muted">${model.tier}</div>
          <h4 class="mt-2 text-lg font-semibold">${model.label}</h4>
          <p class="mt-2 text-sm leading-6 text-muted">${model.description}</p>
          <div class="mt-3 text-xs text-muted">Model: ${model.name}</div>
          <div class="mt-1 text-xs text-muted">Size profile: ${model.size_hint}</div>
          <div class="mt-3 text-sm font-semibold ${installed ? "text-[#275b4a]" : model.status === "error" ? "text-[#8d2817]" : "text-muted"}">
            ${model.status === "downloading" ? "Downloading..." : installed ? "Installed" : model.status === "error" ? "Error" : "Not installed"}
          </div>
          <div class="mt-1 text-xs text-muted">${model.message || ""}</div>
        </div>
      </div>
      <div class="mt-4 flex flex-wrap gap-2">
        <button data-model-download="${model.name}" class="rounded-full bg-gradient-to-br from-ember to-emberdark px-4 py-2 text-sm font-semibold text-white" ${downloading ? "disabled" : ""}>
          ${installed ? "Reinstall" : "Download"}
        </button>
        <button data-model-delete="${model.name}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-4 py-2 text-sm font-semibold text-emberdark" ${removable ? "" : "disabled"}>
          Remove
        </button>
      </div>
    `;
    container.appendChild(card);
  });

  container.querySelectorAll("[data-model-download]").forEach((button) => {
    button.addEventListener("click", () => downloadModel(button.dataset.modelDownload));
  });
  container.querySelectorAll("[data-model-delete]").forEach((button) => {
    button.addEventListener("click", () => deleteModel(button.dataset.modelDelete));
  });
}

function syncModelRefreshTimer() {
  const hasDownloading = state.models.some((item) => item.status === "downloading");
  if (hasDownloading && !state.modelRefreshTimer) {
    state.modelRefreshTimer = setInterval(loadModels, 4000);
  }
  if (!hasDownloading && state.modelRefreshTimer) {
    clearInterval(state.modelRefreshTimer);
    state.modelRefreshTimer = null;
  }
}

function renderSidebarProjects() {
  const container = el("sidebarProjectList");
  if (!container) {
    return;
  }
  container.innerHTML = "";
  if (state.projects.length === 0) {
    const empty = document.createElement("div");
    empty.className = "rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-[rgba(255,247,239,0.82)] p-4 text-sm leading-6 text-muted";
    empty.textContent = "No projects yet.";
    container.appendChild(empty);
    return;
  }

  state.projects.slice(0, 6).forEach((project) => {
    const button = document.createElement("button");
    button.className = `sidebar-project rounded-2xl border px-4 py-3 text-left ${state.selectedProjectId === project.id ? "active" : ""}`;
    button.innerHTML = `
      <strong class="block text-sm">${project.name}</strong>
      <span class="mt-1 block text-xs text-muted">${project.description || "Saved OCR workflow"}</span>
    `;
    button.addEventListener("click", async () => {
      await openProject(project.id, "overview");
    });
    container.appendChild(button);
  });
}

function renderProjectsTable() {
  const tbody = el("projectsTableBody");
  const emptyState = el("projectsEmptyState");
  tbody.innerHTML = "";

  if (state.projects.length === 0) {
    emptyState.classList.remove("hidden");
    return;
  }
  emptyState.classList.add("hidden");

  state.projects.forEach((project) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    tr.innerHTML = `
      <td class="px-4 py-4 align-top">
        <strong class="block text-sm text-ink">${project.name}</strong>
      </td>
      <td class="px-4 py-4 align-top text-sm text-muted">${project.description || "Saved OCR workflow"}</td>
      <td class="px-4 py-4 align-top text-sm text-muted">${(project.settings?.naming_pattern || emptyProjectSettings().naming_pattern)}</td>
      <td class="px-4 py-4 align-top">
        <div class="flex flex-wrap gap-2">
          <button data-action="view" data-project-id="${project.id}" class="rounded-full bg-gradient-to-br from-ember to-emberdark px-4 py-2 text-sm font-semibold text-white">View Project</button>
          <button data-action="edit" data-project-id="${project.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-4 py-2 text-sm font-semibold text-emberdark">Edit</button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });

  tbody.querySelectorAll("[data-action='view']").forEach((button) => {
    button.addEventListener("click", async () => {
      await openProject(Number(button.dataset.projectId), "overview");
    });
  });
  tbody.querySelectorAll("[data-action='edit']").forEach((button) => {
    button.addEventListener("click", async () => {
      const project = state.projects.find((item) => item.id === Number(button.dataset.projectId));
      if (!project) return;
      applyProject(project);
      switchView("projectEditor");
    });
  });
}

function renderDashboard() {
  el("dashboardUser").textContent = state.currentUser?.username || "Signed out";
  if (state.currentUser?.role) {
    el("dashboardUser").textContent = `${state.currentUser.username} (${state.currentUser.role})`;
  }
  el("dashboardProjectCount").textContent = String(state.projects.length);
  const selected = getSelectedProject();
  el("dashboardProjectName").textContent = selected ? selected.name : "None selected";
  el("topbarUsername").textContent = state.currentUser?.role
    ? `${state.currentUser.username} (${state.currentUser.role})`
    : state.currentUser?.username || "Unknown";
}

function parseAmount(value) {
  const parsed = Number(String(value ?? "").replaceAll(",", "").trim());
  return Number.isFinite(parsed) ? Math.abs(parsed) : 0;
}

function formatMoney(value) {
  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value || 0));
}

function formatPct(value) {
  return `${Number(value || 0).toFixed(1)}%`;
}

function bankSheetName(record) {
  if (!record?.source_timestamp) return "Unknown";
  const [sheetName] = String(record.source_timestamp).split(":row:");
  return sheetName || "Unknown";
}

function dashboardMatchStatus(record) {
  const ruleStatus = derivedRuleMeta(record).status;
  if (ruleStatus) {
    return ruleStatus;
  }
  const status = String(record?.match_status || "");
  if (status === "linked_to_bank") {
    return "matched";
  }
  return status;
}

function resolveTransactionDirection(record) {
  const direct = String(record?.transaction_direction || "").toLowerCase();
  if (direct === "debit" || direct === "credit") {
    return direct;
  }
  const raw = String(record?.raw_text || "").toLowerCase();
  const name = String(record?.company_name || "").toLowerCase();
  const combined = `${raw} ${name}`;
  if (
    /\bpayment received\b|\bcredit\b|\bdeposit\b|\btop up\b|\bprofit credit\b|\bfrom\b/.test(combined)
    && !/\bdebit transaction\b/.test(combined)
  ) {
    return "credit";
  }
  if (
    /\bdebit\b|\bdebit transaction\b|\bpurchase\b|\btransfer\b|\bwithdrawal\b|\batm wdl\b|\bfee\b|\bcharges?\b|\bto\b/.test(combined)
  ) {
    return "debit";
  }
  return "unknown";
}

function bankTransactionRecords() {
  return state.documents.filter((item) => item.source_type === "sheet" && item.doc_type === "BankTransaction");
}

function filteredBankTransactionRecords() {
  const query = state.dashboardSearch.trim().toLowerCase();
  return bankTransactionRecords().filter((item) => {
    const direction = resolveTransactionDirection(item);
    const bank = bankSheetName(item);
    const date = /^\d{4}-\d{2}-\d{2}$/.test(item.date || "") ? item.date : "";
    const matchesQuery =
      !query ||
      [
        bank,
        item.date,
        item.number,
        item.company_name,
        item.amount,
        item.match_status,
        item.match_basis,
        item.raw_text,
      ]
        .join(" ")
        .toLowerCase()
        .includes(query);
    const matchesDateFrom = !state.dashboardDateFrom || (date && date >= state.dashboardDateFrom);
    const matchesDateTo = !state.dashboardDateTo || (date && date <= state.dashboardDateTo);
    const matchesDirection = !state.dashboardDirectionFilter || direction === state.dashboardDirectionFilter;
    const matchesMatch = !state.dashboardMatchFilter || dashboardMatchStatus(item) === state.dashboardMatchFilter;
    const matchesBank = !state.dashboardBankFilter || bank === state.dashboardBankFilter;
    return matchesQuery && matchesDateFrom && matchesDateTo && matchesDirection && matchesMatch && matchesBank;
  });
}

async function loadDashboardAnalytics(resetDrilldown = false) {
  if (!state.selectedProjectId) {
    state.dashboardAnalytics = null;
    state.dashboardBankOptions = [];
    state.dashboardDrilldownRows = [];
    state.dashboardDrilldownPagination = { page: 1, page_size: DASHBOARD_DRILLDOWN_PAGE_SIZE, total: 0, total_pages: 1 };
    renderOverviewAnalytics();
    return;
  }
  if (resetDrilldown) {
    state.dashboardDrilldownMode = "all";
    state.dashboardDrilldownValue = "";
    state.dashboardDrilldownPage = 1;
    state.dashboardDrilldownTitle = "All Filtered Bank Rows";
    state.dashboardDrilldownSubtitle = "Current dashboard dataset after applying filters.";
    state.dashboardDrilldownSearch = "";
    state.dashboardDrilldownDirection = "";
    state.dashboardDrilldownMatch = "";
    if (el("overviewDrilldownSearch")) el("overviewDrilldownSearch").value = "";
    if (el("overviewDrilldownDirection")) el("overviewDrilldownDirection").value = "";
    if (el("overviewDrilldownMatch")) el("overviewDrilldownMatch").value = "";
  }
  const params = new URLSearchParams({
    search: state.dashboardSearch,
    direction: state.dashboardDirectionFilter,
    match_status: state.dashboardMatchFilter,
    bank: state.dashboardBankFilter,
    date_from: state.dashboardDateFrom,
    date_to: state.dashboardDateTo,
    drilldown_mode: state.dashboardDrilldownMode || "all",
    drilldown_value: state.dashboardDrilldownValue || "",
    drilldown_search: state.dashboardDrilldownSearch,
    drilldown_direction: state.dashboardDrilldownDirection,
    drilldown_match: state.dashboardDrilldownMatch,
    page: String(state.dashboardDrilldownPage || 1),
    page_size: String(DASHBOARD_DRILLDOWN_PAGE_SIZE),
  });
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/dashboard/bank?${params.toString()}`);
  state.dashboardAnalytics = payload.analytics || null;
  state.dashboardBankOptions = payload.filters?.banks || [];
  state.dashboardDrilldownRows = payload.drilldown?.rows || [];
  state.dashboardDrilldownPagination = payload.drilldown?.pagination || { page: 1, page_size: DASHBOARD_DRILLDOWN_PAGE_SIZE, total: 0, total_pages: 1 };
  renderOverviewAnalytics();
}

function setDashboardDrilldown(title, subtitle, mode = "all", value = "") {
  state.dashboardDrilldownTitle = title;
  state.dashboardDrilldownSubtitle = subtitle;
  state.dashboardDrilldownMode = mode;
  state.dashboardDrilldownValue = value;
  state.dashboardDrilldownSearch = "";
  state.dashboardDrilldownDirection = "";
  state.dashboardDrilldownMatch = "";
  state.dashboardDrilldownPage = 1;
  if (el("overviewDrilldownSearch")) el("overviewDrilldownSearch").value = "";
  if (el("overviewDrilldownDirection")) el("overviewDrilldownDirection").value = "";
  if (el("overviewDrilldownMatch")) el("overviewDrilldownMatch").value = "";
  loadDashboardAnalytics(false);
}

function updateDashboardDrilldownPagination(totalItems) {
  const totalPages = Math.max(1, Number(state.dashboardDrilldownPagination?.total_pages || 1));
  const currentPage = Math.max(1, Number(state.dashboardDrilldownPagination?.page || 1));
  el("overviewDrilldownPageLabel").textContent = `Page ${currentPage} of ${totalPages}`;
  el("overviewDrilldownSummary").textContent = `${totalItems} row${totalItems === 1 ? "" : "s"}`;
  el("overviewDrilldownPrevPage").disabled = currentPage <= 1;
  el("overviewDrilldownNextPage").disabled = currentPage >= totalPages;
  el("overviewDrilldownPrevPage").style.opacity = currentPage <= 1 ? "0.45" : "1";
  el("overviewDrilldownNextPage").style.opacity = currentPage >= totalPages ? "0.45" : "1";
}

function renderOverviewDrilldown() {
  el("overviewDrilldownTitle").textContent = state.dashboardDrilldownTitle;
  el("overviewDrilldownSubtitle").textContent = state.dashboardDrilldownSubtitle;
  const tbody = el("overviewDrilldownTable").querySelector("tbody");
  tbody.innerHTML = "";
  const rows = state.dashboardDrilldownRows || [];
  updateDashboardDrilldownPagination(Number(state.dashboardDrilldownPagination?.total || 0));
  if (rows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="px-4 py-6 text-sm text-muted">No rows match the current dashboard drill-down.</td></tr>`;
    return;
  }
  rows.forEach((item) => {
    const linkedAction = item.matched_record_company_name || item.matched_record_number || item.matched_record_amount
      ? `
        <button type="button" data-linked-record-id="${item.id}" class="inline-flex h-9 w-9 items-center justify-center rounded-full bg-[rgba(64,145,108,0.16)] text-[#2f6f54] transition hover:bg-[rgba(64,145,108,0.26)]" title="Open linked record details">
          <i class="ph ph-link-simple"></i>
        </button>
      `
      : `<span class="text-xs text-muted">-</span>`;
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(bankSheetName(item))}</td>
      <td class="px-4 py-4">${escapeHtml(item.date || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(resolveTransactionDirection(item))}</td>
      <td class="px-4 py-4">${escapeHtml(canonicalVendorName(item.company_name) || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.number || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.amount || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(dashboardMatchStatus(item) || "-")}</td>
      <td class="px-4 py-4">${linkedAction}</td>
    `;
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-linked-record-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const record = state.dashboardDrilldownRows.find((item) => item.id === Number(button.dataset.linkedRecordId));
      if (record) {
        openLinkedRecordModal(record);
      }
    });
  });
}

function populateDashboardBankFilter() {
  const node = el("dashboardBankFilter");
  const current = state.dashboardBankFilter;
  const banks = [...new Set(state.dashboardBankOptions || [])].sort();
  node.innerHTML = '<option value="">All Banks / Sheets</option>';
  banks.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    node.appendChild(option);
  });
  node.value = current;
}

function renderOverviewAnalytics() {
  const empty = el("overviewDashboardEmpty");
  const content = el("overviewDashboardContent");
  const kpiGrid = el("overviewKpiGrid");
  const comparisonTable = el("overviewComparisonTable");
  const agingSnapshot = el("overviewAgingSnapshot");
  const exceptionSnapshot = el("overviewExceptionSnapshot");
  const directionChart = el("overviewDirectionChart");
  const coverageChart = el("overviewCoverageChart");
  const monthlyTable = el("overviewMonthlyTable");
  const bankTable = el("overviewBankTable");
  const attentionTable = el("overviewAttentionTable");
  const vendorTable = el("overviewVendorTable");
  const categoryTable = el("overviewCategoryTable");
  const anomalyTable = el("overviewAnomalyTable");
  const analytics = state.dashboardAnalytics;

  populateDashboardBankFilter();
  if (!analytics || !analytics.totals || !analytics.totals.bank_transactions) {
    empty.classList.remove("hidden");
    content.classList.add("hidden");
    kpiGrid.innerHTML = "";
    comparisonTable.innerHTML = "";
    agingSnapshot.innerHTML = "";
    exceptionSnapshot.innerHTML = "";
    directionChart.innerHTML = "";
    coverageChart.innerHTML = "";
    monthlyTable.innerHTML = "";
    bankTable.innerHTML = "";
    attentionTable.innerHTML = "";
    vendorTable.innerHTML = "";
    categoryTable.innerHTML = "";
    anomalyTable.innerHTML = "";
    renderOverviewDrilldown();
    return;
  }

  empty.classList.add("hidden");
  content.classList.remove("hidden");

  const totals = analytics.totals || {};
  const counts = analytics.counts || {};
  const kpis = [
    ["Bank Transactions", String(totals.bank_transactions || 0), "Imported rows from bank statement sheets"],
    ["Total Debit", `${formatMoney(totals.total_debit || 0)} AED`, "Outgoing debit transactions"],
    ["Total Credit", `${formatMoney(totals.total_credit || 0)} AED`, "Incoming credit transactions"],
    ["Receipt Coverage", formatPct(totals.coverage_pct || 0), `${counts.matched_debit || 0} of ${counts.receipt_relevant_debit || 0} debit transactions matched`],
    ["Missing Receipt Debit", `${formatMoney(totals.missing_receipt_debit || 0)} AED`, `${counts.missing_debit || 0} debit transactions still need support`],
    ["Matched Debit Amount", `${formatMoney(totals.matched_debit_amount || 0)} AED`, "Debit amount already linked to receipt or invoice"],
    ["Banks / Sheets", String(totals.banks_count || 0), "Distinct imported bank statement tabs"],
    ["Credits Marked N/A", String(totals.credits_not_applicable || 0), "Credit transactions excluded from receipt coverage"],
  ];
  kpiGrid.innerHTML = kpis.map(([label, value, note], index) => `
    <button type="button" data-dashboard-kpi="${index}" class="dashboard-kpi-card">
      <div class="dashboard-kpi-label">${label}</div>
      <div class="dashboard-kpi-value">${value}</div>
      <div class="dashboard-kpi-note">${note}</div>
    </button>
  `).join("");

  const sortedMonthlyRows = [...(analytics.monthly || [])].sort((a, b) => String(a.month || "").localeCompare(String(b.month || "")));
  const latestMonth = sortedMonthlyRows[sortedMonthlyRows.length - 1] || null;
  const previousMonth = sortedMonthlyRows[sortedMonthlyRows.length - 2] || null;
  const comparisonEntries = [
    {
      label: "Debit",
      current: latestMonth?.debit || 0,
      previous: previousMonth?.debit || 0,
      format: (value) => `${formatMoney(value)} AED`,
      inverseGood: true,
    },
    {
      label: "Credit",
      current: latestMonth?.credit || 0,
      previous: previousMonth?.credit || 0,
      format: (value) => `${formatMoney(value)} AED`,
      inverseGood: false,
    },
    {
      label: "Missing Receipt",
      current: latestMonth?.missing || 0,
      previous: previousMonth?.missing || 0,
      format: (value) => `${formatMoney(value)} AED`,
      inverseGood: true,
    },
    {
      label: "Coverage",
      current: latestMonth && latestMonth.debit ? (((latestMonth.debit || 0) - (latestMonth.missing || 0)) / Math.max(latestMonth.debit || 0, 1)) * 100 : 0,
      previous: previousMonth && previousMonth.debit ? (((previousMonth.debit || 0) - (previousMonth.missing || 0)) / Math.max(previousMonth.debit || 0, 1)) * 100 : 0,
      format: (value) => formatPct(value),
      inverseGood: false,
    },
  ];
  comparisonTable.innerHTML = latestMonth ? `
    <div class="dashboard-snapshot-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="dashboard-kpi-label">Current Window</div>
          <div class="mt-2 text-lg font-semibold">${escapeHtml(latestMonth.month || "Latest Month")}</div>
        </div>
        <div class="text-right">
          <div class="dashboard-kpi-label">Compared To</div>
          <div class="mt-2 text-sm font-semibold text-muted">${escapeHtml(previousMonth?.month || "No prior month")}</div>
        </div>
      </div>
      <div class="mt-4 dashboard-comparison-grid">
        ${comparisonEntries.map((entry) => {
          const delta = (entry.current || 0) - (entry.previous || 0);
          const direction = Math.abs(delta) < 0.0001 ? "flat" : delta > 0 ? (entry.inverseGood ? "up" : "down") : (entry.inverseGood ? "down" : "up");
          const deltaPrefix = delta > 0 ? "+" : "";
          return `
            <div class="dashboard-comparison-row">
              <div>
                <div class="text-sm font-semibold">${entry.label}</div>
                <div class="mt-1 text-xs text-muted">${entry.format(entry.current || 0)} now / ${entry.format(entry.previous || 0)} before</div>
              </div>
              <span class="dashboard-chip">${entry.format(entry.current || 0)}</span>
              <span class="dashboard-trend-pill ${direction}">${deltaPrefix}${entry.format(delta)}</span>
            </div>
          `;
        }).join("")}
      </div>
    </div>
  ` : `<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white p-4 text-sm text-muted">At least one monthly bucket is needed before period comparison can be shown.</div>`;

  const agingRows = state.closeSummary?.aging || [];
  const maxAgingAmount = Math.max(1, ...agingRows.map((item) => item.amount || 0));
  agingSnapshot.innerHTML = agingRows.length ? `
    <div class="dashboard-snapshot-stack">
      ${agingRows.map((item) => `
        <button type="button" data-dashboard-aging="${escapeHtml(item.bucket)}" class="dashboard-snapshot-card">
          <div class="dashboard-snapshot-row">
            <strong class="text-sm">${escapeHtml(item.bucket)}</strong>
            <span class="dashboard-amount-pill ${item.bucket === "91+ days" ? "danger" : "warning"}">${formatMoney(item.amount || 0)} AED</span>
          </div>
          <div class="mt-2 text-xs text-muted">${item.count} unresolved item${item.count === 1 ? "" : "s"}</div>
          <div class="dashboard-inline-bar"><span style="width:${((item.amount || 0) / maxAgingAmount) * 100}%"></span></div>
        </button>
      `).join("")}
    </div>
  ` : `<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white p-4 text-sm text-muted">No unresolved aging snapshot is available for the current project yet.</div>`;

  const exceptionSummary = state.exceptionsSummary || {};
  const exceptionRows = [
    ["Installments", exceptionSummary.installments || 0],
    ["Refund Pairs", exceptionSummary.refund_pairs || 0],
    ["Split Payments", exceptionSummary.split_groups || 0],
    ["Duplicates", exceptionSummary.duplicates || 0],
    ["Mismatches", exceptionSummary.mismatches || 0],
  ];
  const maxExceptionCount = Math.max(1, ...exceptionRows.map(([, count]) => count));
  exceptionSnapshot.innerHTML = exceptionRows.some(([, count]) => count > 0) ? `
    <div class="dashboard-snapshot-stack">
      <div class="dashboard-snapshot-card">
        <div class="dashboard-kpi-label">Grouped Cases</div>
        <div class="mt-2 text-2xl font-bold">${exceptionSummary.total || 0}</div>
        <div class="mt-2 text-sm text-muted">Server-grouped exception clusters currently open for review.</div>
      </div>
      ${exceptionRows.map(([label, count]) => `
        <button type="button" data-dashboard-exception="${label}" class="dashboard-snapshot-card">
          <div class="dashboard-snapshot-row">
            <strong class="text-sm">${label}</strong>
            <span class="dashboard-chip">${count} case${count === 1 ? "" : "s"}</span>
          </div>
          <div class="dashboard-inline-bar"><span style="width:${(count / maxExceptionCount) * 100}%"></span></div>
        </button>
      `).join("")}
    </div>
  ` : `<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white p-4 text-sm text-muted">No grouped exception cases are currently open.</div>`;

  const directionStats = [
    ["Debit", counts.debit || 0, "#b43a3a"],
    ["Credit", counts.credit || 0, "#40916c"],
    ["Unknown", counts.unknown || 0, "#7c6a5d"],
  ];
  const maxDirectionCount = Math.max(1, ...directionStats.map(([, count]) => count));
  directionChart.innerHTML = directionStats.map(([label, count, color]) => `
    <button type="button" data-dashboard-direction="${label.toLowerCase()}" class="dashboard-stat-card">
      <div class="mb-2 flex items-center justify-between text-sm">
        <strong>${label}</strong>
        <span class="text-muted">${count} rows</span>
      </div>
      <div class="dashboard-bar-track">
        <div class="dashboard-bar-fill" style="width:${(count / maxDirectionCount) * 100}%;background:${color}"></div>
      </div>
    </button>
  `).join("");

  const coverageStats = [
    ["Matched", counts.matched || 0, "#40916c"],
    ["Missing", counts.missing_receipt || 0, "#b43a3a"],
    ["Not Applicable", counts.not_applicable || 0, "#d97706"],
  ];
  const maxCoverageCount = Math.max(1, ...coverageStats.map(([, count]) => count));
  coverageChart.innerHTML = coverageStats.map(([label, count, color]) => `
    <button type="button" data-dashboard-match="${label === "Missing" ? "missing_receipt" : label === "Not Applicable" ? "not_applicable" : "matched"}" class="dashboard-stat-card">
      <div class="mb-2 flex items-center justify-between text-sm">
        <strong>${label}</strong>
        <span class="text-muted">${count} rows</span>
      </div>
      <div class="dashboard-bar-track">
        <div class="dashboard-bar-fill" style="width:${(count / maxCoverageCount) * 100}%;background:${color}"></div>
      </div>
    </button>
  `).join("");

  const monthlyRows = sortedMonthlyRows;
  const maxMonthly = Math.max(1, ...monthlyRows.flatMap((values) => [values.debit || 0, values.credit || 0, values.missing || 0]));
  monthlyTable.innerHTML = monthlyRows.map((values) => {
    const month = values.month || "Unknown";
    const net = (values.credit || 0) - (values.debit || 0);
    return `
      <button type="button" data-dashboard-month="${month}" class="dashboard-month-card">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <strong class="text-sm">${month}</strong>
          <span class="dashboard-net-pill ${net >= 0 ? "positive" : "negative"}">Net ${formatMoney(net)} AED</span>
        </div>
        <div class="mt-3 space-y-2">
          <div>
            <div class="mb-1 flex items-center justify-between text-xs text-muted"><span>Debit</span><span>${formatMoney(values.debit || 0)} AED</span></div>
            <div class="dashboard-mini-track"><div class="dashboard-mini-fill debit" style="width:${((values.debit || 0) / maxMonthly) * 100}%"></div></div>
          </div>
          <div>
            <div class="mb-1 flex items-center justify-between text-xs text-muted"><span>Credit</span><span>${formatMoney(values.credit || 0)} AED</span></div>
            <div class="dashboard-mini-track"><div class="dashboard-mini-fill credit" style="width:${((values.credit || 0) / maxMonthly) * 100}%"></div></div>
          </div>
          <div>
            <div class="mb-1 flex items-center justify-between text-xs text-muted"><span>Missing Receipt Debit</span><span>${formatMoney(values.missing || 0)} AED</span></div>
            <div class="dashboard-mini-track"><div class="dashboard-mini-fill warning" style="width:${((values.missing || 0) / maxMonthly) * 100}%"></div></div>
          </div>
        </div>
      </button>
    `;
  }).join("");

  bankTable.innerHTML = (analytics.banks || []).map((values) => {
    const bank = values.bank || "Unknown";
    const matchRate = values.match_rate || 0;
    return `
      <button type="button" data-dashboard-bank="${escapeHtml(bank)}" class="dashboard-bank-card">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <strong class="text-sm">${escapeHtml(bank)}</strong>
          <span class="dashboard-chip">${values.count} rows</span>
        </div>
        <div class="mt-3 grid gap-3 md:grid-cols-3">
          <div><div class="text-[11px] uppercase tracking-[0.12em] text-muted">Debit</div><div class="mt-1 text-sm font-semibold">${formatMoney(values.debit || 0)} AED</div></div>
          <div><div class="text-[11px] uppercase tracking-[0.12em] text-muted">Credit</div><div class="mt-1 text-sm font-semibold">${formatMoney(values.credit || 0)} AED</div></div>
          <div><div class="text-[11px] uppercase tracking-[0.12em] text-muted">Match Rate</div><div class="mt-1 text-sm font-semibold">${formatPct(matchRate)}</div><div class="dashboard-mini-track mt-2"><div class="dashboard-mini-fill credit" style="width:${matchRate}%"></div></div></div>
        </div>
      </button>
    `;
  }).join("");

  const vendorRows = analytics.vendors || [];
  vendorTable.innerHTML = vendorRows.length ? vendorRows.map((entry) => `
    <button type="button" data-dashboard-vendor="${escapeHtml(entry.vendor)}" class="dashboard-list-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="max-w-[70%] text-sm">${escapeHtml(entry.vendor)}</strong>
        <span class="dashboard-amount-pill warning">${formatMoney(entry.amount || 0)} AED</span>
      </div>
      <div class="mt-2 text-xs text-muted">${entry.count} missing transaction${entry.count === 1 ? "" : "s"}</div>
    </button>
  `).join("") : `<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white p-4 text-sm text-muted">No missing-receipt vendors for this project.</div>`;

  const attentionRows = analytics.attention || [];
  attentionTable.innerHTML = attentionRows.length ? attentionRows.map((item, index) => `
    <button type="button" data-dashboard-attention="${index}" class="dashboard-list-card attention">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="max-w-[72%] text-sm">${escapeHtml(item.canonical_vendor_name || canonicalVendorName(item.company_name) || "Unknown")}</strong>
        <span class="dashboard-amount-pill danger">${formatMoney(parseAmount(item.amount))} AED</span>
      </div>
      <div class="mt-2 text-xs leading-6 text-muted">${escapeHtml(item.bank_name || bankSheetName(item))} • ${escapeHtml(item.date || "Unknown date")} • ${escapeHtml(item.number || "Unknown ref")}</div>
    </button>
  `).join("") : `<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white p-4 text-sm text-muted">No unmatched debit transactions right now.</div>`;

  const categoryRows = analytics.categories || [];
  categoryTable.innerHTML = categoryRows.length ? categoryRows.map((entry) => `
    <button type="button" data-dashboard-category="${escapeHtml(entry.category)}" class="dashboard-list-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="max-w-[72%] text-sm">${escapeHtml(entry.category)}</strong>
        <span class="dashboard-amount-pill">${formatMoney(entry.amount || 0)} AED</span>
      </div>
      <div class="mt-2 text-xs text-muted">${entry.count} debit transaction${entry.count === 1 ? "" : "s"}</div>
    </button>
  `).join("") : `<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white p-4 text-sm text-muted">No categorized debit transactions yet.</div>`;

  const anomalyRows = analytics.anomalies || [];
  anomalyTable.innerHTML = anomalyRows.length ? anomalyRows.map((item, index) => `
    <button type="button" data-dashboard-anomaly="${index}" class="dashboard-list-card attention">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="max-w-[72%] text-sm">${escapeHtml(item.canonical_vendor_name || canonicalVendorName(item.company_name) || "Unknown")}</strong>
        <span class="dashboard-chip">${escapeHtml(item.confidence_label || item.dashboard_match_status || "-")}</span>
      </div>
      <div class="mt-2 text-xs leading-6 text-muted">${escapeHtml(item.bank_name || bankSheetName(item))} • ${escapeHtml(item.date || "-")} • ${escapeHtml(item.amount || "-")}</div>
    </button>
  `).join("") : `<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white p-4 text-sm text-muted">No anomaly rows under current filters.</div>`;

  const kpiRows = [
    { mode: "all", value: "" },
    { mode: "debit", value: "" },
    { mode: "credit", value: "" },
    { mode: "receipt_relevant_debit", value: "" },
    { mode: "match", value: "missing_receipt" },
    { mode: "matched_debit", value: "" },
    { mode: "all", value: "" },
    { mode: "credits_na", value: "" },
  ];
  kpiGrid.querySelectorAll("[data-dashboard-kpi]").forEach((button) => {
    button.addEventListener("click", () => {
      const index = Number(button.dataset.dashboardKpi);
      const scope = kpiRows[index] || { mode: "all", value: "" };
      setDashboardDrilldown(kpis[index][0], kpis[index][2], scope.mode, scope.value);
    });
  });
  directionChart.querySelectorAll("[data-dashboard-direction]").forEach((button) => {
    button.addEventListener("click", () => {
      const direction = button.dataset.dashboardDirection;
      setDashboardDrilldown(`${direction[0].toUpperCase()}${direction.slice(1)} Transactions`, `Filtered bank rows with direction ${direction}.`, direction, "");
    });
  });
  coverageChart.querySelectorAll("[data-dashboard-match]").forEach((button) => {
    button.addEventListener("click", () => {
      const match = button.dataset.dashboardMatch;
      setDashboardDrilldown(`${match.replaceAll("_", " ")}`, `Filtered bank rows with match state ${match}.`, "match", match);
    });
  });
  monthlyTable.querySelectorAll("[data-dashboard-month]").forEach((button) => {
    button.addEventListener("click", () => {
      const month = button.dataset.dashboardMonth;
      setDashboardDrilldown(`Month ${month}`, `Bank rows within ${month}.`, "month", month);
    });
  });
  bankTable.querySelectorAll("[data-dashboard-bank]").forEach((button) => {
    button.addEventListener("click", () => {
      const bank = button.dataset.dashboardBank;
      setDashboardDrilldown(bank, `Bank rows from sheet ${bank}.`, "bank", bank);
    });
  });
  vendorTable.querySelectorAll("[data-dashboard-vendor]").forEach((button) => {
    button.addEventListener("click", () => {
      const vendor = button.dataset.dashboardVendor;
      setDashboardDrilldown(vendor, `Missing receipt debit rows for vendor ${vendor}.`, "vendor_missing", vendor);
    });
  });
  attentionTable.querySelectorAll("[data-dashboard-attention]").forEach((button) => {
    button.addEventListener("click", () => {
      const item = attentionRows[Number(button.dataset.dashboardAttention)];
      setDashboardDrilldown(item.canonical_vendor_name || canonicalVendorName(item.company_name) || "Needs Attention", "Focused drill-down for the selected high-value missing receipt item.", "focus", String(item.id));
    });
  });
  categoryTable.querySelectorAll("[data-dashboard-category]").forEach((button) => {
    button.addEventListener("click", () => {
      const key = button.dataset.dashboardCategory;
      setDashboardDrilldown(key, `Debit rows assigned to category ${key}.`, "category", key);
    });
  });
  anomalyTable.querySelectorAll("[data-dashboard-anomaly]").forEach((button) => {
    button.addEventListener("click", () => {
      const item = anomalyRows[Number(button.dataset.dashboardAnomaly)];
      setDashboardDrilldown(canonicalVendorName(item.company_name) || "Anomaly", "Focused drill-down for the selected anomaly row.", "focus", String(item.id));
    });
  });
  agingSnapshot.querySelectorAll("[data-dashboard-aging]").forEach((button) => {
    button.addEventListener("click", () => {
      const bucket = button.dataset.dashboardAging;
      setDashboardDrilldown(bucket, `Unresolved bank rows that fall under aging bucket ${bucket}.`, "aging", bucket);
    });
  });
  exceptionSnapshot.querySelectorAll("[data-dashboard-exception]").forEach((button) => {
    button.addEventListener("click", () => {
      const label = button.dataset.dashboardException;
      const value = label === "Installments"
        ? "installment"
        : label === "Refund Pairs"
          ? "refund"
          : label === "Split Payments"
            ? "split"
            : label === "Duplicates"
              ? "duplicate"
              : "mismatch";
      setDashboardDrilldown(label, `Bank rows related to ${label.toLowerCase()} exception cases.`, "exception", value);
    });
  });

  renderOverviewDrilldown();
}

function renderActiveProjectTab() {
  if (!state.selectedProjectId) return;
  if (state.projectTab === "reconciliation") {
    renderReconciliationWorkspace();
  } else if (state.projectTab === "review") {
    renderReviewQueue();
  } else if (state.projectTab === "exceptions") {
    renderExceptionsWorkspace();
  } else if (state.projectTab === "feedback") {
    renderFeedbackWorkspace();
  } else if (state.projectTab === "vendors") {
    renderVendors();
  } else if (state.projectTab === "rules") {
    renderRules();
  } else if (state.projectTab === "tags") {
    renderTags();
  } else if (state.projectTab === "search") {
    renderGlobalSearch();
  } else if (state.projectTab === "evidence") {
    renderEvidence();
  } else if (state.projectTab === "activity") {
    renderActivityFeed();
  } else if (state.projectTab === "members") {
    renderProjectMembers();
  } else if (state.projectTab === "close") {
    renderCloseWorkspace();
  } else if (state.projectTab === "resources") {
    renderResources();
  } else if (state.projectTab === "results") {
    renderHistoryTable();
  } else if (state.projectTab === "documents") {
    renderDocumentsTable();
  }
}

function memberUsernameById(userId) {
  return state.projectMembers.find((item) => item.user_id === userId)?.username || "";
}

function renderProjectMembers() {
  const tbody = el("membersTable")?.querySelector("tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  const members = state.projectMembers || [];
  el("membersTotal").textContent = String(members.length);
  el("membersReviewers").textContent = String(members.filter((item) => ["reviewer", "admin", "owner"].includes(item.project_role)).length);
  el("membersViewers").textContent = String(members.filter((item) => item.project_role === "viewer").length);
  if (!members.length) {
    tbody.innerHTML = `<tr><td colspan="5" class="px-4 py-6 text-sm text-muted">No project members configured yet.</td></tr>`;
  } else {
    members.forEach((item) => {
      const tr = document.createElement("tr");
      tr.className = "border-b border-[rgba(77,49,29,0.08)]";
      const canRemove = item.project_role !== "owner";
      tr.innerHTML = `
        <td class="px-4 py-4">${escapeHtml(item.username || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.account_role || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.project_role || "-")}</td>
        <td class="px-4 py-4">${escapeHtml((item.created_at || "").slice(0, 10) || "-")}</td>
        <td class="px-4 py-4">${canRemove ? `<button type="button" data-member-remove="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Remove</button>` : `<span class="text-xs text-muted">Owner</span>`}</td>
      `;
      tbody.appendChild(tr);
    });
  }
  const assignNode = el("reviewAssignUser");
  if (assignNode) {
    const currentValue = assignNode.value;
    assignNode.innerHTML = '<option value="">Unassigned</option>';
    members.forEach((item) => {
      const option = document.createElement("option");
      option.value = String(item.user_id);
      option.textContent = `${item.username} (${item.project_role})`;
      assignNode.appendChild(option);
    });
    assignNode.value = currentValue;
  }
  tbody.querySelectorAll("[data-member-remove]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (!canManageProjectMembers()) return;
      await fetchJson(`/api/projects/${state.selectedProjectId}/members/${button.dataset.memberRemove}`, { method: "DELETE" });
      await loadProjectMembers();
      showSweetAlert("Member Removed", "Project member removed.", "success");
    });
  });
}

function renderCompaniesWorkspace() {
  const company = state.companySettings || {};
  const activeCompanyPane = state.companiesPane || "overview";
  const activeCompanyId = Number(state.currentUser?.company_id || company.id || 0);
  const companyDirectoryPageSize = 8;
  const companyRulesPageSize = 8;
  const partiesPageSize = 8;
  const companyProjects = (state.projects || []).filter((item) => Number(item.company_id || 0) === activeCompanyId);
  const companyProjectsSearchTerm = (state.companyProjectsSearch || "").trim().toLowerCase();
  const filteredCompanyProjects = companyProjects.filter((item) => {
    if (state.companyProjectsStatusFilter && (item.project_status || "active") !== state.companyProjectsStatusFilter) {
      return false;
    }
    if (!companyProjectsSearchTerm) {
      return true;
    }
    const haystack = [
      item.name || "",
      item.job_code || "",
      item.client_name || "",
      item.site_name || "",
      item.contract_number || "",
      item.description || "",
    ].join(" ").toLowerCase();
    return haystack.includes(companyProjectsSearchTerm);
  });
  el("companiesCurrentName").textContent = company.name || state.currentUser?.company_name || "-";
  if (el("companiesActiveName")) el("companiesActiveName").textContent = company.name || state.currentUser?.company_name || "-";
  if (el("companiesActiveMeta")) el("companiesActiveMeta").textContent = `${company.base_currency || "AED"} • ${company.vat_registration_number || "No VAT number"}`;
  el("companiesCurrentUser").textContent = state.currentUser?.username || "-";
  el("companiesProjectCount").textContent = String(companyProjects.length);
  const filteredCompanies = (state.companies || [])
    .filter((item) => {
      const search = (state.companiesDirectorySearch || "").trim().toLowerCase();
      if (!search) return true;
      return [item.name || "", item.base_currency || "", item.created_at || ""].join(" ").toLowerCase().includes(search);
    })
    .sort((a, b) => {
      switch (state.companiesDirectorySort || "name_asc") {
        case "name_desc":
          return (b.name || "").localeCompare(a.name || "");
        case "created_desc":
          return (b.created_at || "").localeCompare(a.created_at || "");
        case "created_asc":
          return (a.created_at || "").localeCompare(b.created_at || "");
        default:
          return (a.name || "").localeCompare(b.name || "");
      }
    });
  const companiesTotalPages = Math.max(1, Math.ceil(filteredCompanies.length / companyDirectoryPageSize));
  state.companiesDirectoryPage = Math.min(Math.max(1, state.companiesDirectoryPage || 1), companiesTotalPages);
  const visibleCompanies = filteredCompanies.slice((state.companiesDirectoryPage - 1) * companyDirectoryPageSize, state.companiesDirectoryPage * companyDirectoryPageSize);
  const companiesBody = el("companiesListTable")?.querySelector("tbody");
  if (companiesBody) {
    companiesBody.innerHTML = filteredCompanies.length
      ? visibleCompanies.map((item) => `
          <tr class="border-b border-[rgba(77,49,29,0.08)] ${item.is_active ? "bg-[#fff8f0]" : ""}">
            <td class="px-4 py-4">
              <div class="font-semibold text-ink">${escapeHtml(item.name || "-")}</div>
              <div class="text-xs text-muted">${item.is_active ? "Active company" : "Available company"}</div>
            </td>
            <td class="px-4 py-4">${escapeHtml(item.base_currency || "AED")}</td>
            <td class="px-4 py-4">${escapeHtml(formatDateTime(item.created_at) || "-")}</td>
            <td class="px-4 py-4"><button type="button" data-company-activate="${item.id}" class="rounded-full ${item.is_active ? "bg-[rgba(57,112,92,0.12)] text-[#275b4a]" : "bg-[rgba(165,78,45,0.1)] text-emberdark"} px-3 py-2 text-xs font-semibold">${item.is_active ? "Viewing" : "View"}</button></td>
          </tr>
        `).join("")
      : '<tr><td colspan="4" class="px-4 py-6 text-sm text-muted">No companies yet.</td></tr>';
  }
  if (el("companiesDirectorySearch")) el("companiesDirectorySearch").value = state.companiesDirectorySearch || "";
  if (el("companiesDirectorySort")) el("companiesDirectorySort").value = state.companiesDirectorySort || "name_asc";
  if (el("companiesDirectoryPaginationLabel")) {
    el("companiesDirectoryPaginationLabel").textContent = `${filteredCompanies.length} companies • Page ${state.companiesDirectoryPage} of ${companiesTotalPages}`;
    el("companiesDirectoryPrevPage").disabled = state.companiesDirectoryPage <= 1;
    el("companiesDirectoryNextPage").disabled = state.companiesDirectoryPage >= companiesTotalPages;
  }
  document.querySelectorAll(".company-pane-button").forEach((button) => {
    const active = button.dataset.companyPane === state.companiesPane;
    button.classList.toggle("bg-[#fff3e6]", active);
    button.classList.toggle("text-emberdark", active);
  });
  document.querySelectorAll("[data-company-pane-section]").forEach((node) => {
    node.classList.toggle("hidden", node.dataset.companyPaneSection !== state.companiesPane);
  });
  if (el("companySettingsName")) {
    el("companySettingsName").value = company.name || state.currentUser?.company_name || "";
    el("companySettingsCurrency").value = company.base_currency || "AED";
    el("companySettingsFiscalMonth").value = String(company.fiscal_year_start_month || 1);
    el("companySettingsVatNumber").value = company.vat_registration_number || "";
    el("companySettingsVatRate").value = company.vat_rate || "5.00";
  }
  const companyRulesBody = el("companiesAccountingRulesTable")?.querySelector("tbody");
  const filteredCompanyRules = (state.companyAccountingRules || [])
    .filter((item) => {
      if (state.companyRulesSourceFilter && (item.source_type || "") !== state.companyRulesSourceFilter) return false;
      const search = (state.companyRulesSearch || "").trim().toLowerCase();
      if (!search) return true;
      return [
        item.keyword || "",
        item.category || "",
        item.subcategory || "",
        item.account_code || "",
        item.offset_account_code || "",
      ].join(" ").toLowerCase().includes(search);
    })
    .sort((a, b) => {
      switch (state.companyRulesSort || "keyword_asc") {
        case "keyword_desc":
          return (b.keyword || "").localeCompare(a.keyword || "");
        case "created_desc":
          return (b.created_at || "").localeCompare(a.created_at || "");
        case "created_asc":
          return (a.created_at || "").localeCompare(b.created_at || "");
        default:
          return (a.keyword || "").localeCompare(b.keyword || "");
      }
    });
  const companyRulesTotalPages = Math.max(1, Math.ceil(filteredCompanyRules.length / companyRulesPageSize));
  state.companyRulesPage = Math.min(Math.max(1, state.companyRulesPage || 1), companyRulesTotalPages);
  const visibleCompanyRules = filteredCompanyRules.slice((state.companyRulesPage - 1) * companyRulesPageSize, state.companyRulesPage * companyRulesPageSize);
  if (companyRulesBody) {
    companyRulesBody.innerHTML = filteredCompanyRules.length
      ? visibleCompanyRules.map((item) => `
          <tr class="border-b border-[rgba(77,49,29,0.08)]">
            <td class="px-4 py-4">
              <div class="font-semibold text-ink">${escapeHtml(item.keyword || "-")}</div>
              <div class="text-xs text-muted">${item.auto_post ? "Auto-post" : "Review first"}${item.vat_flag ? " • VAT" : ""}</div>
            </td>
            <td class="px-4 py-4">${escapeHtml(item.source_type || "Any")}</td>
            <td class="px-4 py-4">${escapeHtml(item.category || "-")}${item.subcategory ? `<div class="text-xs text-muted">${escapeHtml(item.subcategory)}</div>` : ""}</td>
            <td class="px-4 py-4">${escapeHtml(accountFlowLabel(item.account_code, item.offset_account_code))}</td>
            <td class="px-4 py-4"><button type="button" data-company-accounting-rule-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
          </tr>
        `).join("")
      : '<tr><td colspan="5" class="px-4 py-6 text-sm text-muted">No company auto-posting rules yet.</td></tr>';
  }
  if (el("companyRulesSearch")) el("companyRulesSearch").value = state.companyRulesSearch || "";
  if (el("companyRulesSourceFilter")) el("companyRulesSourceFilter").value = state.companyRulesSourceFilter || "";
  if (el("companyRulesSort")) el("companyRulesSort").value = state.companyRulesSort || "keyword_asc";
  if (el("companyRulesPaginationLabel")) {
    el("companyRulesPaginationLabel").textContent = `${filteredCompanyRules.length} rules • Page ${state.companyRulesPage} of ${companyRulesTotalPages}`;
    el("companyRulesPrevPage").disabled = state.companyRulesPage <= 1;
    el("companyRulesNextPage").disabled = state.companyRulesPage >= companyRulesTotalPages;
  }
  ["companySupplierDefaultAccount", "companyCustomerDefaultAccount"].forEach((id) => {
    const node = el(id);
    if (!node) return;
    const currentValue = node.value;
    node.innerHTML = '<option value="">Default account</option>';
    (state.accountingAccounts || []).forEach((account) => {
      const option = document.createElement("option");
      option.value = account.code;
      option.textContent = accountLabel(account.code, account.code);
      node.appendChild(option);
    });
    if (currentValue) node.value = currentValue;
  });
  const supplierBody = el("companiesSuppliersTable")?.querySelector("tbody");
  const filteredSuppliers = (state.supplierParties || [])
    .filter((item) => {
      const search = (state.suppliersSearch || "").trim().toLowerCase();
      if (!search) return true;
      return [
        item.name || "",
        item.tax_registration_number || "",
        item.default_account_code || "",
        item.payment_terms_days ?? "",
      ].join(" ").toLowerCase().includes(search);
    })
    .sort((a, b) => {
      switch (state.suppliersSort || "name_asc") {
        case "name_desc":
          return (b.name || "").localeCompare(a.name || "");
        case "terms_desc":
          return Number(b.payment_terms_days || 0) - Number(a.payment_terms_days || 0);
        case "terms_asc":
          return Number(a.payment_terms_days || 0) - Number(b.payment_terms_days || 0);
        default:
          return (a.name || "").localeCompare(b.name || "");
      }
    });
  const suppliersTotalPages = Math.max(1, Math.ceil(filteredSuppliers.length / partiesPageSize));
  state.suppliersPage = Math.min(Math.max(1, state.suppliersPage || 1), suppliersTotalPages);
  const visibleSuppliers = filteredSuppliers.slice((state.suppliersPage - 1) * partiesPageSize, state.suppliersPage * partiesPageSize);
  if (supplierBody) {
    supplierBody.innerHTML = filteredSuppliers.length
      ? visibleSuppliers.map((item) => `
          <tr class="border-b border-[rgba(77,49,29,0.08)]">
            <td class="px-4 py-4">${escapeHtml(item.name || "-")}</td>
            <td class="px-4 py-4">${escapeHtml(item.tax_registration_number || "-")}</td>
            <td class="px-4 py-4">${escapeHtml(accountLabel(item.default_account_code || "-", "-"))}</td>
            <td class="px-4 py-4">${escapeHtml(String(item.payment_terms_days ?? "-"))}</td>
            <td class="px-4 py-4"><button type="button" data-company-party-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
          </tr>
        `).join("")
      : '<tr><td colspan="5" class="px-4 py-6 text-sm text-muted">No suppliers yet.</td></tr>';
  }
  if (el("suppliersSearch")) el("suppliersSearch").value = state.suppliersSearch || "";
  if (el("suppliersSort")) el("suppliersSort").value = state.suppliersSort || "name_asc";
  if (el("suppliersPaginationLabel")) {
    el("suppliersPaginationLabel").textContent = `${filteredSuppliers.length} suppliers • Page ${state.suppliersPage} of ${suppliersTotalPages}`;
    el("suppliersPrevPage").disabled = state.suppliersPage <= 1;
    el("suppliersNextPage").disabled = state.suppliersPage >= suppliersTotalPages;
  }
  const customerBody = el("companiesCustomersTable")?.querySelector("tbody");
  const filteredCustomers = (state.customerParties || [])
    .filter((item) => {
      const search = (state.customersSearch || "").trim().toLowerCase();
      if (!search) return true;
      return [
        item.name || "",
        item.tax_registration_number || "",
        item.default_account_code || "",
        item.payment_terms_days ?? "",
      ].join(" ").toLowerCase().includes(search);
    })
    .sort((a, b) => {
      switch (state.customersSort || "name_asc") {
        case "name_desc":
          return (b.name || "").localeCompare(a.name || "");
        case "terms_desc":
          return Number(b.payment_terms_days || 0) - Number(a.payment_terms_days || 0);
        case "terms_asc":
          return Number(a.payment_terms_days || 0) - Number(b.payment_terms_days || 0);
        default:
          return (a.name || "").localeCompare(b.name || "");
      }
    });
  const customersTotalPages = Math.max(1, Math.ceil(filteredCustomers.length / partiesPageSize));
  state.customersPage = Math.min(Math.max(1, state.customersPage || 1), customersTotalPages);
  const visibleCustomers = filteredCustomers.slice((state.customersPage - 1) * partiesPageSize, state.customersPage * partiesPageSize);
  if (customerBody) {
    customerBody.innerHTML = filteredCustomers.length
      ? visibleCustomers.map((item) => `
          <tr class="border-b border-[rgba(77,49,29,0.08)]">
            <td class="px-4 py-4">${escapeHtml(item.name || "-")}</td>
            <td class="px-4 py-4">${escapeHtml(item.tax_registration_number || "-")}</td>
            <td class="px-4 py-4">${escapeHtml(accountLabel(item.default_account_code || "-", "-"))}</td>
            <td class="px-4 py-4">${escapeHtml(String(item.payment_terms_days ?? "-"))}</td>
            <td class="px-4 py-4"><button type="button" data-company-party-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
          </tr>
        `).join("")
      : '<tr><td colspan="5" class="px-4 py-6 text-sm text-muted">No customers yet.</td></tr>';
  }
  if (el("customersSearch")) el("customersSearch").value = state.customersSearch || "";
  if (el("customersSort")) el("customersSort").value = state.customersSort || "name_asc";
  if (el("customersPaginationLabel")) {
    el("customersPaginationLabel").textContent = `${filteredCustomers.length} customers • Page ${state.customersPage} of ${customersTotalPages}`;
    el("customersPrevPage").disabled = state.customersPage <= 1;
    el("customersNextPage").disabled = state.customersPage >= customersTotalPages;
  }
  const projectCodeBody = el("companiesProjectCodesTable")?.querySelector("tbody");
  if (projectCodeBody) {
    projectCodeBody.innerHTML = companyProjects.filter((item) => (item.job_code || "").trim()).length
      ? companyProjects.filter((item) => (item.job_code || "").trim()).map((item) => `
          <tr class="border-b border-[rgba(77,49,29,0.08)]">
            <td class="px-4 py-4">${escapeHtml(item.job_code || "-")}</td>
            <td class="px-4 py-4">${escapeHtml(item.name || "-")}</td>
            <td class="px-4 py-4">${escapeHtml(item.project_status || "active")}</td>
            <td class="px-4 py-4"><span class="text-xs text-muted">Manage from Add Project</span></td>
          </tr>
        `).join("")
      : '<tr><td colspan="4" class="px-4 py-6 text-sm text-muted">No project job codes yet. Use Add Project to create them.</td></tr>';
  }
  const costCenterBody = el("companiesCostCentersTable")?.querySelector("tbody");
  if (costCenterBody) {
    costCenterBody.innerHTML = state.costCenterDimensions.length
      ? state.costCenterDimensions.map((item) => `
          <tr class="border-b border-[rgba(77,49,29,0.08)]">
            <td class="px-4 py-4">${escapeHtml(item.code || "-")}</td>
            <td class="px-4 py-4">${escapeHtml(item.name || "-")}</td>
            <td class="px-4 py-4">${item.is_active ? "Active" : "Inactive"}</td>
            <td class="px-4 py-4"><button type="button" data-company-dimension-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
          </tr>
        `).join("")
      : '<tr><td colspan="4" class="px-4 py-6 text-sm text-muted">No cost centers yet.</td></tr>';
  }
  const costCodeBody = el("companiesCostCodesTable")?.querySelector("tbody");
  if (costCodeBody) {
    costCodeBody.innerHTML = state.costCodeDimensions.length
      ? state.costCodeDimensions.map((item) => `
          <tr class="border-b border-[rgba(77,49,29,0.08)]">
            <td class="px-4 py-4">${escapeHtml(item.code || "-")}</td>
            <td class="px-4 py-4">${escapeHtml(item.name || "-")}</td>
            <td class="px-4 py-4">${item.is_active ? "Active" : "Inactive"}</td>
            <td class="px-4 py-4"><button type="button" data-company-dimension-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
          </tr>
        `).join("")
      : '<tr><td colspan="4" class="px-4 py-6 text-sm text-muted">No cost codes yet.</td></tr>';
  }
  if (activeCompanyPane === "finance") {
  const renderAgingSummary = (containerId, payload, noun) => {
    const node = el(containerId);
    if (!node) return;
    const summary = payload?.summary || {};
    const cards = [
      { label: `Total ${noun}`, value: formatMoney(summary.total_amount || 0) },
      { label: "Open Amount", value: formatMoney(summary.open_amount || 0) },
      { label: "Current", value: formatMoney(summary.current || 0) },
      { label: "1-30", value: formatMoney(summary.bucket_1_30 || 0) },
      { label: "31-60", value: formatMoney(summary.bucket_31_60 || 0) },
      { label: "61+", value: formatMoney((summary.bucket_61_90 || 0) + (summary.bucket_over_90 || 0)) },
    ];
    node.innerHTML = cards.map((item) => `
      <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] px-4 py-4">
        <div class="text-[11px] font-semibold uppercase tracking-[0.16em] text-muted">${escapeHtml(item.label)}</div>
        <div class="mt-2 text-lg font-semibold text-ink">${escapeHtml(item.value)}</div>
      </div>
    `).join("");
  };
  const renderTopAgingParties = (containerId, payload) => {
    const node = el(containerId);
    if (!node) return;
    const rows = payload?.top_parties || [];
    if (!rows.length) {
      node.innerHTML = '<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fffaf1] px-4 py-4 text-sm text-muted">No open party balances yet.</div>';
      return;
    }
    node.innerHTML = rows.map((item) => `
      <div class="flex items-center justify-between rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fffaf1] px-4 py-3 text-sm">
        <div>
          <div class="font-semibold text-ink">${escapeHtml(item.party_name || "Unknown")}</div>
          <div class="text-xs text-muted">${escapeHtml(String(item.count || 0))} rows</div>
        </div>
        <div class="text-right">
          <div class="font-semibold text-ink">${formatMoney(item.open_amount || 0)}</div>
          <div class="text-xs text-muted">Total ${formatMoney(item.total_amount || 0)}</div>
        </div>
      </div>
    `).join("");
  };
  const renderAgingTable = (tableId, payload, noun) => {
    const body = el(tableId)?.querySelector("tbody");
    if (!body) return;
    const rows = payload?.rows || [];
    if (!rows.length) {
      body.innerHTML = `<tr><td colspan="6" class="px-4 py-6 text-sm text-muted">No ${noun.toLowerCase()} rows detected yet.</td></tr>`;
      return;
    }
    body.innerHTML = rows.map((item) => `
      <tr class="border-b border-[rgba(77,49,29,0.08)]">
        <td class="px-4 py-4">
          <div class="font-semibold text-ink">${escapeHtml(item.party_name || item.company_name || "Unknown")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.doc_type || "-")} • ${escapeHtml(item.source_file || "-")}</div>
        </td>
        <td class="px-4 py-4">${escapeHtml(item.date || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.due_date || "-")}</td>
        <td class="px-4 py-4">${formatMoney(item.amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.outstanding_amount || 0)}</td>
        <td class="px-4 py-4"><span class="rounded-full px-3 py-1 text-xs font-semibold ${item.status === "open" ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]" : "bg-[rgba(63,115,91,0.12)] text-[#26624c]"}">${escapeHtml(item.status || "-")}</span></td>
      </tr>
    `).join("");
  };
  renderAgingSummary("companiesApSummary", state.apSummary, "Payables");
  renderAgingSummary("companiesArSummary", state.arSummary, "Receivables");
  renderTopAgingParties("companiesApTopParties", state.apSummary);
  renderTopAgingParties("companiesArTopParties", state.arSummary);
  renderAgingTable("companiesApTable", state.apSummary, "payable");
  renderAgingTable("companiesArTable", state.arSummary, "receivable");
  const procurementSummaryNode = el("companiesProcurementSummary");
  const procurementBody = el("companiesProcurementTable")?.querySelector("tbody");
  if (procurementSummaryNode) {
    const summary = state.procurementSummary?.summary || {};
    const cards = [
      { label: "Rows", value: String(summary.rows || 0) },
      { label: "Committed", value: formatMoney(summary.committed_amount || 0) },
      { label: "Received", value: formatMoney(summary.received_amount || 0) },
      { label: "Billed", value: formatMoney(summary.billed_amount || 0) },
      { label: "Paid", value: formatMoney(summary.paid_amount || 0) },
      { label: "Not Received", value: formatMoney(summary.not_received_amount || 0) },
      { label: "Received Not Billed", value: formatMoney(summary.received_not_billed_amount || 0) },
      { label: "Billed Not Paid", value: formatMoney(summary.billed_not_paid_amount || 0) },
      { label: "PO Overrun", value: formatMoney(summary.po_overrun_amount || 0) },
      { label: "Billed Before Received", value: formatMoney(summary.billed_before_received_amount || 0) },
    ];
    procurementSummaryNode.innerHTML = cards.map((item) => `
      <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] px-4 py-4">
        <div class="text-[11px] font-semibold uppercase tracking-[0.16em] text-muted">${escapeHtml(item.label)}</div>
        <div class="mt-2 text-lg font-semibold text-ink">${escapeHtml(item.value)}</div>
      </div>
    `).join("");
  }
  if (procurementBody) {
    const rows = state.procurementSummary?.rows || [];
    procurementBody.innerHTML = rows.length ? rows.map((item) => `
      <tr class="border-b border-[rgba(77,49,29,0.08)]">
        <td class="px-4 py-4">
          <div class="font-semibold text-ink">${escapeHtml(item.project_name || "-")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.project_code || "-")}</div>
        </td>
        <td class="px-4 py-4">${escapeHtml(item.supplier_name || "-")}</td>
        <td class="px-4 py-4">${formatMoney(item.committed_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.received_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.billed_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.paid_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.not_received_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.received_not_billed_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.billed_not_paid_amount || 0)}</td>
        <td class="px-4 py-4"><span class="rounded-full px-3 py-1 text-xs font-semibold ${item.match_flag === "aligned" ? "bg-[rgba(57,112,92,0.12)] text-[#275b4a]" : item.match_flag === "po_overrun" ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]" : "bg-[rgba(217,119,6,0.12)] text-[#9a5b00]"}">${escapeHtml(item.match_flag || "-")}</span></td>
      </tr>
    `).join("") : '<tr><td colspan="10" class="px-4 py-6 text-sm text-muted">No procurement control rows yet.</td></tr>';
  }
  const procurementExceptionsSummaryNode = el("companiesProcurementExceptionsSummary");
  const procurementExceptionsBody = el("companiesProcurementExceptionsTable")?.querySelector("tbody");
  if (procurementExceptionsSummaryNode) {
    const summary = state.procurementExceptions?.summary || {};
    if (el("companiesProcurementExceptionReviewFilter")) {
      el("companiesProcurementExceptionReviewFilter").value = state.procurementExceptionReviewFilter || "";
    }
    if (el("companiesProcurementExceptionMineOnly")) {
      el("companiesProcurementExceptionMineOnly").checked = Boolean(state.procurementExceptionMineOnly);
    }
    const cards = [
      { label: "Total", value: String(summary.total || 0) },
      { label: "Open", value: String(summary.open || 0) },
      { label: "Reviewed", value: String(summary.reviewed || 0) },
      { label: "Ignored", value: String(summary.ignored || 0) },
      { label: "PO Overrun", value: String(summary.po_overrun || 0) },
      { label: "Billed Before Received", value: String(summary.billed_before_received || 0) },
      { label: "Billed Not Paid", value: String(summary.billed_not_paid || 0) },
      { label: "Received Not Billed", value: String(summary.received_not_billed || 0) },
      { label: "Partial Receipt", value: String(summary.partial_receipt || 0) },
    ];
    procurementExceptionsSummaryNode.innerHTML = cards.map((item) => `
      <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] px-4 py-4">
        <div class="text-[11px] font-semibold uppercase tracking-[0.16em] text-muted">${escapeHtml(item.label)}</div>
        <div class="mt-2 text-lg font-semibold text-ink">${escapeHtml(item.value)}</div>
      </div>
    `).join("");
  }
  if (procurementExceptionsBody) {
    const rows = state.procurementExceptions?.rows || [];
    procurementExceptionsBody.innerHTML = rows.length ? rows.map((item) => `
      <tr class="border-b border-[rgba(77,49,29,0.08)] cursor-pointer hover:bg-[#fff8f0]" data-company-procurement-exception-project="${escapeHtml(String(item.project_id || ""))}" data-company-procurement-exception-supplier="${escapeHtml(item.supplier_name || "")}">
        <td class="px-4 py-4">
          <div class="font-semibold text-ink">${escapeHtml(item.project_name || "-")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.project_code || "-")}</div>
        </td>
        <td class="px-4 py-4">${escapeHtml(item.supplier_name || "-")}</td>
        <td class="px-4 py-4"><span class="rounded-full px-3 py-1 text-xs font-semibold ${item.match_flag === "po_overrun" ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]" : "bg-[rgba(217,119,6,0.12)] text-[#9a5b00]"}">${escapeHtml(item.match_flag || "-")}</span></td>
        <td class="px-4 py-4">${formatMoney(item.committed_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.received_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.billed_amount || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.paid_amount || 0)}</td>
        <td class="px-4 py-4">
          <div class="text-xs font-semibold text-ink">${escapeHtml(item.review?.review_state || "open")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.review?.assigned_username || "unassigned")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.review?.note || "")}</div>
        </td>
        <td class="px-4 py-4">
          <div class="flex flex-wrap gap-2">
            <button type="button" data-company-exception-open-project="${escapeHtml(String(item.project_id || ""))}" class="rounded-full bg-[rgba(57,112,92,0.12)] px-3 py-2 text-xs font-semibold text-[#275b4a]">View Project</button>
            <button type="button" data-company-exception-review-bills="${escapeHtml(String(item.project_id || ""))}" data-company-exception-supplier-button="${escapeHtml(item.supplier_name || "")}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Review Bills</button>
            <button type="button" data-company-exception-assign-me="${escapeHtml(String(item.project_id || ""))}" data-company-exception-assign-supplier="${escapeHtml(item.supplier_name || "")}" data-company-exception-assign-flag="${escapeHtml(item.match_flag || "")}" class="rounded-full bg-[rgba(42,99,167,0.12)] px-3 py-2 text-xs font-semibold text-[#1f4b7d]">Assign Me</button>
            <button type="button" data-company-exception-mark-reviewed="${escapeHtml(String(item.project_id || ""))}" data-company-exception-reviewed-supplier="${escapeHtml(item.supplier_name || "")}" data-company-exception-reviewed-flag="${escapeHtml(item.match_flag || "")}" class="rounded-full bg-[rgba(57,112,92,0.12)] px-3 py-2 text-xs font-semibold text-[#275b4a]">Reviewed</button>
            <button type="button" data-company-exception-note="${escapeHtml(String(item.project_id || ""))}" data-company-exception-note-supplier="${escapeHtml(item.supplier_name || "")}" data-company-exception-note-flag="${escapeHtml(item.match_flag || "")}" data-company-exception-current-note="${escapeHtml(item.review?.note || "")}" class="rounded-full bg-[rgba(107,114,128,0.14)] px-3 py-2 text-xs font-semibold text-[#5c6470]">Note</button>
          </div>
        </td>
      </tr>
    `).join("") : '<tr><td colspan="9" class="px-4 py-6 text-sm text-muted">No procurement exceptions are currently open.</td></tr>';
  }
  }
  if (activeCompanyPane === "activity") {
  const companyActivitySummaryNode = el("companiesActivitySummary");
  const companyActivityFeedNode = el("companiesActivityFeed");
  if (companyActivitySummaryNode) {
    const events = state.companyActivityEvents || [];
    const kindCount = (kind) => events.filter((item) => item.kind === kind).length;
    const cards = [
      { label: "Events", value: String(events.length) },
      { label: "Procurement Reviews", value: String(kindCount("procurement_review")) },
      { label: "Allocations", value: String(kindCount("allocation")) },
      { label: "Billing Events", value: String(kindCount("billing_event")) },
      { label: "PO / Receipts", value: String(kindCount("purchase_order") + kindCount("receipt")) },
    ];
    companyActivitySummaryNode.innerHTML = cards.map((item) => `
      <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] px-4 py-4">
        <div class="text-[11px] font-semibold uppercase tracking-[0.16em] text-muted">${escapeHtml(item.label)}</div>
        <div class="mt-2 text-lg font-semibold text-ink">${escapeHtml(item.value)}</div>
      </div>
    `).join("");
  }
  if (companyActivityFeedNode) {
    const events = state.companyActivityEvents || [];
    companyActivityFeedNode.innerHTML = events.length ? events.map((item) => `
      <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] p-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div class="text-xs uppercase tracking-[0.14em] text-muted">${escapeHtml((item.kind || "").replaceAll("_", " "))}</div>
            <div class="mt-1 text-sm font-semibold text-ink">${escapeHtml(item.project_name || item.label || item.reference || item.counterparty || "Company Activity")}</div>
          </div>
          <div class="text-right">
            <div class="text-xs uppercase tracking-[0.14em] text-muted">${escapeHtml(formatDateTime(item.at) || "-")}</div>
            <div class="mt-1 text-xs text-muted">${escapeHtml(item.username || "System")}</div>
          </div>
        </div>
        <div class="mt-3 text-sm leading-6 text-muted">${escapeHtml(item.summary || "-")}</div>
      </div>
    `).join("") : '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-[rgba(255,247,239,0.82)] p-5 text-sm leading-6 text-muted">No company activity tracked yet.</div>';
  }
  }
  if (activeCompanyPane === "costing") {
  const jobSummaryNode = el("companiesJobCostingSummary");
  const jobTableBody = el("companiesJobCostingTable")?.querySelector("tbody");
  const billingProjectSelect = el("companyBillingProjectSelect");
  const poProjectSelect = el("companyPoProjectSelect");
  const poSupplierSelect = el("companyPoSupplierSelect");
  const poCostCodeSelect = el("companyPoCostCode");
  const receiptPoSelect = el("companyReceiptPoSelect");
  if (billingProjectSelect) {
    const currentValue = billingProjectSelect.value;
    billingProjectSelect.innerHTML = '<option value="">Select project</option>';
    companyProjects
      .slice()
      .sort((a, b) => String(a.name || "").localeCompare(String(b.name || "")))
      .forEach((project) => {
        const option = document.createElement("option");
        option.value = String(project.id);
        option.textContent = `${project.name || "-"}${project.job_code ? ` · ${project.job_code}` : ""}`;
        billingProjectSelect.appendChild(option);
      });
    if (currentValue) billingProjectSelect.value = currentValue;
  }
  if (poProjectSelect) {
    const currentValue = poProjectSelect.value;
    poProjectSelect.innerHTML = '<option value="">Select project</option>';
    companyProjects
      .slice()
      .sort((a, b) => String(a.name || "").localeCompare(String(b.name || "")))
      .forEach((project) => {
        const option = document.createElement("option");
        option.value = String(project.id);
        option.textContent = `${project.name || "-"}${project.job_code ? ` · ${project.job_code}` : ""}`;
        poProjectSelect.appendChild(option);
      });
    if (currentValue) poProjectSelect.value = currentValue;
  }
  if (poSupplierSelect) {
    const currentValue = poSupplierSelect.value;
    poSupplierSelect.innerHTML = '<option value="">Select supplier</option>';
    (state.supplierParties || []).forEach((item) => {
      const option = document.createElement("option");
      option.value = String(item.id);
      option.textContent = item.name || "-";
      poSupplierSelect.appendChild(option);
    });
    if (currentValue) poSupplierSelect.value = currentValue;
  }
  if (poCostCodeSelect) {
    const currentValue = poCostCodeSelect.value;
    poCostCodeSelect.innerHTML = '<option value="">Cost code</option>';
    (state.costCodeDimensions || []).forEach((item) => {
      const option = document.createElement("option");
      option.value = item.code || "";
      option.textContent = item.code ? `${item.code} · ${item.name || ""}` : item.name || "";
      poCostCodeSelect.appendChild(option);
    });
    if (currentValue) poCostCodeSelect.value = currentValue;
  }
  if (receiptPoSelect) {
    const currentValue = receiptPoSelect.value;
    receiptPoSelect.innerHTML = '<option value="">Select PO</option>';
    (state.companyPurchaseOrders || []).forEach((item) => {
      const option = document.createElement("option");
      option.value = String(item.id);
      option.textContent = `${item.po_number || `PO-${item.id}`} · ${item.project_name || "-"} · ${formatMoney(item.amount || 0)}`;
      receiptPoSelect.appendChild(option);
    });
    if (currentValue) receiptPoSelect.value = currentValue;
  }
  const billingEventsBody = el("companiesBillingEventsTable")?.querySelector("tbody");
  if (billingEventsBody) {
    const rows = state.companyBillingEvents || [];
    billingEventsBody.innerHTML = rows.length ? rows.map((item) => `
      <tr class="border-b border-[rgba(77,49,29,0.08)]">
        <td class="px-4 py-4">
          <div class="font-semibold text-ink">${escapeHtml(item.project_name || "-")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.project_code || "-")}</div>
        </td>
        <td class="px-4 py-4">${escapeHtml(item.event_type || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.label || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.event_date || "-")}</td>
        <td class="px-4 py-4">${formatMoney(item.amount || 0)}</td>
        <td class="px-4 py-4"><span class="rounded-full px-3 py-1 text-xs font-semibold ${item.status === "draft" ? "bg-[rgba(107,114,128,0.14)] text-[#5c6470]" : item.status === "cancelled" ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]" : "bg-[rgba(57,112,92,0.12)] text-[#275b4a]"}">${escapeHtml(item.status || "-")}</span></td>
        <td class="px-4 py-4"><button type="button" data-company-billing-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
      </tr>
    `).join("") : '<tr><td colspan="7" class="px-4 py-6 text-sm text-muted">No billing events recorded yet.</td></tr>';
  }
  const poBody = el("companiesPoTable")?.querySelector("tbody");
  if (poBody) {
    const rows = state.companyPurchaseOrders || [];
    poBody.innerHTML = rows.length ? rows.map((item) => `
      <tr class="border-b border-[rgba(77,49,29,0.08)]">
        <td class="px-4 py-4">
          <div class="font-semibold text-ink">${escapeHtml(item.project_name || "-")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.project_code || "-")}</div>
        </td>
        <td class="px-4 py-4">${escapeHtml(item.supplier_name || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.po_number || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.cost_code || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.po_date || "-")}</td>
        <td class="px-4 py-4">${formatMoney(item.amount || 0)}</td>
        <td class="px-4 py-4"><span class="rounded-full px-3 py-1 text-xs font-semibold ${item.status === "cancelled" ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]" : item.status === "closed" ? "bg-[rgba(57,112,92,0.12)] text-[#275b4a]" : "bg-[rgba(165,78,45,0.1)] text-emberdark"}">${escapeHtml(item.status || "-")}</span></td>
        <td class="px-4 py-4"><button type="button" data-company-po-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
      </tr>
    `).join("") : '<tr><td colspan="8" class="px-4 py-6 text-sm text-muted">No purchase orders recorded yet.</td></tr>';
  }
  const receiptsBody = el("companiesReceiptsTable")?.querySelector("tbody");
  if (receiptsBody) {
    const rows = state.companyReceipts || [];
    receiptsBody.innerHTML = rows.length ? rows.map((item) => `
      <tr class="border-b border-[rgba(77,49,29,0.08)]">
        <td class="px-4 py-4">
          <div class="font-semibold text-ink">${escapeHtml(item.project_name || "-")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.project_code || "-")}</div>
        </td>
        <td class="px-4 py-4">${escapeHtml(item.po_number || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.receipt_type || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.receipt_number || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.receipt_date || "-")}</td>
        <td class="px-4 py-4">${formatMoney(item.amount || 0)}</td>
        <td class="px-4 py-4"><span class="rounded-full px-3 py-1 text-xs font-semibold ${item.status === "cancelled" ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]" : "bg-[rgba(57,112,92,0.12)] text-[#275b4a]"}">${escapeHtml(item.status || "-")}</span></td>
        <td class="px-4 py-4"><button type="button" data-company-receipt-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
      </tr>
    `).join("") : '<tr><td colspan="8" class="px-4 py-6 text-sm text-muted">No receipts recorded yet.</td></tr>';
  }
  if (jobSummaryNode) {
    const summary = state.jobCostingSummary?.summary || {};
    const cards = [
      { label: "Projects", value: String(summary.projects || 0) },
      { label: "Contract Total", value: formatMoney(summary.contract_total || 0) },
      { label: "Budget", value: formatMoney(summary.budget_total || 0) },
      { label: "Committed Cost", value: formatMoney(summary.committed_cost_total || 0) },
      { label: "Actual Cost", value: formatMoney(summary.actual_cost_total || 0) },
      { label: "Certified Revenue", value: formatMoney(summary.earned_revenue_total || 0) },
      { label: "Billed To Date", value: formatMoney(summary.billed_to_date_total || 0) },
      { label: "Unbilled WIP", value: formatMoney(summary.unbilled_wip_total || 0) },
      { label: "Retention", value: formatMoney(summary.retention_total || 0) },
      { label: "Overbilled", value: formatMoney(summary.overbilled_total || 0) },
      { label: "Gross Margin", value: formatMoney(summary.gross_margin_total || 0) },
    ];
    jobSummaryNode.innerHTML = cards.map((item) => `
      <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] px-4 py-4">
        <div class="text-[11px] font-semibold uppercase tracking-[0.16em] text-muted">${escapeHtml(item.label)}</div>
        <div class="mt-2 text-lg font-semibold text-ink">${escapeHtml(item.value)}</div>
      </div>
    `).join("");
  }
  if (jobTableBody) {
    const rows = state.jobCostingSummary?.rows || [];
    jobTableBody.innerHTML = rows.length ? rows.map((item) => `
      <tr class="border-b border-[rgba(77,49,29,0.08)]">
        <td class="px-4 py-4">
          <div class="font-semibold text-ink">${escapeHtml(item.project_code || "-")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.project_name || "-")} • ${escapeHtml(item.site_name || item.client_name || "-")} • ${escapeHtml(item.contract_number || "-")}</div>
        </td>
        <td class="px-4 py-4">${formatMoney(item.contract_total || 0)}</td>
        <td class="px-4 py-4">${formatMoney(item.budget_amount || 0)}</td>
        <td class="px-4 py-4">
          <div>${formatMoney(item.actual_cost || 0)}</div>
          <div class="text-xs text-muted">Committed ${formatMoney(item.committed_cost || 0)}</div>
        </td>
        <td class="px-4 py-4">
          <div>${formatMoney(item.earned_revenue || 0)}</div>
          <div class="text-xs text-muted">${escapeHtml(String(item.certified_progress_pct || 0))}% certified</div>
        </td>
        <td class="px-4 py-4">
          <div>${formatMoney(item.billed_to_date || 0)}</div>
          <div class="text-xs text-muted">Advance ${formatMoney(item.advance_received || 0)}</div>
        </td>
        <td class="px-4 py-4">
          <div>${formatMoney(item.unbilled_wip || 0)}</div>
          <div class="text-xs text-muted">Over ${formatMoney(item.overbilled_amount || 0)}</div>
        </td>
        <td class="px-4 py-4">${formatMoney(item.retention_amount || 0)}</td>
        <td class="px-4 py-4"><span class="rounded-full px-3 py-1 text-xs font-semibold ${item.billing_status === "underbilled" ? "bg-[rgba(217,119,6,0.12)] text-[#9a5b00]" : item.billing_status === "overbilled" ? "bg-[rgba(42,99,167,0.12)] text-[#1f4b7d]" : "bg-[rgba(57,112,92,0.12)] text-[#275b4a]"}">${escapeHtml(item.billing_status || "aligned")}</span></td>
        <td class="px-4 py-4">
          <div>${formatMoney(item.earned_margin || 0)}</div>
          <div class="text-xs text-muted">Gross ${formatMoney(item.gross_margin || 0)}</div>
        </td>
        <td class="px-4 py-4 text-xs text-muted">${(item.top_cost_codes || []).map((row) => `${escapeHtml(row.cost_code)}: ${formatMoney(row.amount || 0)}`).join(" • ") || "-"}</td>
      </tr>
    `).join("") : '<tr><td colspan="11" class="px-4 py-6 text-sm text-muted">No project costing rows yet. Tag records with project code and cost code to populate this view.</td></tr>';
  }
  const renderCompanyDocTable = (tableId, rows, emptyText) => {
    const body = el(tableId)?.querySelector("tbody");
    if (!body) return;
    if (!rows.length) {
      body.innerHTML = `<tr><td colspan="7" class="px-4 py-6 text-sm text-muted">${escapeHtml(emptyText)}</td></tr>`;
      return;
    }
    body.innerHTML = rows.map((item) => `
      <tr class="border-b border-[rgba(77,49,29,0.08)]">
        <td class="px-4 py-4">
          <div class="font-semibold text-ink">${escapeHtml(item.party_name || item.company_name || "Unknown")}</div>
          <div class="text-xs text-muted">${escapeHtml(item.doc_type || "-")} • ${escapeHtml(item.source_file || "-")}</div>
        </td>
        <td class="px-4 py-4">${escapeHtml(item.date || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(item.due_date || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(accountLabel(item.account_code || item.default_party_account_code || "-", "-"))}</td>
        <td class="px-4 py-4">${escapeHtml(item.project_code || item.cost_center || "-")}</td>
        <td class="px-4 py-4">
          <div>${formatMoney(item.outstanding_amount || 0)}</div>
          <div class="text-xs text-muted">Alloc ${formatMoney(item.allocated_amount || 0)}</div>
        </td>
        <td class="px-4 py-4"><span class="rounded-full px-3 py-1 text-xs font-semibold ${item.status === "open" ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]" : "bg-[rgba(63,115,91,0.12)] text-[#26624c]"}">${escapeHtml(item.status || "-")}</span></td>
      </tr>
    `).join("");
  };
  renderCompanyDocTable("companiesApDocsTable", state.apDocsRows || [], "No supplier bill candidates found.");
  renderCompanyDocTable("companiesArDocsTable", state.arDocsRows || [], "No customer invoice candidates found.");
  if (el("companiesApDocsPageLabel")) {
    el("companiesApDocsPageLabel").textContent = `Page ${state.apDocsPagination.page || 1} of ${state.apDocsPagination.total_pages || 1}`;
    el("companiesApDocsPrev").disabled = (state.apDocsPagination.page || 1) <= 1;
    el("companiesApDocsNext").disabled = (state.apDocsPagination.page || 1) >= (state.apDocsPagination.total_pages || 1);
    el("companiesApDocsSearch").value = state.apDocsSearch || "";
  }
  if (el("companiesArDocsPageLabel")) {
    el("companiesArDocsPageLabel").textContent = `Page ${state.arDocsPagination.page || 1} of ${state.arDocsPagination.total_pages || 1}`;
    el("companiesArDocsPrev").disabled = (state.arDocsPagination.page || 1) <= 1;
    el("companiesArDocsNext").disabled = (state.arDocsPagination.page || 1) >= (state.arDocsPagination.total_pages || 1);
    el("companiesArDocsSearch").value = state.arDocsSearch || "";
  }
  if (el("companyAllocationType")) {
    el("companyAllocationType").value = state.companyAllocationType || "payable";
  }
  const allocationWorkspace = state.companyAllocationWorkspace || { targets: [], payments: [], allocations: [] };
  const targetSelect = el("companyAllocationTargetSelect");
  const paymentSelect = el("companyAllocationPaymentSelect");
  if (targetSelect && paymentSelect) {
    const currentTarget = targetSelect.value;
    const currentPayment = paymentSelect.value;
    targetSelect.innerHTML = '<option value="">Select open target</option>';
    paymentSelect.innerHTML = '<option value="">Select payment</option>';
    (allocationWorkspace.targets || []).forEach((item) => {
      const option = document.createElement("option");
      option.value = String(item.document_id);
      option.textContent = `${item.party_name || item.company_name || "Unknown"} · ${item.date || "-"} · ${formatMoney(item.outstanding_amount || 0)}`;
      targetSelect.appendChild(option);
    });
    (allocationWorkspace.payments || []).forEach((item) => {
      const option = document.createElement("option");
      option.value = String(item.id);
      option.textContent = `${item.company_name || "Unknown"} · ${item.date || "-"} · ${formatMoney(item.remaining_amount || 0)}`;
      paymentSelect.appendChild(option);
    });
    if (currentTarget) targetSelect.value = currentTarget;
    if (currentPayment) paymentSelect.value = currentPayment;
  }
  const renderAllocationList = (containerId, rows, emptyText, valueKey, isHistory = false) => {
    const node = el(containerId);
    if (!node) return;
    if (!rows.length) {
      node.innerHTML = `<div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white px-4 py-4 text-sm text-muted">${escapeHtml(emptyText)}</div>`;
      return;
    }
    node.innerHTML = rows.map((item) => {
      if (isHistory) {
        return `
          <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white px-4 py-3 text-sm">
            <div class="flex items-start justify-between gap-3">
              <div>
                <div class="font-semibold text-ink">${escapeHtml(item.target_label || "Target")} <- ${escapeHtml(item.payment_label || "Payment")}</div>
                <div class="mt-1 text-xs text-muted">${escapeHtml(item.target_date || "-")} • ${escapeHtml(item.payment_date || "-")}</div>
              </div>
              <button type="button" data-company-allocation-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button>
            </div>
            <div class="mt-2 text-sm font-semibold text-ink">${formatMoney(Number(item.amount || 0))}</div>
          </div>
        `;
      }
      return `
        <button type="button" data-company-allocation-select="${valueKey === "payment" ? item.id : item.document_id}" data-company-allocation-kind="${valueKey}" class="block w-full rounded-2xl border border-[rgba(70,43,24,0.12)] bg-white px-4 py-3 text-left text-sm hover:bg-[#fff8f0]">
          <div class="font-semibold text-ink">${escapeHtml(item.party_name || item.company_name || "Unknown")}</div>
          <div class="mt-1 text-xs text-muted">${escapeHtml(item.date || "-")} • ${formatMoney((valueKey === "payment" ? item.remaining_amount : item.outstanding_amount) || 0)}</div>
        </button>
      `;
    }).join("");
  };
  renderAllocationList("companyAllocationTargetsList", allocationWorkspace.targets || [], "No open targets available for allocation.", "target");
  renderAllocationList("companyAllocationPaymentsList", allocationWorkspace.payments || [], "No available payment rows available for allocation.", "payment");
  renderAllocationList("companyAllocationHistoryList", allocationWorkspace.allocations || [], "No allocations created yet.", "history", true);
  }
  if (activeCompanyPane === "projects") {
  const tbody = el("companiesProjectsTable")?.querySelector("tbody");
  if (!tbody) return;
  if (el("companiesProjectsSearch")) {
    el("companiesProjectsSearch").value = state.companyProjectsSearch || "";
  }
  if (el("companiesProjectsStatusFilter")) {
    el("companiesProjectsStatusFilter").value = state.companyProjectsStatusFilter || "";
  }
  tbody.innerHTML = "";
  if (!companyProjects.length) {
    tbody.innerHTML = '<tr><td colspan="4" class="px-4 py-6 text-sm text-muted">No projects linked to the current company yet.</td></tr>';
    return;
  }
  if (!filteredCompanyProjects.length) {
    tbody.innerHTML = '<tr><td colspan="4" class="px-4 py-6 text-sm text-muted">No projects matched the current company filters.</td></tr>';
    return;
  }
  filteredCompanyProjects.forEach((project) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)] cursor-pointer hover:bg-[#fff8f0]";
    tr.dataset.companyProjectId = String(project.id);
    tr.innerHTML = `
      <td class="px-4 py-4">
        <div class="font-semibold text-ink">${escapeHtml(project.name || "-")}</div>
        <div class="text-xs text-muted">${escapeHtml(project.job_code || "-")} • ${escapeHtml(project.project_status || "active")}</div>
      </td>
      <td class="px-4 py-4">${escapeHtml(project.site_name || project.client_name || project.description || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(project.contract_number || "-")}</td>
      <td class="px-4 py-4">
        <div class="flex flex-wrap gap-2">
          <button type="button" data-company-project-view="${project.id}" class="rounded-full bg-[rgba(57,112,92,0.12)] px-3 py-2 text-xs font-semibold text-[#275b4a]">View</button>
          <button type="button" data-company-project-edit="${project.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Edit</button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
  }
}

async function handleCompaniesViewClick(event) {
  const companyView = el("companiesView");
  if (!companyView || !companyView.contains(event.target)) return;

  const button = event.target.closest("button");
  const row = event.target.closest("tr");

  const paneButton = event.target.closest(".company-pane-button");
  if (paneButton) {
    const nextPane = paneButton.dataset.companyPane || "overview";
    if (state.companiesPane === nextPane && isCompanyPaneLoaded(nextPane)) return;
    state.companiesPane = nextPane;
    renderCompaniesWorkspace();
    await ensureCompanyPaneData(state.companiesPane);
    return;
  }

  if (button?.dataset.companyActivate) {
    const companyId = Number(button.dataset.companyActivate || 0);
    if (!companyId) return;
    const response = await fetchJson(`/api/companies/${companyId}/activate`, { method: "POST" });
    if (state.currentUser) {
      state.currentUser.company_id = response.company?.id || companyId;
      state.currentUser.company_name = response.company?.name || state.currentUser.company_name;
    }
    invalidateCompanyPaneCache();
    await runCompanyRenderBatch(async () => {
      await loadCompanyBaseData();
      await ensureCompanyPaneData(state.companiesPane, true);
    });
    return;
  }

  if (button?.dataset.companyPartyDelete) {
    await fetchJson(`/api/companies/current/parties/${button.dataset.companyPartyDelete}`, { method: "DELETE" });
    await Promise.all([loadCompanyParties(), loadCompanyAging(), loadCompanyAllocationWorkspace(), loadCompanyActivity()]);
    return;
  }

  if (button?.dataset.companyDimensionDelete) {
    await fetchJson(`/api/companies/current/dimensions/${button.dataset.companyDimensionDelete}`, { method: "DELETE" });
    await Promise.all([loadCompanyDimensions(), loadCompanyActivity()]);
    renderAccountingFoundation();
    return;
  }

  if (button?.dataset.companyAccountingRuleDelete) {
    await fetchJson(`/api/companies/current/accounting-rules/${button.dataset.companyAccountingRuleDelete}`, { method: "DELETE" });
    await loadCompanyAccountingRules();
    return;
  }

  if (button?.dataset.companyAllocationSelect) {
    if ((button.dataset.companyAllocationKind || "") === "payment") {
      if (el("companyAllocationPaymentSelect")) {
        el("companyAllocationPaymentSelect").value = String(button.dataset.companyAllocationSelect || "");
      }
    } else if (el("companyAllocationTargetSelect")) {
      el("companyAllocationTargetSelect").value = String(button.dataset.companyAllocationSelect || "");
    }
    return;
  }

  if (button?.dataset.companyAllocationDelete) {
    await fetchJson(`/api/companies/current/allocations/${button.dataset.companyAllocationDelete}`, { method: "DELETE" });
    await Promise.all([loadCompanyAging(), loadCompanyApDocuments(), loadCompanyArDocuments(), loadCompanyAllocationWorkspace(), loadCompanyActivity()]);
    return;
  }

  if (button?.dataset.companyBillingDelete) {
    await fetchJson(`/api/companies/current/billing-events/${button.dataset.companyBillingDelete}`, { method: "DELETE" });
    await Promise.all([loadCompanyBillingEvents(), loadCompanyJobCostingSummary(), loadCompanyActivity()]);
    return;
  }

  if (button?.dataset.companyPoDelete) {
    await fetchJson(`/api/companies/current/purchase-orders/${button.dataset.companyPoDelete}`, { method: "DELETE" });
    await Promise.all([loadCompanyPurchaseOrders(), loadCompanyJobCostingSummary(), loadCompanyActivity()]);
    return;
  }

  if (button?.dataset.companyReceiptDelete) {
    await fetchJson(`/api/companies/current/receipts/${button.dataset.companyReceiptDelete}`, { method: "DELETE" });
    await Promise.all([loadCompanyReceipts(), loadCompanyProcurementSummary(), loadCompanyActivity()]);
    return;
  }

  if (button?.dataset.companyProjectView) {
    const project = state.projects.find((item) => item.id === Number(button.dataset.companyProjectView));
    if (project) await openProject(project.id, "overview");
    return;
  }

  if (button?.dataset.companyProjectEdit) {
    const project = state.projects.find((item) => item.id === Number(button.dataset.companyProjectEdit));
    if (!project) return;
    applyProject(project);
    switchView("projectEditor");
    window.scrollTo({ top: 0, behavior: "smooth" });
    return;
  }

  if (button?.dataset.companyExceptionOpenProject) {
    const projectId = Number(button.dataset.companyExceptionOpenProject || 0);
    if (projectId) await openProject(projectId, "overview");
    return;
  }

  if (button?.dataset.companyExceptionReviewBills) {
    const projectId = Number(button.dataset.companyExceptionReviewBills || 0);
    const supplierName = button.dataset.companyExceptionSupplierButton || "";
    if (!projectId) return;
    await openProject(projectId, "tags");
    state.tagsSearch = supplierName;
    renderTags();
    return;
  }

  if (button?.dataset.companyExceptionAssignMe) {
    await updateProcurementExceptionReview({
      projectId: Number(button.dataset.companyExceptionAssignMe || 0),
      supplierName: button.dataset.companyExceptionAssignSupplier || "",
      matchFlag: button.dataset.companyExceptionAssignFlag || "",
      assignedUserId: Number(state.currentUser?.id || 0) || null,
      reviewState: "open",
      note: "",
    });
    return;
  }

  if (button?.dataset.companyExceptionMarkReviewed) {
    await updateProcurementExceptionReview({
      projectId: Number(button.dataset.companyExceptionMarkReviewed || 0),
      supplierName: button.dataset.companyExceptionReviewedSupplier || "",
      matchFlag: button.dataset.companyExceptionReviewedFlag || "",
      assignedUserId: Number(state.currentUser?.id || 0) || null,
      reviewState: "reviewed",
      note: "",
    });
    return;
  }

  if (button?.dataset.companyExceptionNote) {
    const note = window.prompt("Procurement exception note", button.dataset.companyExceptionCurrentNote || "");
    if (note === null) return;
    await updateProcurementExceptionReview({
      projectId: Number(button.dataset.companyExceptionNote || 0),
      supplierName: button.dataset.companyExceptionNoteSupplier || "",
      matchFlag: button.dataset.companyExceptionNoteFlag || "",
      assignedUserId: Number(state.currentUser?.id || 0) || null,
      reviewState: "open",
      note,
    });
    return;
  }

  if (row?.dataset.companyProcurementExceptionProject) {
    const projectId = Number(row.dataset.companyProcurementExceptionProject || 0);
    const supplierName = row.dataset.companyProcurementExceptionSupplier || "";
    if (!projectId) return;
    await openProject(projectId, "tags");
    state.tagsSearch = supplierName;
    renderTags();
    return;
  }

  if (row?.dataset.companyProjectId) {
    const project = state.projects.find((item) => item.id === Number(row.dataset.companyProjectId));
    if (project) await openProject(project.id, "overview");
  }
}

function bindCompaniesViewHandlers() {
  const companyView = el("companiesView");
  if (!companyView || companyView.dataset.handlersBound === "true") return;
  companyView.dataset.handlersBound = "true";
  companyView.addEventListener("click", (event) => {
    handleCompaniesViewClick(event).catch((error) => {
      showSweetAlert("Load Error", error.message, "error");
    });
  });
}

function renderAccountingFoundation() {
  const accountsBody = el("foundationAccountsTable")?.querySelector("tbody");
  const periodsBody = el("foundationPeriodsTable")?.querySelector("tbody");
  const journalBody = el("foundationJournalTable")?.querySelector("tbody");
  const entriesBody = el("foundationEntriesTable")?.querySelector("tbody");
  const trialBalanceBody = el("foundationTrialBalanceTable")?.querySelector("tbody");
  const ledgerBody = el("foundationLedgerTable")?.querySelector("tbody");
  if (!accountsBody || !periodsBody || !journalBody || !entriesBody || !trialBalanceBody || !ledgerBody) return;
  const accounts = state.accountingAccounts || [];
  const periods = state.accountingPeriods || [];
  const drafts = state.journalDrafts || [];
  const entries = state.journalEntries || [];
  const trialBalance = state.trialBalanceRows || [];
  const ledgerRows = state.ledgerRows || [];
  const periodPageSize = 10;
  const draftPageSize = 12;
  const entriesPageSize = 10;
  const ledgerPageSize = 12;
  const periodSearch = (state.accountingPeriodsSearch || "").trim().toLowerCase();
  const filteredPeriods = periods
    .filter((item) => {
      if (state.accountingPeriodsStatusFilter && (item.status || "") !== state.accountingPeriodsStatusFilter) return false;
      if (!periodSearch) return true;
      const haystack = [item.name || "", item.start_date || "", item.end_date || "", item.status || ""].join(" ").toLowerCase();
      return haystack.includes(periodSearch);
    })
    .sort((a, b) => {
      switch (state.accountingPeriodsSort || "start_desc") {
        case "start_asc":
          return (a.start_date || "").localeCompare(b.start_date || "");
        case "name_asc":
          return (a.name || "").localeCompare(b.name || "");
        case "name_desc":
          return (b.name || "").localeCompare(a.name || "");
        default:
          return (b.start_date || "").localeCompare(a.start_date || "");
      }
    });
  const draftSearch = (state.journalDraftsSearch || "").trim().toLowerCase();
  const filteredDrafts = drafts
    .filter((item) => {
      const postingState = item.posting_allowed ? "allowed" : ((item.period_status || "") === "missing" ? "missing" : "blocked");
      if (state.journalDraftsStatusFilter && postingState !== state.journalDraftsStatusFilter) return false;
      if (!draftSearch) return true;
      const haystack = [
        item.date || "",
        item.reference || "",
        item.vendor || "",
        item.memo || "",
        item.amount || "",
        item.period_name || "",
        item.rule_keyword || "",
      ].join(" ").toLowerCase();
      return haystack.includes(draftSearch);
    })
    .sort((a, b) => {
      switch (state.journalDraftsSort || "date_desc") {
        case "date_asc":
          return (a.date || "").localeCompare(b.date || "");
        case "amount_desc":
          return Number(b.amount || 0) - Number(a.amount || 0);
        case "amount_asc":
          return Number(a.amount || 0) - Number(b.amount || 0);
        case "vendor_asc":
          return (a.vendor || "").localeCompare(b.vendor || "");
        default:
          return (b.date || "").localeCompare(a.date || "");
      }
    });
  const periodsTotalPages = Math.max(1, Math.ceil(filteredPeriods.length / periodPageSize));
  const draftsTotalPages = Math.max(1, Math.ceil(filteredDrafts.length / draftPageSize));
  state.accountingPeriodsPage = Math.min(Math.max(1, state.accountingPeriodsPage || 1), periodsTotalPages);
  state.journalDraftsPage = Math.min(Math.max(1, state.journalDraftsPage || 1), draftsTotalPages);
  const visiblePeriods = filteredPeriods.slice((state.accountingPeriodsPage - 1) * periodPageSize, state.accountingPeriodsPage * periodPageSize);
  const visibleDrafts = filteredDrafts.slice((state.journalDraftsPage - 1) * draftPageSize, state.journalDraftsPage * draftPageSize);
  const entriesSearch = (state.journalEntriesSearch || "").trim().toLowerCase();
  const filteredEntries = entries
    .filter((item) => {
      if (state.journalEntriesStatusFilter && (item.status || "") !== state.journalEntriesStatusFilter) return false;
      if (!entriesSearch) return true;
      const haystack = [item.entry_date || "", item.reference || "", item.memo || "", item.status || ""].join(" ").toLowerCase();
      return haystack.includes(entriesSearch);
    })
    .sort((a, b) => {
      switch (state.journalEntriesSort || "date_desc") {
        case "date_asc":
          return (a.entry_date || "").localeCompare(b.entry_date || "");
        case "reference_asc":
          return (a.reference || "").localeCompare(b.reference || "");
        case "reference_desc":
          return (b.reference || "").localeCompare(a.reference || "");
        case "status_asc":
          return (a.status || "").localeCompare(b.status || "");
        default:
          return (b.entry_date || "").localeCompare(a.entry_date || "");
      }
    });
  const entriesTotalPages = Math.max(1, Math.ceil(filteredEntries.length / entriesPageSize));
  state.journalEntriesPage = Math.min(Math.max(1, state.journalEntriesPage || 1), entriesTotalPages);
  const visibleEntries = filteredEntries.slice((state.journalEntriesPage - 1) * entriesPageSize, state.journalEntriesPage * entriesPageSize);
  const ledgerSearch = (state.ledgerSearch || "").trim().toLowerCase();
  const filteredLedgerRows = ledgerRows
    .filter((item) => {
      if (!ledgerSearch) return true;
      const haystack = [
        item.entry_date || "",
        item.reference || "",
        item.memo || "",
        item.project_code || "",
        item.cost_center || "",
        item.debit || "",
        item.credit || "",
        item.balance || "",
      ].join(" ").toLowerCase();
      return haystack.includes(ledgerSearch);
    })
    .sort((a, b) => {
      switch (state.ledgerSort || "date_desc") {
        case "date_asc":
          return (a.entry_date || "").localeCompare(b.entry_date || "");
        case "reference_asc":
          return (a.reference || "").localeCompare(b.reference || "");
        case "reference_desc":
          return (b.reference || "").localeCompare(a.reference || "");
        case "balance_desc":
          return Number(b.balance || 0) - Number(a.balance || 0);
        case "balance_asc":
          return Number(a.balance || 0) - Number(b.balance || 0);
        default:
          return (b.entry_date || "").localeCompare(a.entry_date || "");
      }
    });
  const ledgerTotalPages = Math.max(1, Math.ceil(filteredLedgerRows.length / ledgerPageSize));
  state.ledgerPage = Math.min(Math.max(1, state.ledgerPage || 1), ledgerTotalPages);
  const visibleLedgerRows = filteredLedgerRows.slice((state.ledgerPage - 1) * ledgerPageSize, state.ledgerPage * ledgerPageSize);
  el("foundationCompanyLabel").textContent = `Company book: ${state.currentUser?.company_name || getSelectedProject()?.company_name || "-"}`;
  renderCompaniesWorkspace();
  document.querySelectorAll(".manual-journal-account").forEach((select) => {
    const currentValue = select.value;
    select.innerHTML = '<option value="">Select account</option>';
    accounts.forEach((account) => {
      const option = document.createElement("option");
      option.value = account.code;
      option.textContent = `${account.code} · ${account.name}`;
      select.appendChild(option);
    });
    if (currentValue) select.value = currentValue;
  });
  const activeCompanyId = Number(state.currentUser?.company_id || 0);
  const projectCodeOptions = (state.projects || [])
    .filter((item) => Number(item.company_id || 0) === activeCompanyId && (item.job_code || "").trim())
    .map((item) => ({ code: item.job_code, name: item.name, is_active: true }));
  const costCodeOptions = (state.costCodeDimensions || []).filter((item) => item.is_active);
  const costCenterOptions = (state.costCenterDimensions || []).filter((item) => item.is_active);
  document.querySelectorAll(".manual-journal-project").forEach((select) => {
    const currentValue = select.value;
    select.innerHTML = '<option value="">Select project code</option>';
    projectCodeOptions.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.code;
      option.textContent = item.name ? `${item.code} · ${item.name}` : item.code;
      select.appendChild(option);
    });
    if (currentValue) select.value = currentValue;
  });
  document.querySelectorAll(".manual-journal-cost").forEach((select) => {
    const currentValue = select.value;
    select.innerHTML = '<option value="">Select cost center</option>';
    costCenterOptions.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.code;
      option.textContent = item.name ? `${item.code} · ${item.name}` : item.code;
      select.appendChild(option);
    });
    if (currentValue) select.value = currentValue;
  });
  const projectCodeNode = el("tagProjectCode");
  const costCodeNode = el("tagCostCode");
  const costCenterNode = el("tagCostCenter");
  const purchaseOrderNode = el("tagPurchaseOrderId");
  if (projectCodeNode && costCenterNode && costCodeNode && purchaseOrderNode) {
    const currentProjectCode = projectCodeNode.value;
    const currentCostCode = costCodeNode.value;
    const currentCostCenter = costCenterNode.value;
    const currentPurchaseOrderId = purchaseOrderNode.value;
    projectCodeNode.innerHTML = '<option value="">Select project code</option>';
    costCodeNode.innerHTML = '<option value="">Select cost code</option>';
    costCenterNode.innerHTML = '<option value="">Select cost center</option>';
    purchaseOrderNode.innerHTML = '<option value="">Select purchase order</option>';
    projectCodeOptions.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.code;
      option.textContent = item.name ? `${item.code} · ${item.name}` : item.code;
      projectCodeNode.appendChild(option);
    });
    costCodeOptions.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.code;
      option.textContent = item.name ? `${item.code} · ${item.name}` : item.code;
      costCodeNode.appendChild(option);
    });
    costCenterOptions.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.code;
      option.textContent = item.name ? `${item.code} · ${item.name}` : item.code;
      costCenterNode.appendChild(option);
    });
    (state.companyPurchaseOrders || []).forEach((item) => {
      const option = document.createElement("option");
      option.value = String(item.id);
      option.textContent = `${item.po_number || `PO-${item.id}`} · ${item.project_code || "-"} · ${formatMoney(item.amount || 0)}`;
      purchaseOrderNode.appendChild(option);
    });
    if (currentProjectCode) projectCodeNode.value = currentProjectCode;
    if (currentCostCode) costCodeNode.value = currentCostCode;
    if (currentCostCenter) costCenterNode.value = currentCostCenter;
    if (currentPurchaseOrderId) purchaseOrderNode.value = currentPurchaseOrderId;
  }
  if (el("tagCostCode")) {
    el("tagCostCode").value = el("tagCostCode").value || "";
  }
  if (el("foundationLedgerProjectFilter")) {
    const currentProjectFilter = state.ledgerProjectFilter || "";
    const currentCostFilter = state.ledgerCostCenterFilter || "";
    el("foundationLedgerProjectFilter").innerHTML = '<option value="">All Project Codes</option>';
    el("foundationLedgerCostCenterFilter").innerHTML = '<option value="">All Cost Centers</option>';
    projectCodeOptions.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.code;
      option.textContent = item.name ? `${item.code} · ${item.name}` : item.code;
      el("foundationLedgerProjectFilter").appendChild(option);
    });
    costCenterOptions.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.code;
      option.textContent = item.name ? `${item.code} · ${item.name}` : item.code;
      el("foundationLedgerCostCenterFilter").appendChild(option);
    });
    el("foundationLedgerProjectFilter").value = currentProjectFilter;
    el("foundationLedgerCostCenterFilter").value = currentCostFilter;
  }
  updateManualJournalTotals();
  el("foundationAccountsTotal").textContent = String(accounts.length);
  el("foundationActiveAccounts").textContent = String(accounts.filter((item) => item.is_active).length);
  el("foundationPeriodsTotal").textContent = String(periods.length);
  if (el("foundationPeriodsSearch")) el("foundationPeriodsSearch").value = state.accountingPeriodsSearch || "";
  if (el("foundationPeriodsStatusFilter")) el("foundationPeriodsStatusFilter").value = state.accountingPeriodsStatusFilter || "";
  if (el("foundationPeriodsSort")) el("foundationPeriodsSort").value = state.accountingPeriodsSort || "start_desc";
  if (el("foundationJournalSearch")) el("foundationJournalSearch").value = state.journalDraftsSearch || "";
  if (el("foundationJournalStatusFilter")) el("foundationJournalStatusFilter").value = state.journalDraftsStatusFilter || "";
  if (el("foundationJournalSort")) el("foundationJournalSort").value = state.journalDraftsSort || "date_desc";
  if (el("foundationEntriesSearch")) el("foundationEntriesSearch").value = state.journalEntriesSearch || "";
  if (el("foundationEntriesStatusFilter")) el("foundationEntriesStatusFilter").value = state.journalEntriesStatusFilter || "";
  if (el("foundationEntriesSort")) el("foundationEntriesSort").value = state.journalEntriesSort || "date_desc";
  if (el("foundationLedgerSearch")) el("foundationLedgerSearch").value = state.ledgerSearch || "";
  if (el("foundationLedgerSort")) el("foundationLedgerSort").value = state.ledgerSort || "date_desc";

  if (!accounts.length) {
    accountsBody.innerHTML = '<tr><td colspan="6" class="px-4 py-6 text-sm text-muted">No accounts configured yet. Seed the construction chart or add accounts manually.</td></tr>';
  } else {
    accountsBody.innerHTML = "";
    accounts.forEach((account) => {
      const tr = document.createElement("tr");
      tr.className = "border-b border-[rgba(77,49,29,0.08)]";
      tr.innerHTML = `
        <td class="px-4 py-4">${escapeHtml(account.code)}</td>
        <td class="px-4 py-4">${escapeHtml(account.name)}</td>
        <td class="px-4 py-4">${escapeHtml(account.account_type)}</td>
        <td class="px-4 py-4">${escapeHtml(account.subtype || "-")}</td>
        <td class="px-4 py-4">${account.is_active ? "Active" : "Inactive"}</td>
        <td class="px-4 py-4"><button type="button" data-account-delete="${account.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
      `;
      accountsBody.appendChild(tr);
    });
    accountsBody.querySelectorAll("[data-account-delete]").forEach((button) => {
      button.addEventListener("click", async () => {
        await fetchJson(`/api/companies/current/accounts/${button.dataset.accountDelete}`, { method: "DELETE" });
        await loadAccountingFoundation();
      });
    });
  }

  if (!filteredPeriods.length) {
    periodsBody.innerHTML = '<tr><td colspan="5" class="px-4 py-6 text-sm text-muted">No accounting periods created yet.</td></tr>';
  } else {
    periodsBody.innerHTML = "";
    visiblePeriods.forEach((period) => {
      const tr = document.createElement("tr");
      tr.className = "border-b border-[rgba(77,49,29,0.08)]";
      tr.innerHTML = `
        <td class="px-4 py-4">${escapeHtml(period.name)}</td>
        <td class="px-4 py-4">${escapeHtml(period.start_date || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(period.end_date || "-")}</td>
        <td class="px-4 py-4">
          <select data-period-status="${period.id}" class="rounded-xl border border-[rgba(77,49,29,0.15)] bg-white px-3 py-2 text-xs">
            <option value="open" ${period.status === "open" ? "selected" : ""}>Open</option>
            <option value="closed" ${period.status === "closed" ? "selected" : ""}>Closed</option>
            <option value="locked" ${period.status === "locked" ? "selected" : ""}>Locked</option>
          </select>
        </td>
        <td class="px-4 py-4"><button type="button" data-period-save="${period.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Save</button></td>
      `;
      periodsBody.appendChild(tr);
    });
    periodsBody.querySelectorAll("[data-period-save]").forEach((button) => {
      button.addEventListener("click", async () => {
        const period = periods.find((item) => item.id === Number(button.dataset.periodSave));
        const status = periodsBody.querySelector(`[data-period-status="${button.dataset.periodSave}"]`)?.value || period?.status || "open";
        if (!period) return;
        await fetchJson(`/api/companies/current/periods/${period.id}`, {
          method: "PUT",
          body: JSON.stringify({
            name: period.name,
            start_date: period.start_date,
            end_date: period.end_date,
            status,
          }),
        });
        await loadAccountingFoundation();
      });
    });
  }
  if (el("foundationPeriodsPaginationLabel")) {
    el("foundationPeriodsPaginationLabel").textContent = `${filteredPeriods.length} periods • Page ${state.accountingPeriodsPage} of ${periodsTotalPages}`;
    el("foundationPeriodsPrevPage").disabled = state.accountingPeriodsPage <= 1;
    el("foundationPeriodsNextPage").disabled = state.accountingPeriodsPage >= periodsTotalPages;
  }

  el("foundationJournalSummary").textContent = `${state.journalDraftSummary?.draft_count || 0} drafts • ${formatMoney(state.journalDraftSummary?.posted_amount || 0)} total`;
  if (!filteredDrafts.length) {
    journalBody.innerHTML = '<tr><td colspan="8" class="px-4 py-6 text-sm text-muted">No journal drafts yet. Assign a primary account to tagged records first.</td></tr>';
  } else {
    journalBody.innerHTML = "";
    visibleDrafts.forEach((draft) => {
      const primary = draft.lines.find((item) => item.role === "primary");
      const offset = draft.lines.find((item) => item.role === "offset");
      const periodTone = draft.posting_allowed
        ? "bg-[rgba(57,112,92,0.12)] text-[#275b4a]"
        : "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]";
      const periodLabel = draft.period_name
        ? `${draft.period_name} (${draft.period_status || "open"})`
        : "Missing Period";
      const tr = document.createElement("tr");
      tr.className = "border-b border-[rgba(77,49,29,0.08)]";
      tr.innerHTML = `
        <td class="px-4 py-4">${escapeHtml(draft.date || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(draft.reference || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(draft.vendor || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(draft.amount || "-")}</td>
        <td class="px-4 py-4"><span class="inline-flex rounded-full px-3 py-1 text-xs font-semibold ${periodTone}" title="${escapeHtml(draft.posting_reason || "")}">${escapeHtml(periodLabel)}</span></td>
        <td class="px-4 py-4">${escapeHtml(accountLabel(primary?.account_code || "-", "-"))} ${primary?.debit ? `(Dr ${escapeHtml(primary.debit)})` : `(Cr ${escapeHtml(primary?.credit || "")})`}</td>
        <td class="px-4 py-4">${escapeHtml(accountLabel(offset?.account_code || "-", "-"))} ${offset?.debit ? `(Dr ${escapeHtml(offset.debit)})` : `(Cr ${escapeHtml(offset?.credit || "")})`}</td>
        <td class="px-4 py-4">${escapeHtml(draft.memo || "-")}</td>
      `;
      journalBody.appendChild(tr);
    });
  }
  if (el("foundationJournalPaginationLabel")) {
    el("foundationJournalPaginationLabel").textContent = `${filteredDrafts.length} drafts • Page ${state.journalDraftsPage} of ${draftsTotalPages}`;
    el("foundationJournalPrevPage").disabled = state.journalDraftsPage <= 1;
    el("foundationJournalNextPage").disabled = state.journalDraftsPage >= draftsTotalPages;
  }

  if (!filteredEntries.length) {
    entriesBody.innerHTML = '<tr><td colspan="5" class="px-4 py-6 text-sm text-muted">No posted journal entries yet.</td></tr>';
  } else {
    entriesBody.innerHTML = "";
    visibleEntries.forEach((entry) => {
      const tr = document.createElement("tr");
      tr.className = "border-b border-[rgba(77,49,29,0.08)]";
      tr.innerHTML = `
        <td class="px-4 py-4">${escapeHtml(entry.entry_date || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(entry.reference || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(entry.memo || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(entry.status || "-")}</td>
        <td class="px-4 py-4">${entry.status === "posted" ? `<button type="button" data-entry-unpost="${entry.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Unpost</button>` : "-"}</td>
      `;
      entriesBody.appendChild(tr);
    });
    entriesBody.querySelectorAll("[data-entry-unpost]").forEach((button) => {
      button.addEventListener("click", async () => {
        await fetchJson(`/api/companies/current/journal-entries/${button.dataset.entryUnpost}/unpost`, {
          method: "POST",
        });
        await loadAccountingFoundation();
      });
    });
  }
  if (el("foundationEntriesPaginationLabel")) {
    el("foundationEntriesPaginationLabel").textContent = `${filteredEntries.length} entries • Page ${state.journalEntriesPage} of ${entriesTotalPages}`;
    el("foundationEntriesPrevPage").disabled = state.journalEntriesPage <= 1;
    el("foundationEntriesNextPage").disabled = state.journalEntriesPage >= entriesTotalPages;
  }

  if (!trialBalance.length) {
    trialBalanceBody.innerHTML = '<tr><td colspan="4" class="px-4 py-6 text-sm text-muted">No posted balances yet.</td></tr>';
  } else {
    trialBalanceBody.innerHTML = "";
    trialBalance.forEach((row) => {
      const tr = document.createElement("tr");
      tr.className = `border-b border-[rgba(77,49,29,0.08)] cursor-pointer hover:bg-[#fff8f0] ${state.ledgerAccountCode === row.account_code ? "bg-[#fff3e6]" : ""}`;
      tr.dataset.ledgerAccountCode = row.account_code || "";
      tr.innerHTML = `
        <td class="px-4 py-4">${escapeHtml(accountLabel(row.account_code || "-", "-"))}</td>
        <td class="px-4 py-4">${formatMoney(row.debit || 0)}</td>
        <td class="px-4 py-4">${formatMoney(row.credit || 0)}</td>
        <td class="px-4 py-4">${formatMoney(row.balance || 0)}</td>
      `;
      trialBalanceBody.appendChild(tr);
    });
    trialBalanceBody.querySelectorAll("[data-ledger-account-code]").forEach((row) => {
      row.addEventListener("click", () => {
        loadCompanyLedger(row.dataset.ledgerAccountCode || "");
      });
    });
  }

  el("foundationLedgerTitle").textContent = state.ledgerAccountCode ? `General Ledger · ${accountLabel(state.ledgerAccountCode, state.ledgerAccountCode)}` : "General Ledger";
  el("foundationLedgerSubtitle").textContent = state.ledgerAccountCode
    ? "Posted account activity with running balance."
    : "Click an account in trial balance to inspect posted activity and running balance.";
  el("foundationLedgerSummary").textContent = `${state.ledgerSummary?.count || 0} rows • Ending ${formatMoney(state.ledgerSummary?.ending_balance || 0)}`;
  if (!filteredLedgerRows.length) {
    ledgerBody.innerHTML = '<tr><td colspan="8" class="px-4 py-6 text-sm text-muted">No ledger rows selected yet.</td></tr>';
  } else {
    ledgerBody.innerHTML = "";
    visibleLedgerRows.forEach((row) => {
      const tr = document.createElement("tr");
      tr.className = "border-b border-[rgba(77,49,29,0.08)]";
      tr.innerHTML = `
        <td class="px-4 py-4">${escapeHtml(row.entry_date || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(row.reference || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(row.memo || "-")}</td>
        <td class="px-4 py-4">${formatMoney(row.debit || 0)}</td>
        <td class="px-4 py-4">${formatMoney(row.credit || 0)}</td>
        <td class="px-4 py-4">${formatMoney(row.balance || 0)}</td>
        <td class="px-4 py-4">${escapeHtml(row.project_code || "-")}</td>
        <td class="px-4 py-4">${escapeHtml(row.cost_center || "-")}</td>
      `;
      ledgerBody.appendChild(tr);
    });
  }
  if (el("foundationLedgerPaginationLabel")) {
    el("foundationLedgerPaginationLabel").textContent = `${filteredLedgerRows.length} rows • Page ${state.ledgerPage} of ${ledgerTotalPages}`;
    el("foundationLedgerPrevPage").disabled = state.ledgerPage <= 1;
    el("foundationLedgerNextPage").disabled = state.ledgerPage >= ledgerTotalPages;
  }
}

function manualJournalRows() {
  return Array.from(document.querySelectorAll("#manualJournalTable tbody tr")).map((row) => ({
    account_code: row.querySelector(".manual-journal-account")?.value || "",
    debit: row.querySelector(".manual-journal-debit")?.value.trim() || "",
    credit: row.querySelector(".manual-journal-credit")?.value.trim() || "",
    project_code: row.querySelector(".manual-journal-project")?.value.trim() || "",
    cost_center: row.querySelector(".manual-journal-cost")?.value.trim() || "",
  }));
}

function updateManualJournalTotals() {
  const rows = manualJournalRows();
  let debit = 0;
  let credit = 0;
  rows.forEach((row) => {
    debit += Number(parseFloat(row.debit || "0") || 0);
    credit += Number(parseFloat(row.credit || "0") || 0);
  });
  const balanced = Math.abs(debit - credit) < 0.005;
  el("manualJournalTotals").textContent = `Debit ${formatMoney(debit)} • Credit ${formatMoney(credit)}${balanced ? " • Balanced" : " • Not Balanced"}`;
}

function updateRunAvailability() {
  const button = el("runJob");
  const stopButton = el("stopJob");
  const quickButton = el("projectRunNowButton");
  const hint = el("runHint");
  const hasProject = Boolean(state.selectedProjectId);

  [button, quickButton].forEach((node) => {
    node.disabled = !hasProject;
    node.style.opacity = hasProject ? "1" : "0.55";
    node.style.cursor = hasProject ? "pointer" : "not-allowed";
  });
  stopButton.disabled = !state.jobId;
  stopButton.style.opacity = state.jobId ? "1" : "0.55";
  stopButton.style.cursor = state.jobId ? "pointer" : "not-allowed";

  hint.textContent = hasProject
    ? "Run OCR for the selected project."
    : "Select or create a project to enable processing.";
}

function renderProjectDetail() {
  const project = getSelectedProject();
  const manageSettings = canManageProjectSettings();
  const deleteProject = canDeleteSelectedProject();
  const manageMembers = canManageProjectMembers();
  if (!project) {
    el("projectDetailTitle").textContent = "No project selected";
    el("projectDetailDescription").textContent = "Open a project from the dashboard to manage OCR settings and stored documents.";
    el("overviewProjectName").textContent = "-";
    el("overviewOcrBackend").textContent = "-";
    el("overviewDocumentCount").textContent = "0";
    el("overviewNamingPattern").textContent = emptyProjectSettings().naming_pattern;
    el("projectSettingsSummary").innerHTML = "";
    [el("editProjectButton"), el("editProjectButtonInline"), el("rebuildReconciliationButton"), el("memberSaveButton"), el("deleteProjectButton")].forEach((node) => {
      if (!node) return;
      node.disabled = true;
      node.style.opacity = "0.45";
      node.style.cursor = "not-allowed";
    });
    renderOverviewAnalytics();
    return;
  }

  const settings = { ...emptyProjectSettings(), ...(project.settings || {}) };
  el("projectDetailTitle").textContent = project.name;
  el("projectDetailDescription").textContent = project.description || "Saved OCR workflow";
  el("overviewProjectName").textContent = settings.project_name || project.name;
  el("overviewOcrBackend").textContent = settings.ocr_backend;
  el("overviewDocumentCount").textContent = String(state.documents.length);
  el("overviewNamingPattern").textContent = settings.naming_pattern;
  [el("editProjectButton"), el("editProjectButtonInline"), el("rebuildReconciliationButton")].forEach((node) => {
    if (!node) return;
    node.disabled = !manageSettings;
    node.style.opacity = manageSettings ? "1" : "0.45";
    node.style.cursor = manageSettings ? "pointer" : "not-allowed";
  });
  if (el("memberSaveButton")) {
    el("memberSaveButton").disabled = !manageMembers;
    el("memberSaveButton").style.opacity = manageMembers ? "1" : "0.45";
    el("memberSaveButton").style.cursor = manageMembers ? "pointer" : "not-allowed";
  }
  if (el("deleteProjectButton")) {
    el("deleteProjectButton").disabled = !deleteProject;
    el("deleteProjectButton").style.opacity = deleteProject ? "1" : "0.45";
    el("deleteProjectButton").style.cursor = deleteProject ? "pointer" : "not-allowed";
  }

  const items = [
    ["Source Folder", settings.source_dir || "-"],
    ["Output Folder", settings.output_dir || "-"],
    ["Debug Folder", settings.debug_image_dir || "-"],
    ["Archive Folder", settings.archive_source_dir || "-"],
    ["OCR Profile", settings.ocr_profile],
    ["Handwriting", settings.handwriting_backend],
    ["TrOCR Model", settings.trocr_model],
    ["Export Mode", settings.export_image_mode],
    ["Language", settings.lang],
    ["DPI", String(settings.dpi)],
    ["Video Sample Seconds", String(settings.video_sample_seconds)],
    ["Video Max Frames", String(settings.video_max_frames)],
    ["Excel", settings.excel_name],
    ["Move Processed Source", settings.move_processed_source ? "Enabled" : "Disabled"],
  ];
  el("projectSettingsSummary").innerHTML = items
    .map(
      ([label, value]) => `
        <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] p-4">
          <div class="text-xs uppercase tracking-[0.14em] text-muted">${label}</div>
          <div class="mt-2 break-words text-sm leading-6 text-ink">${value}</div>
        </div>
      `,
    )
    .join("");
  renderOverviewAnalytics();
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(options.headers || {}),
    },
    ...options,
  });
  const rawText = await response.text();
  let payload = null;
  if (rawText) {
    try {
      payload = JSON.parse(rawText);
    } catch {
      payload = null;
    }
  }
  if (!response.ok) {
    const message =
      payload?.detail ||
      payload?.message ||
      rawText ||
      `Request failed (${response.status})`;
    throw new Error(message);
  }
  return payload ?? {};
}

function buildQuery(params) {
  const search = new URLSearchParams();
  Object.entries(params || {}).forEach(([key, value]) => {
    if (value === "" || value === null || value === undefined) return;
    search.set(key, String(value));
  });
  const query = search.toString();
  return query ? `?${query}` : "";
}

async function loadProjectRulesRemote() {
  if (!state.selectedProjectId) {
    state.projectRules = [];
    return;
  }
  let payload = await fetchJson(`/api/projects/${state.selectedProjectId}/rules`);
  let rules = payload.rules || [];
  if (!rules.length) {
    try {
      const seedPayload = await fetchJson(`/api/projects/${state.selectedProjectId}/rules/seed-accounting`, {
        method: "POST",
      });
      if ((seedPayload.created_count || 0) > 0) {
        payload = await fetchJson(`/api/projects/${state.selectedProjectId}/rules`);
        rules = payload.rules || [];
      }
    } catch (error) {
      console.warn("Automatic accounting rule seeding skipped:", error);
    }
  }
  state.projectRules = rules;
}

async function loadVendorAliasesRemote() {
  if (!state.selectedProjectId) {
    state.vendorAliases = {};
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/vendor-aliases`);
  state.vendorAliases = Object.fromEntries((payload.aliases || []).map((item) => [item.normalized_key, item.canonical_name]));
}

function syncRecordTagsFromDocuments() {
  state.recordTags = {};
  state.documents.forEach((item) => {
    state.recordTags[String(item.id)] = {
      category: item.category || "",
      subcategory: item.subcategory || "",
      account_code: item.account_code || "",
      offset_account_code: item.offset_account_code || "",
      cost_code: item.cost_code || "",
      cost_center: item.cost_center || "",
      project_code: item.project_code || "",
      purchase_order_id: item.purchase_order_id || "",
      payment_method: item.payment_method || "",
      vat_flag: Boolean(item.vat_flag),
      canonical_company_name: item.canonical_company_name || "",
    };
  });
}

async function loadDocumentsTable() {
  if (!state.selectedProjectId) {
    state.documentsTableRows = [];
    state.documentsTablePagination = { page: 1, page_size: DOCUMENTS_PAGE_SIZE, total: 0, total_pages: 1 };
    renderDocumentsTable();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/documents${buildQuery({
    page: state.documentsPage,
    page_size: DOCUMENTS_PAGE_SIZE,
    search: state.documentsSearch,
    source_type: state.documentsKindFilter,
    doc_type: state.documentsTypeFilter,
    confidence_label: state.documentsConfidenceFilter,
    match_status: state.documentsMatchFilter,
  })}`);
  state.documentsTableRows = payload.documents || [];
  state.documentsTablePagination = payload.pagination || { page: 1, page_size: DOCUMENTS_PAGE_SIZE, total: 0, total_pages: 1 };
  renderDocumentsTable();
}

async function loadHistoryTable() {
  if (!state.selectedProjectId) {
    state.historyTableRows = [];
    state.historyTablePagination = { page: 1, page_size: HISTORY_PAGE_SIZE, total: 0, total_pages: 1 };
    renderHistoryTable();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/documents${buildQuery({
    page: state.historyPage,
    page_size: HISTORY_PAGE_SIZE,
    search: state.historySearch,
    doc_type: state.historyTypeFilter,
    confidence_label: state.historyConfidenceFilter,
    company: state.historyCompanyFilter,
  })}`);
  state.historyTableRows = payload.documents || [];
  state.historyTablePagination = payload.pagination || { page: 1, page_size: HISTORY_PAGE_SIZE, total: 0, total_pages: 1 };
  renderHistoryTable();
}

async function loadResourcesTable() {
  if (!state.selectedProjectId) {
    state.resourcesRows = [];
    state.resourcesPagination = { page: 1, page_size: RESOURCES_PAGE_SIZE, total: 0, total_pages: 1 };
    state.resourceKindOptions = [];
    state.resourceDetail = null;
    state.resourceDetailRows = [];
    state.resourceDetailPagination = { page: 1, page_size: RESOURCE_DETAIL_PAGE_SIZE, total: 0, total_pages: 1 };
    state.resourceDiagnostics = null;
    renderResources();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/resources${buildQuery({
    page: state.resourcesPage,
    page_size: RESOURCES_PAGE_SIZE,
    search: state.resourcesSearch,
    source_type: state.resourcesKindFilter,
  })}`);
  state.resourcesRows = payload.resources || [];
  state.resourcesPagination = payload.pagination || { page: 1, page_size: RESOURCES_PAGE_SIZE, total: 0, total_pages: 1 };
  state.resourceKindOptions = payload.filters?.source_types || [];
  if (!state.resourcesRows.some((item) => item.key === state.selectedResourceKey)) {
    state.selectedResourceKey = state.resourcesRows[0]?.key || "";
    state.resourceDetailPage = 1;
  }
  renderResources();
  await loadResourceDetail();
}

async function loadResourceDetail() {
  if (!state.selectedProjectId || !state.selectedResourceKey) {
    state.resourceDetail = null;
    state.resourceDetailRows = [];
    state.resourceDetailPagination = { page: 1, page_size: RESOURCE_DETAIL_PAGE_SIZE, total: 0, total_pages: 1 };
    state.resourceDiagnostics = null;
    state.resourceActivity = [];
    state.closeSummary = null;
    renderResourceDetail(null);
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/resource-detail${buildQuery({
    key: state.selectedResourceKey,
    page: state.resourceDetailPage,
    page_size: RESOURCE_DETAIL_PAGE_SIZE,
  })}`);
  state.resourceDetail = payload.resource || null;
  state.resourceDetailRows = payload.records || [];
  state.resourceDetailPagination = payload.pagination || { page: 1, page_size: RESOURCE_DETAIL_PAGE_SIZE, total: 0, total_pages: 1 };
  state.resourceDiagnostics = payload.diagnostics || null;
  state.resourceActivity = payload.activity || [];
  renderResourceDetail(state.resourceDetail);
}

async function loadGlobalSearch() {
  if (!state.selectedProjectId) {
    state.globalSearchRows = [];
    state.globalSearchPagination = { page: 1, page_size: GLOBAL_SEARCH_PAGE_SIZE, total: 0, total_pages: 1 };
    state.globalSearchKindOptions = [];
    renderGlobalSearch();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/documents${buildQuery({
    page: state.globalSearchPage,
    page_size: GLOBAL_SEARCH_PAGE_SIZE,
    search: state.globalSearchQuery,
    source_type: state.globalSearchKindFilter,
    match_status: state.globalSearchStatusFilter,
    confidence_label: state.globalSearchConfidenceFilter,
    mode: "filters",
  })}`);
  state.globalSearchRows = payload.documents || [];
  state.globalSearchPagination = payload.pagination || { page: 1, page_size: GLOBAL_SEARCH_PAGE_SIZE, total: 0, total_pages: 1 };
  state.globalSearchKindOptions = payload.filters?.source_types || [];
  renderGlobalSearch();
}

async function loadCloseSummary() {
  if (!state.selectedProjectId) {
    state.closeSummary = null;
    renderCloseWorkspace();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/close-summary`);
  state.closeSummary = payload;
  renderCloseWorkspace();
}

async function loadAccountingExportOptions() {
  const payload = await fetchJson("/api/accounting-export-options");
  state.accountingExportPresets = payload.presets || [];
  if (!state.accountingExportPreset) {
    state.accountingExportPreset = payload.default_preset || "ultra_force";
  }
  if (!state.accountingExportPresets.some((item) => item.key === state.accountingExportPreset)) {
    state.accountingExportPreset = payload.default_preset || state.accountingExportPresets[0]?.key || "ultra_force";
  }
  renderCloseWorkspace();
}

async function loadReviewComments(documentId) {
  if (!state.selectedProjectId || !documentId) {
    state.reviewComments = [];
    renderReviewComments();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/comments${buildQuery({ document_id: documentId })}`);
  state.reviewComments = payload.comments || [];
  renderReviewComments();
}

async function loadSavedSearches() {
  if (!state.selectedProjectId) {
    state.savedSearches = [];
    renderSavedSearches();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/saved-searches`);
  state.savedSearches = payload.saved_searches || [];
  renderSavedSearches();
}

async function loadProjectMembers() {
  if (!state.selectedProjectId) {
    state.projectMembers = [];
    renderProjectMembers();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/members`);
  state.projectMembers = payload.members || [];
  renderProjectMembers();
}

async function loadAccountingFoundation() {
  if (!state.authToken) {
    state.accountingAccounts = [];
    state.accountingPeriods = [];
    state.journalDrafts = [];
    state.journalDraftSummary = { draft_count: 0, posted_amount: 0 };
    state.journalEntries = [];
    state.trialBalanceRows = [];
    renderAccountingFoundation();
    return;
  }
  const [accountsPayload, periodsPayload, draftsPayload, entriesPayload] = await Promise.all([
    fetchJson(`/api/companies/current/accounts`),
    fetchJson(`/api/companies/current/periods`),
    fetchJson(`/api/companies/current/journal-drafts`),
    fetchJson(`/api/companies/current/journal-entries`),
  ]);
  state.accountingAccounts = accountsPayload.accounts || [];
  state.accountingPeriods = periodsPayload.periods || [];
  state.journalDrafts = draftsPayload.drafts || [];
  state.journalDraftSummary = draftsPayload.summary || { draft_count: 0, posted_amount: 0 };
  state.journalEntries = entriesPayload.entries || [];
  state.trialBalanceRows = entriesPayload.trial_balance || [];
  if (state.ledgerAccountCode) {
    await loadCompanyLedger(state.ledgerAccountCode);
  } else {
    state.ledgerRows = [];
    state.ledgerSummary = { count: 0, ending_balance: 0 };
  }
  renderAccountingFoundation();
}

async function loadCompanyLedger(accountCode) {
  state.ledgerAccountCode = accountCode || "";
  state.ledgerPage = 1;
  if (!state.ledgerAccountCode) {
    state.ledgerRows = [];
    state.ledgerSummary = { count: 0, ending_balance: 0 };
    renderAccountingFoundation();
    return;
  }
  const query = new URLSearchParams({
    account_code: state.ledgerAccountCode,
    project_code: state.ledgerProjectFilter || "",
    cost_center: state.ledgerCostCenterFilter || "",
  });
  const payload = await fetchJson(`/api/companies/current/ledger?${query.toString()}`);
  state.ledgerRows = payload.rows || [];
  state.ledgerSummary = payload.summary || { count: 0, ending_balance: 0 };
  renderAccountingFoundation();
}

async function loadCompanySettings() {
  if (!state.authToken) {
    state.companySettings = null;
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies/current`);
  state.companySettings = payload.company || null;
  requestCompaniesRender();
}

async function loadCompanyAccountingRules() {
  if (!state.authToken) {
    state.companyAccountingRules = [];
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies/current/accounting-rules`);
  state.companyAccountingRules = payload.rules || [];
  requestCompaniesRender();
}

async function loadCompanies() {
  if (!state.authToken) {
    state.companies = [];
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies`);
  state.companies = payload.companies || [];
  requestCompaniesRender();
}

async function loadCompanyParties() {
  if (!state.authToken) {
    state.supplierParties = [];
    state.customerParties = [];
    requestCompaniesRender();
    return;
  }
  const [suppliersPayload, customersPayload] = await Promise.all([
    fetchJson(`/api/companies/current/parties?party_type=supplier`),
    fetchJson(`/api/companies/current/parties?party_type=customer`),
  ]);
  state.supplierParties = suppliersPayload.parties || [];
  state.customerParties = customersPayload.parties || [];
  requestCompaniesRender();
}

async function loadCompanyDimensions() {
  if (!state.authToken) {
    state.projectCodeDimensions = [];
    state.costCenterDimensions = [];
    state.costCodeDimensions = [];
    requestCompaniesRender();
    return;
  }
  const [costsPayload, costCodesPayload] = await Promise.all([
    fetchJson(`/api/companies/current/dimensions?dimension_type=cost_center`),
    fetchJson(`/api/companies/current/dimensions?dimension_type=cost_code`),
  ]);
  state.projectCodeDimensions = [];
  state.costCenterDimensions = costsPayload.dimensions || [];
  state.costCodeDimensions = costCodesPayload.dimensions || [];
  requestCompaniesRender();
}

async function loadCompanyJobCostingSummary() {
  if (!state.authToken) {
    state.jobCostingSummary = null;
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies/current/job-costing-summary`);
  state.jobCostingSummary = payload || null;
  requestCompaniesRender();
}

async function loadCompanyBillingEvents() {
  if (!state.authToken) {
    state.companyBillingEvents = [];
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies/current/billing-events`);
  state.companyBillingEvents = payload.events || [];
  requestCompaniesRender();
}

async function loadCompanyPurchaseOrders() {
  if (!state.authToken) {
    state.companyPurchaseOrders = [];
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies/current/purchase-orders`);
  state.companyPurchaseOrders = payload.orders || [];
  requestCompaniesRender();
}

async function loadCompanyActivity() {
  if (!state.authToken) {
    state.companyActivityEvents = [];
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies/current/activity`);
  state.companyActivityEvents = payload.events || [];
  requestCompaniesRender();
}

async function loadCompanyProcurementSummary() {
  if (!state.authToken) {
    state.procurementSummary = null;
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies/current/procurement-summary`);
  state.procurementSummary = payload || null;
  requestCompaniesRender();
}

async function loadCompanyProcurementExceptions() {
  if (!state.authToken) {
    state.procurementExceptions = null;
    requestCompaniesRender();
    return;
  }
  const params = new URLSearchParams({
    review_state: state.procurementExceptionReviewFilter || "",
    mine_only: state.procurementExceptionMineOnly ? "true" : "false",
  });
  const payload = await fetchJson(`/api/companies/current/procurement-exceptions?${params.toString()}`);
  state.procurementExceptions = payload || null;
  requestCompaniesRender();
}

async function updateProcurementExceptionReview({ projectId, supplierName, matchFlag, assignedUserId, reviewState, note }) {
  await fetchJson(`/api/companies/current/procurement-exceptions/review`, {
    method: "PUT",
    body: JSON.stringify({
      project_id: projectId,
      supplier_name: supplierName,
      match_flag: matchFlag,
      assigned_user_id: assignedUserId,
      review_state: reviewState,
      note: note || "",
    }),
  });
  await Promise.all([loadCompanyProcurementExceptions(), loadCompanyActivity()]);
}

async function loadCompanyReceipts() {
  if (!state.authToken) {
    state.companyReceipts = [];
    requestCompaniesRender();
    return;
  }
  const payload = await fetchJson(`/api/companies/current/receipts`);
  state.companyReceipts = payload.receipts || [];
  requestCompaniesRender();
}

async function loadCompanyAging() {
  if (!state.authToken) {
    state.apSummary = null;
    state.arSummary = null;
    requestCompaniesRender();
    return;
  }
  const [apPayload, arPayload] = await Promise.all([
    fetchJson(`/api/companies/current/ap-summary`),
    fetchJson(`/api/companies/current/ar-summary`),
  ]);
  state.apSummary = apPayload || null;
  state.arSummary = arPayload || null;
  requestCompaniesRender();
}

async function loadCompanyApDocuments() {
  if (!state.authToken) {
    state.apDocsRows = [];
    state.apDocsPagination = { page: 1, page_size: 10, total: 0, total_pages: 1 };
    requestCompaniesRender();
    return;
  }
  const params = new URLSearchParams({
    page: String(state.apDocsPagination.page || 1),
    page_size: String(state.apDocsPagination.page_size || 10),
    query: state.apDocsSearch || "",
  });
  const payload = await fetchJson(`/api/companies/current/ap-documents?${params.toString()}`);
  state.apDocsRows = payload.rows || [];
  state.apDocsPagination = payload.pagination || { page: 1, page_size: 10, total: 0, total_pages: 1 };
  requestCompaniesRender();
}

async function loadCompanyArDocuments() {
  if (!state.authToken) {
    state.arDocsRows = [];
    state.arDocsPagination = { page: 1, page_size: 10, total: 0, total_pages: 1 };
    requestCompaniesRender();
    return;
  }
  const params = new URLSearchParams({
    page: String(state.arDocsPagination.page || 1),
    page_size: String(state.arDocsPagination.page_size || 10),
    query: state.arDocsSearch || "",
  });
  const payload = await fetchJson(`/api/companies/current/ar-documents?${params.toString()}`);
  state.arDocsRows = payload.rows || [];
  state.arDocsPagination = payload.pagination || { page: 1, page_size: 10, total: 0, total_pages: 1 };
  requestCompaniesRender();
}

async function loadCompanyAllocationWorkspace() {
  if (!state.authToken) {
    state.companyAllocationWorkspace = null;
    requestCompaniesRender();
    return;
  }
  const kind = state.companyAllocationType || "payable";
  const payload = await fetchJson(`/api/companies/current/allocation-workspace?allocation_type=${encodeURIComponent(kind)}`);
  state.companyAllocationWorkspace = payload || { targets: [], payments: [], allocations: [] };
  requestCompaniesRender();
}

async function loadEvidenceAttachments(documentId) {
  if (!documentId) {
    state.evidenceAttachments = [];
    state.evidenceSelectedAttachmentId = 0;
    setEvidencePreview("", "Select output or an attachment to preview it here.");
    renderEvidenceAttachments();
    return;
  }
  const payload = await fetchJson(`/api/documents/${documentId}/attachments`);
  state.evidenceAttachments = payload.attachments || [];
  if (!state.evidenceAttachments.some((item) => item.id === state.evidenceSelectedAttachmentId)) {
    state.evidenceSelectedAttachmentId = state.evidenceAttachments[0]?.id || 0;
  }
  renderEvidenceAttachments();
}

async function loadEvidenceAttachmentCounts() {
  if (!state.selectedProjectId) {
    state.evidenceAttachmentCounts = {};
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/attachment-counts`);
  state.evidenceAttachmentCounts = payload.counts || {};
}

async function loadActivityFeed() {
  if (!state.selectedProjectId) {
    state.activityEvents = [];
    renderActivityFeed();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/activity`);
  state.activityEvents = payload.events || [];
  renderActivityFeed();
}

async function pickFile(purpose) {
  const payload = await fetchJson("/api/pick-file", {
    method: "POST",
    body: JSON.stringify({ purpose }),
  });
  return payload.path || "";
}

function replaceDocumentInState(updated) {
  if (!updated?.id) return;
  state.documents = state.documents.map((item) => (item.id === updated.id ? { ...item, ...updated } : item));
  state.documentsTableRows = state.documentsTableRows.map((item) => (item.id === updated.id ? { ...item, ...updated } : item));
  state.historyTableRows = state.historyTableRows.map((item) => (item.id === updated.id ? { ...item, ...updated } : item));
  if (state.resourcesRows.length) {
    state.resourcesRows = state.resourcesRows.map((resource) => ({
      ...resource,
      records: (resource.records || []).map((item) => (item.id === updated.id ? { ...item, ...updated } : item)),
    }));
  }
  invalidateProjectTabs(["overview", "reconciliation", "review", "exceptions", "close", "resources", "documents", "results", "search", "activity", "evidence", "feedback"]);
}

async function loadModels() {
  const payload = await fetchJson("/api/models");
  state.models = payload.models;
  renderModels();
  syncModelRefreshTimer();
}

async function downloadModel(modelName) {
  try {
    showLoading("Downloading Model", "ULTRA FORCE is downloading the selected handwritten OCR model.");
    await fetchJson("/api/models/download", {
      method: "POST",
      body: JSON.stringify({ name: modelName }),
    });
    await loadModels();
    showSweetAlert("Model Download Started", "The model download has started. Refresh the model manager to track progress.", "success");
  } catch (error) {
    showSweetAlert("Model Download Error", error.message, "error");
  } finally {
    hideLoading();
  }
}

async function deleteModel(modelName) {
  const confirmed = await confirmSweetAlert(
    "Remove Model",
    `Remove the downloaded model "${modelName}" from local storage?`,
    "Remove Model",
  );
  if (!confirmed) return;
  try {
    showLoading("Removing Model", "Deleting the downloaded model from local storage.");
    await fetchJson(`/api/models/${encodeURIComponent(modelName)}`, { method: "DELETE" });
    await loadModels();
    showSweetAlert("Model Removed", "The downloaded model was removed.", "success");
  } catch (error) {
    showSweetAlert("Model Remove Error", error.message, "error");
  } finally {
    hideLoading();
  }
}

async function pickFolder(purpose) {
  try {
    showLoading("Opening Folder Picker", "Choose a folder to continue.");
    const payload = await fetchJson("/api/pick-folder", {
      method: "POST",
      body: JSON.stringify({ purpose }),
    });
    if (purpose === "source") el("sourceDir").value = payload.path;
    if (purpose === "output") el("outputDir").value = payload.path;
    if (purpose === "debug") el("debugImageDir").value = payload.path;
    if (purpose === "archive") el("archiveSourceDir").value = payload.path;
  } catch (error) {
    showSweetAlert("Folder Picker Error", error.message, "error");
  } finally {
    hideLoading();
  }
}

function sourceSummary(record) {
  const kind = record.source_type || "pdf";
  const origin = record.source_origin || "";
  return origin ? `${kind} · ${origin}` : kind;
}

function renderJob(job) {
  setStatus(job.status);
  el("logs").textContent = job.logs.join("\n");
  el("resultsMeta").textContent =
    job.status === "completed"
      ? `${job.records.length} records, ${job.generated_files.length} files${job.excel_path ? `, Excel: ${job.excel_path}` : ""}`
      : job.status === "cancelled"
        ? `Run cancelled. ${job.records.length} result rows were produced before stopping.`
      : job.status === "failed"
        ? `Run failed: ${job.error}`
        : "Run in progress.";

  const tbody = el("resultsTable").querySelector("tbody");
  tbody.innerHTML = "";
  job.records.forEach((record) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    tr.innerHTML = `
      <td class="px-4 py-4">${sourceSummary(record)}</td>
      <td class="px-4 py-4">${record.source_timestamp || "-"}</td>
      <td class="px-4 py-4">${fileCell(record.output_file, record.output_file)}</td>
      <td class="px-4 py-4">${record.doc_type}</td>
      <td class="px-4 py-4">${record.date}</td>
      <td class="px-4 py-4">${record.number}</td>
      <td class="px-4 py-4">${escapeHtml(canonicalVendorName(record.company_name))}${reconciliationBadge(record)}</td>
      <td class="px-4 py-4">${record.amount}</td>
      <td class="px-4 py-4">${confidenceBadge(record.confidence_label, record.confidence_score)}</td>
    `;
    tbody.appendChild(tr);
  });
}

function fileLink(path, label) {
  if (!path) return "";
  const href = `/api/file?path=${encodeURIComponent(path)}&token=${encodeURIComponent(state.authToken)}`;
  return `
    <div class="file-cell" data-tooltip="${escapeHtml(path)}">
      <div class="file-actions">
        <a class="file-icon-action" href="${href}" target="_blank" rel="noreferrer" aria-label="Open file" title="Open file">
          <i class="ph ph-arrow-up-right"></i>
        </a>
        <button type="button" class="file-icon-action" data-copy-name="${escapeHtml(label)}" aria-label="Copy file name" title="Copy file name">
          <i class="ph ph-copy"></i>
        </button>
      </div>
      <span class="file-name">${escapeHtml(label)}</span>
    </div>
  `;
}

function fileCell(label, title = "") {
  return `<div class="file-cell" data-tooltip="${escapeHtml(title || label || "")}"><span class="file-name">${escapeHtml(label || "")}</span></div>`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function normalizeCompanyName(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/\b\d+\b/g, " ")
    .replace(/[_#:/\\|()[\]{}.,+-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function canonicalVendorName(value) {
  const normalized = normalizeCompanyName(value);
  return state.vendorAliases[normalized] || String(value || "").trim() || "Unknown";
}

function recordTextHaystack(record) {
  return [
    record.company_name || "",
    record.number || "",
    record.raw_text || "",
    record.source_file || "",
    record.doc_type || "",
  ].join(" ").toLowerCase();
}

function matchingRules(record) {
  const text = recordTextHaystack(record);
  return [...state.projectRules, ...state.companyAccountingRules].filter((rule) => {
    const keyword = String(rule.keyword || "").trim().toLowerCase();
    if (!keyword) return false;
    const sourceOk = !rule.source_type || rule.source_type === record.source_type;
    return sourceOk && text.includes(keyword);
  });
}

function derivedRuleMeta(record) {
  const rules = matchingRules(record);
  const first = rules[0];
  return {
    rules,
    status: first?.status || "",
    category: first?.category || "",
    subcategory: first?.subcategory || "",
    account_code: first?.account_code || "",
    offset_account_code: first?.offset_account_code || "",
    cost_code: first?.cost_code || "",
    cost_center: first?.cost_center || "",
    project_code: first?.project_code || "",
    payment_method: first?.payment_method || "",
    vat_flag: Boolean(first?.vat_flag),
    auto_post: Boolean(first?.auto_post),
  };
}

function recordTagData(record) {
  const manual = state.recordTags[String(record.id)] || {};
  const ruleMeta = derivedRuleMeta(record);
  return {
    category: manual.category || record.category || ruleMeta.category || "",
    subcategory: manual.subcategory || record.subcategory || ruleMeta.subcategory || "",
    account_code: manual.account_code || record.account_code || ruleMeta.account_code || "",
    offset_account_code: manual.offset_account_code || record.offset_account_code || ruleMeta.offset_account_code || "",
    cost_code: manual.cost_code || record.cost_code || ruleMeta.cost_code || "",
    cost_center: manual.cost_center || record.cost_center || ruleMeta.cost_center || "",
    project_code: manual.project_code || record.project_code || ruleMeta.project_code || "",
    purchase_order_id: manual.purchase_order_id || record.purchase_order_id || "",
    payment_method: manual.payment_method || record.payment_method || ruleMeta.payment_method || "",
    vat_flag: Boolean(manual.vat_flag || record.vat_flag || ruleMeta.vat_flag),
  };
}

function showRichTooltip(text, x, y) {
  const tooltip = el("richTooltip");
  tooltip.textContent = text;
  tooltip.classList.remove("hidden");
  const offset = 14;
  const maxX = window.innerWidth - tooltip.offsetWidth - 12;
  const maxY = window.innerHeight - tooltip.offsetHeight - 12;
  tooltip.style.left = `${Math.max(12, Math.min(x + offset, maxX))}px`;
  tooltip.style.top = `${Math.max(12, Math.min(y + offset, maxY))}px`;
}

function hideRichTooltip() {
  el("richTooltip").classList.add("hidden");
}

async function copyToClipboard(value, successText) {
  try {
    await navigator.clipboard.writeText(value);
    showSweetAlert("Copied", successText, "success");
  } catch {
    showSweetAlert("Copy Failed", "Clipboard access was not available.", "error");
  }
}

function exportResults(format) {
  if (!state.selectedProjectId) {
    showSweetAlert("Project Required", "Open a project before exporting previous results.", "error");
    return;
  }
  const href = `/api/projects/${state.selectedProjectId}/export-results?format=${encodeURIComponent(format)}&token=${encodeURIComponent(state.authToken)}`;
  window.open(href, "_blank", "noopener,noreferrer");
}

function exportUnresolvedResults() {
  if (!state.selectedProjectId) {
    showSweetAlert("Project Required", "Open a project before exporting unresolved items.", "error");
    return;
  }
  const href = `/api/projects/${state.selectedProjectId}/export-unresolved?token=${encodeURIComponent(state.authToken)}`;
  window.open(href, "_blank", "noopener,noreferrer");
}

function exportEvidencePack(scope) {
  if (!state.selectedProjectId) {
    showSweetAlert("Project Required", "Open a project before exporting an evidence pack.", "error");
    return;
  }
  const ids = Array.from(state.evidenceSelectedIds).join(",");
  const href =
    `/api/projects/${state.selectedProjectId}/evidence-pack?scope=${encodeURIComponent(scope)}` +
    `&ids=${encodeURIComponent(ids)}&token=${encodeURIComponent(state.authToken)}`;
  window.open(href, "_blank", "noopener,noreferrer");
}

function exportAccountingResults() {
  if (!state.selectedProjectId) {
    showSweetAlert("Project Required", "Open a project before exporting accounting rows.", "error");
    return;
  }
  const href = `/api/projects/${state.selectedProjectId}/export-accounting?preset=${encodeURIComponent(state.accountingExportPreset || "ultra_force")}&token=${encodeURIComponent(state.authToken)}`;
  window.open(href, "_blank", "noopener,noreferrer");
}

function exportClosePackage() {
  if (!state.selectedProjectId) {
    showSweetAlert("Project Required", "Open a project before exporting a close package.", "error");
    return;
  }
  const href = `/api/projects/${state.selectedProjectId}/close-package?preset=${encodeURIComponent(state.accountingExportPreset || "ultra_force")}&token=${encodeURIComponent(state.authToken)}`;
  window.open(href, "_blank", "noopener,noreferrer");
}

function exportCloseAccounting() {
  exportAccountingResults();
}

function exportCloseUnresolved() {
  exportUnresolvedResults();
}

function downloadOutputs(scope) {
  if (!state.selectedProjectId) {
    showSweetAlert("Project Required", "Open a project before downloading output PDFs.", "error");
    return;
  }
  if (scope === "selected" && state.selectedHistoryIds.size === 0) {
    showSweetAlert("Selection Required", "Select one or more previous results first.", "error");
    return;
  }
  const ids = Array.from(state.selectedHistoryIds).join(",");
  const href =
    `/api/projects/${state.selectedProjectId}/download-results?scope=${encodeURIComponent(scope)}` +
    `&ids=${encodeURIComponent(ids)}&token=${encodeURIComponent(state.authToken)}`;
  window.open(href, "_blank", "noopener,noreferrer");
}

function formatDateTime(value) {
  if (!value) return "-";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  const day = String(parsed.getDate()).padStart(2, "0");
  const month = String(parsed.getMonth() + 1).padStart(2, "0");
  const year = parsed.getFullYear();
  return `${day}/${month}/${year}`;
}

function confidenceBadge(label, score) {
  const normalized = label || "low";
  const safeScore = Number.isFinite(Number(score)) ? Number(score) : 0;
  return `<span class="confidence-badge confidence-${normalized}" title="Confidence score: ${safeScore}">${normalized} ${safeScore}</span>`;
}

function reconciliationBadge(record) {
  if (!record || !record.match_status || record.match_status === "candidate" || record.match_status === "unreviewed") {
    return "";
  }
  const status = escapeHtml(record.match_status);
  const score = Number.isFinite(Number(record.match_score)) ? Number(record.match_score) : 0;
  const parts = [record.match_basis || ""];
  if (record.matched_record_company_name || record.matched_record_amount || record.matched_record_number) {
    parts.push(
      [
        record.matched_record_company_name || "",
        record.matched_record_amount || "",
        record.matched_record_number || "",
        record.matched_record_source_timestamp || record.matched_record_date || "",
      ].filter(Boolean).join(" | "),
    );
  }
  const detail = escapeHtml(parts.filter(Boolean).join(" || "));
  const tone =
    record.match_status === "matched" || record.match_status === "linked_to_bank"
      ? "bg-[rgba(64,145,108,0.12)] text-[#2f6f54]"
      : record.match_status === "missing_receipt"
        ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]"
        : "bg-[rgba(107,114,128,0.14)] text-[#5c6470]";
  const canOpenLinked = Boolean(record.id && (record.matched_record_company_name || record.matched_record_number || record.matched_record_amount));
  if (canOpenLinked) {
    return `<div class="mt-2"><button type="button" data-linked-record-id="${record.id}" class="inline-flex rounded-full px-2 py-1 text-[11px] font-semibold ${tone}" title="${detail}">${status}${score ? ` ${score}` : ""}</button></div>`;
  }
  return `<div class="mt-2"><span class="inline-flex rounded-full px-2 py-1 text-[11px] font-semibold ${tone}" title="${detail}">${status}${score ? ` ${score}` : ""}</span></div>`;
}

function attachLinkedRecordHandlers(container) {
  container.querySelectorAll("[data-linked-record-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const record = findRecordById(button.dataset.linkedRecordId);
      if (record) {
        openLinkedRecordModal(record);
      }
    });
  });
}

function explainRecord(record) {
  if (!record) return "-";
  const parts = [];
  const explainability = record.explainability || {};
  const status = explainability.status || dashboardMatchStatus(record) || record.review_state || "unreviewed";
  parts.push(`Status: ${status}.`);
  const matchReasons = explainability.match_reasons || [];
  const matchFactors = explainability.match_factors || [];
  if (matchReasons.length) {
    parts.push(`Reason: ${matchReasons.join("; ")}.`);
  } else if (record.match_basis) {
    parts.push(`Match basis: ${record.match_basis}.`);
  }
  if (matchFactors.length) {
    parts.push(`Factors: ${matchFactors.map((item) => item.label).join("; ")}.`);
  }
  if (explainability.review_note || record.review_note) {
    parts.push(`Review note: ${explainability.review_note || record.review_note}.`);
  }
  const tags = recordTagData(record);
  if (tags.category || tags.subcategory) {
    parts.push(`Tags: ${tags.category || "-"}${tags.subcategory ? ` / ${tags.subcategory}` : ""}.`);
  }
  const provenance = explainability.provenance || record.provenance || {};
  parts.push(`Trace: ${provenance.source_type || record.source_type || "-"} from ${provenance.source_file || record.source_file || "-"} at ${provenance.source_timestamp || record.source_timestamp || record.date || "-"}.`);
  return parts.join(" ");
}

function parserWarningsForRecord(record) {
  if (!record) return [];
  const warnings = record.parser_warnings || record.explainability?.parser_warnings || [];
  const labels = {
    date_unresolved: "date unresolved",
    vendor_unresolved: "vendor unresolved",
    amount_unresolved: "amount unresolved",
    reference_unresolved: "reference unresolved",
    low_confidence_ocr: "low confidence OCR",
    direction_inferred: "direction inferred",
    missing_receipt: "no linked receipt",
  };
  return warnings.map((item) => labels[item] || item.replaceAll("_", " "));
}

function renderReviewComments() {
  const node = el("reviewCommentsList");
  if (!node) return;
  if (!state.reviewComments.length) {
    node.innerHTML = '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-[rgba(255,247,239,0.72)] px-4 py-3 text-sm text-muted">No comments yet.</div>';
    return;
  }
  node.innerHTML = state.reviewComments.map((item) => `
    <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[rgba(255,247,239,0.72)] px-4 py-3">
      <div class="flex items-center justify-between gap-3 text-[11px] uppercase tracking-[0.14em] text-muted">
        <span>${escapeHtml(item.username || "Unknown User")}</span>
        <span>${escapeHtml(formatDateTime(item.created_at))}</span>
      </div>
      <div class="mt-1 text-sm leading-6 text-ink">${escapeHtml(item.body || "")}</div>
    </div>
  `).join("");
}

function renderSavedSearches() {
  const node = el("savedSearchSelect");
  if (!node) return;
  node.innerHTML = '<option value="">Saved Searches</option>';
  state.savedSearches.forEach((item) => {
    const option = document.createElement("option");
    option.value = String(item.id);
    option.textContent = item.name;
    node.appendChild(option);
  });
}

function evidenceFilteredRows() {
  const q = state.evidenceSearch.trim().toLowerCase();
  return state.documents.filter((item) => {
    const attachmentCount = Number(state.evidenceAttachmentCounts[String(item.id)] || 0);
    const matchesQuery = !q || [
      item.source_file,
      item.output_file,
      item.company_name,
      item.number,
      item.amount,
      item.doc_type,
      item.source_type,
    ].join(" ").toLowerCase().includes(q);
    const matchesAttachment =
      !state.evidenceAttachmentFilter
      || (state.evidenceAttachmentFilter === "with_attachments" && attachmentCount > 0)
      || (state.evidenceAttachmentFilter === "without_attachments" && attachmentCount === 0);
    return matchesQuery && matchesAttachment;
  });
}

function renderEvidenceAttachments() {
  const node = el("evidenceAttachmentsList");
  if (!node) return;
  if (!state.evidenceAttachments.length) {
    node.innerHTML = '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-[rgba(255,247,239,0.72)] px-4 py-3 text-sm text-muted">No attachments stored for this document.</div>';
    return;
  }
  node.innerHTML = state.evidenceAttachments.map((item) => `
    <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] ${item.id === state.evidenceSelectedAttachmentId ? "bg-[rgba(165,78,45,0.08)]" : "bg-[rgba(255,247,239,0.72)]"} px-4 py-3">
      <div class="flex items-center justify-between gap-3">
        <div>
          <div class="flex flex-wrap items-center gap-2">
            <div class="text-sm font-semibold text-ink">${escapeHtml(item.label || item.file_name || "Attachment")}</div>
            <span class="inline-flex rounded-full px-2 py-1 text-[11px] font-semibold ${attachmentToneClass(item.attachment_type)}">${escapeHtml(attachmentTypeLabel(item.attachment_type))}</span>
          </div>
          <div class="mt-1 text-xs text-muted">${escapeHtml(item.file_name || "")} • ${escapeHtml(item.username || "Unknown User")}</div>
          <div class="mt-1 text-xs text-muted">${escapeHtml(item.note || "No note")}</div>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" data-attachment-preview="${item.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Preview</button>
          <a class="rounded-full bg-[rgba(57,112,92,0.12)] px-3 py-2 text-xs font-semibold text-[#275b4a]" href="${filePreviewHref(item.file_path)}" target="_blank" rel="noreferrer">Open</a>
          <button type="button" data-attachment-delete="${item.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button>
        </div>
      </div>
    </div>
  `).join("");
  node.querySelectorAll("[data-attachment-preview]").forEach((button) => {
    button.addEventListener("click", () => {
      const attachment = state.evidenceAttachments.find((item) => item.id === Number(button.dataset.attachmentPreview));
      if (!attachment) return;
      state.evidenceSelectedAttachmentId = attachment.id;
      setEvidencePreview(attachment.file_path, `${attachmentTypeLabel(attachment.attachment_type)} • ${attachment.label || attachment.file_name}`);
      renderEvidenceAttachments();
    });
  });
  node.querySelectorAll("[data-attachment-delete]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (!state.evidenceSelectedId) return;
      await fetchJson(`/api/documents/${state.evidenceSelectedId}/attachments/${button.dataset.attachmentDelete}`, { method: "DELETE" });
      await loadEvidenceAttachments(state.evidenceSelectedId);
      renderEvidence();
    });
  });
}

function populateResourceFilters() {
  const node = el("resourcesKindFilter");
  const current = state.resourcesKindFilter;
  node.innerHTML = '<option value="">All Kinds</option>';
  state.resourceKindOptions.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    node.appendChild(option);
  });
  node.value = current;
}

function updateResourcesPagination() {
  const totalPages = state.resourcesPagination.total_pages || 1;
  el("resourcesPageLabel").textContent = `Page ${state.resourcesPagination.page} of ${totalPages}`;
  const totalItems = state.resourcesPagination.total || 0;
  el("resourcesSummary").textContent = `${totalItems} resource${totalItems === 1 ? "" : "s"}`;
  el("resourcesPrevPage").disabled = state.resourcesPagination.page <= 1;
  el("resourcesNextPage").disabled = state.resourcesPagination.page >= totalPages;
  el("resourcesPrevPage").style.opacity = state.resourcesPagination.page <= 1 ? "0.45" : "1";
  el("resourcesNextPage").style.opacity = state.resourcesPagination.page >= totalPages ? "0.45" : "1";
}

function updateResourceDetailPagination(totalItems) {
  const totalPages = Math.max(1, Number(state.resourceDetailPagination?.total_pages || 1));
  const currentPage = Math.max(1, Number(state.resourceDetailPagination?.page || 1));
  el("resourceDetailPageLabel").textContent = `Page ${currentPage} of ${totalPages}`;
  el("resourceDetailSummary").textContent = `${totalItems} record${totalItems === 1 ? "" : "s"}`;
  el("resourceDetailPrevPage").disabled = currentPage <= 1;
  el("resourceDetailNextPage").disabled = currentPage >= totalPages;
  el("resourceDetailPrevPage").style.opacity = currentPage <= 1 ? "0.45" : "1";
  el("resourceDetailNextPage").style.opacity = currentPage >= totalPages ? "0.45" : "1";
}

function renderResourceDetail(resource) {
  const tbody = el("resourceDetailTable").querySelector("tbody");
  const activityNode = el("resourceActivityList");
  tbody.innerHTML = "";
  if (!resource) {
    el("resourceDetailTitle").textContent = "Resource Records";
    el("resourceDetailSubtitle").textContent = "Select a processed source above to inspect its extracted records.";
    updateResourceDetailPagination(0);
    el("resourceDiagnostics").textContent = "No diagnostics available.";
    if (activityNode) activityNode.innerHTML = "No activity available.";
    el("resourceRerunButton").disabled = true;
    el("resourceRerunButton").style.opacity = "0.45";
    tbody.innerHTML = `<tr><td colspan="7" class="px-4 py-6 text-sm text-muted">No resource selected.</td></tr>`;
    return;
  }
  const diagnostics = state.resourceDiagnostics || {};
  const lowConfidenceCount = Number(diagnostics.low_confidence_count || 0);
  const missingReceiptCount = Number(diagnostics.missing_receipt_count || 0);
  const parsingWarnings = Number(diagnostics.parsing_warnings || 0);
  const matchedCount = Number(diagnostics.matched_count || 0);
  const directions = Number(diagnostics.direction_profiles || 0);
  const diagnosticParts = [
    `${lowConfidenceCount} low confidence`,
    `${missingReceiptCount} missing receipt`,
    `${parsingWarnings} parsing warnings`,
    `${matchedCount} matched`,
    `${directions} direction profile${directions === 1 ? "" : "s"}`,
  ];
  const warnings = diagnostics.warnings || [];
  el("resourceDetailTitle").textContent = resource.source_file;
  el("resourceDetailSubtitle").textContent = `${resource.source_type} • ${resource.source_origin} • ${resource.record_count} extracted records • low confidence ${lowConfidenceCount} • missing receipt ${missingReceiptCount} • parsing warnings ${parsingWarnings}`;
  el("resourceDiagnostics").textContent = warnings.length ? `${diagnosticParts.join(" • ")}\nWarnings: ${warnings.join(" • ")}` : diagnosticParts.join(" • ");
  if (activityNode) {
    if (!state.resourceActivity.length) {
      activityNode.innerHTML = "No activity available.";
    } else {
      activityNode.innerHTML = state.resourceActivity.map((item) => `
        <div class="rounded-2xl border border-[rgba(70,43,24,0.10)] bg-[rgba(255,247,239,0.72)] px-4 py-3">
          <div class="flex items-center justify-between gap-3">
            <strong class="text-xs uppercase tracking-[0.14em] text-muted">${escapeHtml(item.kind || "event")}</strong>
            <span class="text-xs text-muted">${escapeHtml(formatDateTime(item.at || ""))}</span>
          </div>
          <div class="mt-1 text-[11px] uppercase tracking-[0.14em] text-muted">${escapeHtml(item.username || "System")}</div>
          <div class="mt-2 text-sm leading-6 text-ink">${escapeHtml(item.summary || "-")}</div>
        </div>
      `).join("");
    }
  }
  el("resourceRerunButton").disabled = !resource.source_path;
  el("resourceRerunButton").style.opacity = resource.source_path ? "1" : "0.45";
  el("resourceRerunButton").dataset.sourcePath = resource.source_path || "";
  updateResourceDetailPagination(Number(state.resourceDetailPagination?.total || 0));
  const rows = state.resourceDetailRows || [];
  if (!rows.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="px-4 py-6 text-sm text-muted">No extracted records for this source.</td></tr>`;
    return;
  }
  rows.forEach((item) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(item.source_timestamp || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.doc_type || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.date || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.number || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(canonicalVendorName(item.company_name) || "-")}${reconciliationBadge(item)}</td>
      <td class="px-4 py-4">${escapeHtml(item.amount || "-")}</td>
      <td class="px-4 py-4">${confidenceBadge(item.confidence_label, item.confidence_score)}</td>
    `;
    tbody.appendChild(tr);
  });
  attachLinkedRecordHandlers(tbody);
}

function effectiveReconciliationStatus(record) {
  const decision = state.reconciliationSessionDecisions[record.id];
  if (decision?.status) {
    return decision.status;
  }
  if (record.review_state && record.review_state !== "unreviewed") {
    return record.review_state;
  }
  return dashboardMatchStatus(record);
}

function reconciliationPriority(record) {
  const status = effectiveReconciliationStatus(record);
  if (status === "missing_receipt") return 0;
  if (status === "matched") return 1;
  if (status === "not_applicable") return 2;
  if (status === "reviewed") return 3;
  return 4;
}

function reconciliationQueueRecords() {
  const query = state.reconciliationSearch.trim().toLowerCase();
  const records = bankTransactionRecords().filter((item) => {
    const bank = bankSheetName(item);
    const status = effectiveReconciliationStatus(item);
    const matchesQuery =
      !query ||
      [
        bank,
        item.date,
        item.number,
        item.company_name,
        item.amount,
        item.match_basis,
        item.raw_text,
      ].join(" ").toLowerCase().includes(query);
    const matchesStatus =
      state.reconciliationStatusFilter === "attention"
        ? resolveTransactionDirection(item) === "debit" && status !== "matched" && status !== "not_applicable" && status !== "reviewed"
        : !state.reconciliationStatusFilter || status === state.reconciliationStatusFilter;
    const matchesBank = !state.reconciliationBankFilter || bank === state.reconciliationBankFilter;
    return matchesQuery && matchesStatus && matchesBank;
  });

  records.sort((a, b) => {
    if (state.reconciliationSort === "amount_desc") {
      return parseAmount(b.amount) - parseAmount(a.amount);
    }
    if (state.reconciliationSort === "date_asc") {
      return String(a.date || "").localeCompare(String(b.date || ""));
    }
    if (state.reconciliationSort === "date_desc") {
      return String(b.date || "").localeCompare(String(a.date || ""));
    }
    return (
      reconciliationPriority(a) - reconciliationPriority(b)
      || parseAmount(b.amount) - parseAmount(a.amount)
      || String(b.date || "").localeCompare(String(a.date || ""))
    );
  });
  return records;
}

function populateReconciliationBankFilter() {
  const node = el("reconciliationBankFilter");
  const current = state.reconciliationBankFilter;
  const banks = [...new Set(state.reconciliationBankOptions || [])].sort();
  node.innerHTML = '<option value="">All Banks / Sheets</option>';
  banks.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    node.appendChild(option);
  });
  node.value = current;
}

function updateReconciliationPagination(totalItems) {
  const totalPages = Math.max(1, Number(state.reconciliationPagination?.total_pages || 1));
  const currentPage = Math.max(1, Number(state.reconciliationPagination?.page || 1));
  el("reconciliationPageLabel").textContent = `Page ${currentPage} of ${totalPages}`;
  el("reconciliationSummary").textContent = `${totalItems} transaction${totalItems === 1 ? "" : "s"}`;
  el("reconciliationPrevPage").disabled = currentPage <= 1;
  el("reconciliationNextPage").disabled = currentPage >= totalPages;
  el("reconciliationPrevPage").style.opacity = currentPage <= 1 ? "0.45" : "1";
  el("reconciliationNextPage").style.opacity = currentPage >= totalPages ? "0.45" : "1";
}

function renderReconciliationDetail(record) {
  const empty = el("reconciliationDetailEmpty");
  const panel = el("reconciliationDetailPanel");
  if (!record) {
    empty.classList.remove("hidden");
    panel.classList.add("hidden");
    el("reconciliationDetailTitle").textContent = "Review Detail";
    el("reconciliationDetailSubtitle").textContent = "Pick a transaction from the queue to inspect and review it.";
    return;
  }
  empty.classList.add("hidden");
  panel.classList.remove("hidden");
  const status = effectiveReconciliationStatus(record);
  const decision = state.reconciliationSessionDecisions[record.id];
  el("reconciliationDetailTitle").textContent = canonicalVendorName(record.company_name) || "Bank Transaction";
  el("reconciliationDetailSubtitle").textContent = `${bankSheetName(record)} • ${record.date || "Unknown date"} • ${record.number || "No reference"}`;
  el("reconciliationDetailStatus").textContent = status || "-";
  el("reconciliationDetailSheet").textContent = bankSheetName(record);
  el("reconciliationDetailDate").textContent = record.date || "-";
  el("reconciliationDetailDirection").textContent = resolveTransactionDirection(record);
  el("reconciliationDetailCompany").textContent = canonicalVendorName(record.company_name) || "-";
  el("reconciliationDetailAmount").textContent = record.amount || "-";
  el("reconciliationDetailReference").textContent = record.number || "-";
  el("reconciliationDetailRawText").textContent = record.raw_text || "No raw OCR text stored.";
  el("reconciliationDetailExplainability").textContent = explainRecord(record);
  el("reconciliationDetailWarnings").textContent = warningsAndConfidenceText(record);
  el("reconciliationDetailTrace").textContent = provenanceText(record);
  el("reconciliationDetailNote").textContent = decision?.note || record.review_note || "No persisted review note yet.";
  const hasLinked = Boolean(record.matched_record_company_name || record.matched_record_number || record.matched_record_amount);
  el("reconciliationOpenLinked").disabled = !hasLinked;
  el("reconciliationOpenLinked").style.opacity = hasLinked ? "1" : "0.45";
}

async function loadReconciliationQueue() {
  if (!state.selectedProjectId) {
    state.reconciliationRows = [];
    state.reconciliationPagination = { page: 1, page_size: RECONCILIATION_PAGE_SIZE, total: 0, total_pages: 1 };
    state.reconciliationSummary = { needs_review_count: 0, missing_amount: 0, reviewed_count: 0 };
    state.reconciliationBankOptions = [];
    renderReconciliationWorkspace();
    return;
  }
  const params = new URLSearchParams({
    search: state.reconciliationSearch,
    status: state.reconciliationStatusFilter,
    bank: state.reconciliationBankFilter,
    sort: state.reconciliationSort,
    page: String(state.reconciliationPage || 1),
    page_size: String(RECONCILIATION_PAGE_SIZE),
  });
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/reconciliation?${params.toString()}`);
  state.reconciliationRows = payload.rows || [];
  state.reconciliationPagination = payload.pagination || { page: 1, page_size: RECONCILIATION_PAGE_SIZE, total: 0, total_pages: 1 };
  state.reconciliationSummary = payload.summary || { needs_review_count: 0, missing_amount: 0, reviewed_count: 0 };
  state.reconciliationBankOptions = payload.filters?.banks || [];
  renderReconciliationWorkspace();
}

function renderReconciliationWorkspace() {
  populateReconciliationBankFilter();
  el("reconciliationNeedsReviewCount").textContent = String(state.reconciliationSummary?.needs_review_count || 0);
  el("reconciliationMissingAmount").textContent = `${formatMoney(state.reconciliationSummary?.missing_amount || 0)} AED`;
  el("reconciliationReviewedCount").textContent = String(state.reconciliationSummary?.reviewed_count || 0);

  const tbody = el("reconciliationTable").querySelector("tbody");
  tbody.innerHTML = "";
  updateReconciliationPagination(Number(state.reconciliationPagination?.total || 0));
  if (!state.selectedProjectId || Number(state.reconciliationPagination?.total || 0) === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="px-4 py-6 text-sm text-muted">No bank transactions are available for reconciliation yet.</td></tr>`;
    renderReconciliationDetail(null);
    return;
  }
  const pageRows = state.reconciliationRows || [];
  if (pageRows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="px-4 py-6 text-sm text-muted">No transactions match the current reconciliation filters.</td></tr>`;
    renderReconciliationDetail(null);
    return;
  }
  if (!pageRows.some((item) => item.id === state.reconciliationSelectedId)) {
    state.reconciliationSelectedId = pageRows[0].id;
  }
  pageRows.forEach((item) => {
    const status = item.effective_status || effectiveReconciliationStatus(item);
    const selected = item.id === state.reconciliationSelectedId;
    const tone =
      status === "missing_receipt"
        ? "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]"
        : status === "matched"
          ? "bg-[rgba(64,145,108,0.12)] text-[#2f6f54]"
          : status === "not_applicable"
            ? "bg-[rgba(217,119,6,0.12)] text-[#9a5b00]"
            : "bg-[rgba(107,114,128,0.14)] text-[#5c6470]";
    const tr = document.createElement("tr");
    tr.className = `border-b border-[rgba(77,49,29,0.08)] ${selected ? "bg-[rgba(165,78,45,0.08)]" : ""}`;
    tr.style.cursor = "pointer";
    tr.innerHTML = `
      <td class="px-4 py-4"><span class="inline-flex rounded-full px-2 py-1 text-[11px] font-semibold ${tone}">${escapeHtml(status || "-")}</span></td>
      <td class="px-4 py-4">${escapeHtml(bankSheetName(item))}</td>
      <td class="px-4 py-4">${escapeHtml(item.date || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(canonicalVendorName(item.company_name) || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.number || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.amount || "-")}</td>
      <td class="px-4 py-4"><button type="button" data-reconciliation-id="${item.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Review</button></td>
    `;
    tr.addEventListener("click", () => {
      state.reconciliationSelectedId = item.id;
      renderReconciliationWorkspace();
    });
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-reconciliation-id]").forEach((button) => {
    button.addEventListener("click", () => {
      state.reconciliationSelectedId = Number(button.dataset.reconciliationId);
      renderReconciliationWorkspace();
    });
  });
  renderReconciliationDetail(pageRows.find((item) => item.id === state.reconciliationSelectedId) || null);
}

function buildReviewIssues() {
  const issues = [];
  const seen = new Map();
  const repeated = new Map();
  const splitCandidates = new Map();
  state.documents.forEach((item) => {
    if (item.confidence_label === "low") {
      issues.push({
        key: `low-${item.id}`,
        type: "low_confidence",
        label: "Low Confidence",
        reason: `Confidence score ${item.confidence_score || 0} on ${item.doc_type || "Unknown"}.`,
        source_type: item.source_type || "-",
        source_file: item.source_file || "-",
        company_name: canonicalVendorName(item.company_name) || "-",
        amount: item.amount || "-",
        record_id: item.id,
      });
    }
    if (!item.date || item.date === "Unknown" || !item.amount || item.amount === "Unknown" || !item.company_name || item.company_name === "Unknown") {
      issues.push({
        key: `parse-${item.id}`,
        type: "parsing_issue",
        label: "Parsing Issue",
        reason: "One or more key extracted fields are missing or unresolved.",
        source_type: item.source_type || "-",
        source_file: item.source_file || "-",
        company_name: canonicalVendorName(item.company_name) || "-",
        amount: item.amount || "-",
        record_id: item.id,
      });
    }
    if (item.source_type === "sheet" && item.doc_type === "BankTransaction" && dashboardMatchStatus(item) === "missing_receipt") {
      issues.push({
        key: `missing-${item.id}`,
        type: "missing_receipt",
        label: "Missing Receipt",
        reason: "Debit bank transaction still has no linked supporting receipt or invoice.",
        source_type: item.source_type || "-",
        source_file: item.source_file || "-",
        company_name: canonicalVendorName(item.company_name) || "-",
        amount: item.amount || "-",
        record_id: item.id,
      });
    }
    const dupKey = [
      item.source_type || "",
      normalizeCompanyName(item.company_name),
      item.date || "",
      String(item.amount || ""),
    ].join("||");
    const repeatedKey = [
      normalizeCompanyName(item.company_name),
      String(item.amount || ""),
    ].join("||");
    const splitKey = [
      normalizeCompanyName(item.company_name),
      item.date || "",
    ].join("||");
    if (normalizeCompanyName(item.company_name) && item.date && item.amount) {
      if (!seen.has(dupKey)) seen.set(dupKey, []);
      seen.get(dupKey).push(item);
    }
    if (normalizeCompanyName(item.company_name) && item.amount) {
      if (!repeated.has(repeatedKey)) repeated.set(repeatedKey, []);
      repeated.get(repeatedKey).push(item);
    }
    if (item.source_type === "sheet" && item.doc_type === "BankTransaction" && normalizeCompanyName(item.company_name) && item.date) {
      if (!splitCandidates.has(splitKey)) splitCandidates.set(splitKey, []);
      splitCandidates.get(splitKey).push(item);
    }
    const raw = `${item.company_name || ""} ${item.raw_text || ""} ${item.number || ""}`.toLowerCase();
    if (/\brefund\b|\breversal\b|\breversed\b|\bchargeback\b/.test(raw)) {
      issues.push({
        key: `refund-${item.id}`,
        type: "refund_or_reversal",
        label: "Refund / Reversal",
        reason: "Record text suggests a refund, reversal, or chargeback that should be reviewed against original spending.",
        source_type: item.source_type || "-",
        source_file: item.source_file || "-",
        company_name: canonicalVendorName(item.company_name) || "-",
        amount: item.amount || "-",
        record_id: item.id,
      });
    }
    if (item.source_type === "sheet" && item.doc_type === "BankTransaction" && resolveTransactionDirection(item) === "credit" && dashboardMatchStatus(item) === "missing_receipt") {
      issues.push({
        key: `credit-misclassified-${item.id}`,
        type: "credit_needs_review",
        label: "Credit Needs Review",
        reason: "Credit transaction is still marked unresolved and may be misclassified or need special handling.",
        source_type: item.source_type || "-",
        source_file: item.source_file || "-",
        company_name: canonicalVendorName(item.company_name) || "-",
        amount: item.amount || "-",
        record_id: item.id,
      });
    }
    if (dashboardMatchStatus(item) === "matched" && item.matched_record_amount && Math.abs(parseAmount(item.amount) - parseAmount(item.matched_record_amount)) > 0.01) {
      issues.push({
        key: `mismatch-${item.id}`,
        type: "amount_mismatch",
        label: "Amount Mismatch",
        reason: `Matched record amount ${item.matched_record_amount} differs from row amount ${item.amount}.`,
        source_type: item.source_type || "-",
        source_file: item.source_file || "-",
        company_name: canonicalVendorName(item.company_name) || "-",
        amount: item.amount || "-",
        record_id: item.id,
      });
    }
  });
  seen.forEach((items, key) => {
    if (items.length > 1) {
      items.forEach((item) => {
        issues.push({
          key: `dup-${key}-${item.id}`,
          type: "duplicate_suspect",
          label: "Duplicate Suspect",
          reason: `${items.length} records share the same normalized vendor, date, and amount.`,
          source_type: item.source_type || "-",
          source_file: item.source_file || "-",
          company_name: canonicalVendorName(item.company_name) || "-",
          amount: item.amount || "-",
          record_id: item.id,
        });
      });
    }
  });
  repeated.forEach((items, key) => {
    const dated = items.filter((item) => item.date && item.date !== "Unknown");
    if (dated.length < 2) return;
    const sorted = [...dated].sort((a, b) => String(a.date || "").localeCompare(String(b.date || "")));
    for (let index = 1; index < sorted.length; index += 1) {
      const prev = sorted[index - 1];
      const curr = sorted[index];
      if (prev.date === curr.date) continue;
      issues.push({
        key: `repeat-${key}-${curr.id}`,
        type: "repeated_charge",
        label: "Repeated Charge",
        reason: `Same normalized vendor and amount appeared again on ${curr.date}; check for subscription, installment, or duplicate charge.`,
        source_type: curr.source_type || "-",
        source_file: curr.source_file || "-",
        company_name: canonicalVendorName(curr.company_name) || "-",
        amount: curr.amount || "-",
        record_id: curr.id,
      });
    }
  });
  splitCandidates.forEach((items) => {
    const debitItems = items.filter((item) => resolveTransactionDirection(item) === "debit");
    if (debitItems.length < 2) return;
    const total = debitItems.reduce((sum, item) => sum + parseAmount(item.amount), 0);
    debitItems.forEach((item) => {
      issues.push({
        key: `split-${item.id}`,
        type: "split_payment_candidate",
        label: "Split Payment Candidate",
        reason: `${debitItems.length} debit rows for the same vendor/date sum to ${formatMoney(total)} AED.`,
        source_type: item.source_type || "-",
        source_file: item.source_file || "-",
        company_name: canonicalVendorName(item.company_name) || "-",
        amount: item.amount || "-",
        record_id: item.id,
      });
    });
  });
  return issues;
}

function filteredReviewIssues() {
  const query = state.reviewQueueSearch.trim().toLowerCase();
  return buildReviewIssues().filter((issue) => {
    const matchesQuery =
      !query ||
      [issue.label, issue.reason, issue.source_file, issue.company_name, issue.amount, issue.source_type].join(" ").toLowerCase().includes(query);
    const matchesType = !state.reviewQueueTypeFilter || issue.type === state.reviewQueueTypeFilter;
    const matchesSource = !state.reviewQueueSourceFilter || issue.source_type === state.reviewQueueSourceFilter;
    return matchesQuery && matchesType && matchesSource;
  });
}

async function loadReviewQueue() {
  if (!state.selectedProjectId) {
    state.reviewQueueRows = [];
    state.reviewQueuePagination = { page: 1, page_size: REVIEW_QUEUE_PAGE_SIZE, total: 0, total_pages: 1 };
    state.reviewQueueSummary = { total: 0, low_confidence: 0, duplicates: 0, parsing: 0 };
    state.reviewQueueSourceOptions = [];
    renderReviewQueue();
    return;
  }
  const params = new URLSearchParams({
    search: state.reviewQueueSearch,
    issue_type: state.reviewQueueTypeFilter,
    source_type: state.reviewQueueSourceFilter,
    page: String(state.reviewQueuePage || 1),
    page_size: String(REVIEW_QUEUE_PAGE_SIZE),
  });
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/review-queue?${params.toString()}`);
  state.reviewQueueRows = payload.rows || [];
  state.reviewQueuePagination = payload.pagination || { page: 1, page_size: REVIEW_QUEUE_PAGE_SIZE, total: 0, total_pages: 1 };
  state.reviewQueueSummary = payload.summary || { total: 0, low_confidence: 0, duplicates: 0, parsing: 0 };
  state.reviewQueueSourceOptions = payload.filters?.source_types || [];
  renderReviewQueue();
}

async function loadExceptions() {
  if (!state.selectedProjectId) {
    state.exceptionsRows = [];
    state.exceptionsPagination = { page: 1, page_size: 12, total: 0, total_pages: 1 };
    state.exceptionsSummary = { total: 0, installments: 0, refund_pairs: 0, split_groups: 0, duplicates: 0, mismatches: 0 };
    renderExceptionsWorkspace();
    return;
  }
  const params = new URLSearchParams({
    search: state.exceptionsSearch,
    case_type: state.exceptionsTypeFilter,
    page: String(state.exceptionsPage || 1),
    page_size: "12",
  });
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/exceptions?${params.toString()}`);
  state.exceptionsRows = payload.rows || [];
  state.exceptionsPagination = payload.pagination || { page: 1, page_size: 12, total: 0, total_pages: 1 };
  state.exceptionsSummary = payload.summary || { total: 0, installments: 0, refund_pairs: 0, split_groups: 0, duplicates: 0, mismatches: 0 };
  renderExceptionsWorkspace();
}

async function loadFeedbackInsights() {
  if (!state.selectedProjectId) {
    state.feedbackInsights = null;
    renderFeedbackWorkspace();
    return;
  }
  const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/feedback-insights`);
  state.feedbackInsights = payload;
  renderFeedbackWorkspace();
}

function renderReviewQueue() {
  const filtered = state.reviewQueueRows || [];
  const tbody = el("reviewQueueTable").querySelector("tbody");
  tbody.innerHTML = "";
  const sourceNode = el("reviewQueueSourceFilter");
  const currentSource = state.reviewQueueSourceFilter;
  const kinds = [...new Set(state.reviewQueueSourceOptions || [])].sort();
  sourceNode.innerHTML = '<option value="">All Source Kinds</option>';
  kinds.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    sourceNode.appendChild(option);
  });
  sourceNode.value = currentSource;
  el("reviewQueueTotal").textContent = String(state.reviewQueueSummary?.total || 0);
  el("reviewQueueLowConfidence").textContent = String(state.reviewQueueSummary?.low_confidence || 0);
  el("reviewQueueDuplicates").textContent = String(state.reviewQueueSummary?.duplicates || 0);
  el("reviewQueueParsing").textContent = String(state.reviewQueueSummary?.parsing || 0);
  const totalPages = Math.max(1, Number(state.reviewQueuePagination?.total_pages || 1));
  const currentPage = Math.max(1, Number(state.reviewQueuePagination?.page || 1));
  el("reviewQueuePageLabel").textContent = `Page ${currentPage} of ${totalPages}`;
  el("reviewQueueSummary").textContent = `${Number(state.reviewQueuePagination?.total || 0)} issue${Number(state.reviewQueuePagination?.total || 0) === 1 ? "" : "s"}`;
  el("reviewQueuePrevPage").disabled = currentPage <= 1;
  el("reviewQueueNextPage").disabled = currentPage >= totalPages;
  el("reviewQueuePrevPage").style.opacity = currentPage <= 1 ? "0.45" : "1";
  el("reviewQueueNextPage").style.opacity = currentPage >= totalPages ? "0.45" : "1";

  const empty = el("reviewDetailEmpty");
  const panel = el("reviewDetailPanel");
  if (Number(state.reviewQueuePagination?.total || 0) === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="px-4 py-6 text-sm text-muted">No issues match the current review queue filters.</td></tr>`;
    empty.classList.remove("hidden");
    panel.classList.add("hidden");
    return;
  }
  if (!filtered.some((item) => item.key === state.reviewQueueSelectedKey)) {
    state.reviewQueueSelectedKey = filtered[0].key;
  }
  filtered.forEach((issue) => {
    const tr = document.createElement("tr");
    tr.className = `border-b border-[rgba(77,49,29,0.08)] ${issue.key === state.reviewQueueSelectedKey ? "bg-[rgba(165,78,45,0.08)]" : ""}`;
    tr.style.cursor = "pointer";
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(issue.label)}</td>
      <td class="px-4 py-4">${escapeHtml(issue.source_type)}</td>
      <td class="px-4 py-4">${escapeHtml(issue.source_file)}</td>
      <td class="px-4 py-4">${escapeHtml(issue.company_name)}</td>
      <td class="px-4 py-4">${escapeHtml(issue.amount)}</td>
      <td class="px-4 py-4">${escapeHtml(memberUsernameById((state.documents.find((item) => item.id === issue.record_id) || {}).assigned_user_id) || "-")}</td>
      <td class="px-4 py-4"><button type="button" data-review-key="${issue.key}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Inspect</button></td>
    `;
    tr.addEventListener("click", () => {
      state.reviewQueueSelectedKey = issue.key;
      renderReviewQueue();
    });
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-review-key]").forEach((button) => {
    button.addEventListener("click", () => {
      state.reviewQueueSelectedKey = button.dataset.reviewKey;
      renderReviewQueue();
    });
  });
  const issue = filtered.find((item) => item.key === state.reviewQueueSelectedKey);
  const record = state.documents.find((item) => item.id === issue?.record_id) || null;
  empty.classList.add("hidden");
  panel.classList.remove("hidden");
  el("reviewDetailTitle").textContent = issue?.label || "Issue Detail";
  el("reviewDetailSubtitle").textContent = issue ? `${issue.source_file} • ${issue.source_type}` : "Pick an issue from the queue to inspect it.";
  el("reviewDetailIssue").textContent = issue?.label || "-";
  el("reviewDetailReason").textContent = issue?.reason || "-";
  el("reviewDetailRecord").textContent = record ? `${record.doc_type || "-"} • ${record.date || "-"} • ${record.number || "-"} • ${canonicalVendorName(record.company_name) || "-"} • ${record.amount || "-"}` : "-";
  el("reviewDetailTrust").textContent = explainRecord(record);
  el("reviewDetailTrace").textContent = record ? (() => {
    return `${provenanceText(record)} | ${confidenceBreakdownText(record)}`;
  })() : "-";
  el("reviewDetailAssignment").textContent = record?.assigned_user_id ? memberUsernameById(record.assigned_user_id) || `User #${record.assigned_user_id}` : "Unassigned";
  el("reviewAssignUser").value = record?.assigned_user_id ? String(record.assigned_user_id) : "";
  el("reviewOpenDocument").disabled = !record?.output_path;
  el("reviewOpenDocument").style.opacity = record?.output_path ? "1" : "0.45";
  el("reviewOpenLinkedDocument").disabled = !(record && (record.matched_record_company_name || record.matched_record_number || record.matched_record_amount));
  el("reviewOpenLinkedDocument").style.opacity = !(record && (record.matched_record_company_name || record.matched_record_number || record.matched_record_amount)) ? "0.45" : "1";
  loadReviewComments(record?.id || 0);
}

function renderExceptionsWorkspace() {
  el("exceptionsTotal").textContent = String(state.exceptionsSummary?.total || 0);
  el("exceptionsInstallments").textContent = String(state.exceptionsSummary?.installments || 0);
  el("exceptionsRefunds").textContent = String(state.exceptionsSummary?.refund_pairs || 0);
  el("exceptionsSplits").textContent = String(state.exceptionsSummary?.split_groups || 0);
  el("exceptionsOther").textContent = String((state.exceptionsSummary?.duplicates || 0) + (state.exceptionsSummary?.mismatches || 0));
  const totalPages = Math.max(1, Number(state.exceptionsPagination?.total_pages || 1));
  const currentPage = Math.max(1, Number(state.exceptionsPagination?.page || 1));
  el("exceptionsPageLabel").textContent = `Page ${currentPage} of ${totalPages}`;
  el("exceptionsSummary").textContent = `${Number(state.exceptionsPagination?.total || 0)} case${Number(state.exceptionsPagination?.total || 0) === 1 ? "" : "s"}`;
  el("exceptionsPrevPage").disabled = currentPage <= 1;
  el("exceptionsNextPage").disabled = currentPage >= totalPages;
  const tbody = el("exceptionsTable").querySelector("tbody");
  tbody.innerHTML = "";
  const empty = el("exceptionsDetailEmpty");
  const panel = el("exceptionsDetailPanel");
  if (!state.exceptionsRows.length) {
    tbody.innerHTML = `<tr><td colspan="5" class="px-4 py-6 text-sm text-muted">No exception cases match the current filters.</td></tr>`;
    empty.classList.remove("hidden");
    panel.classList.add("hidden");
    return;
  }
  if (!state.exceptionsRows.some((item) => item.key === state.exceptionsSelectedKey)) {
    state.exceptionsSelectedKey = state.exceptionsRows[0].key;
  }
  state.exceptionsRows.forEach((item) => {
    const selected = item.key === state.exceptionsSelectedKey;
    const tr = document.createElement("tr");
    tr.className = `border-b border-[rgba(77,49,29,0.08)] ${selected ? "bg-[rgba(165,78,45,0.08)]" : ""}`;
    tr.style.cursor = "pointer";
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(item.label || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.company_name || "-")}</td>
      <td class="px-4 py-4">${formatMoney(item.amount || 0)} AED</td>
      <td class="px-4 py-4">${Array.isArray(item.rows) ? item.rows.length : 0}</td>
      <td class="px-4 py-4"><button type="button" data-exception-key="${escapeHtml(item.key)}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Inspect</button></td>
    `;
    tr.addEventListener("click", () => {
      state.exceptionsSelectedKey = item.key;
      renderExceptionsWorkspace();
    });
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-exception-key]").forEach((button) => {
    button.addEventListener("click", () => {
      state.exceptionsSelectedKey = button.dataset.exceptionKey;
      renderExceptionsWorkspace();
    });
  });
  const item = state.exceptionsRows.find((entry) => entry.key === state.exceptionsSelectedKey);
  if (!item) {
    empty.classList.remove("hidden");
    panel.classList.add("hidden");
    return;
  }
  empty.classList.add("hidden");
  panel.classList.remove("hidden");
  el("exceptionsDetailTitle").textContent = item.label || "Exception Detail";
  el("exceptionsDetailSubtitle").textContent = `${item.company_name || "-"} • ${formatMoney(item.amount || 0)} AED`;
  el("exceptionsDetailReason").textContent = item.reason || "-";
  el("exceptionsDetailRows").innerHTML = (item.rows || []).map((row) => `
    <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] p-4">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="text-sm">${escapeHtml(row.company_name || "-")}</strong>
        <span class="dashboard-amount-pill">${formatMoney(row.amount || 0)} AED</span>
      </div>
      <div class="mt-2 text-xs leading-6 text-muted">${escapeHtml(row.date || "-")} • ${escapeHtml(row.number || "-")} • ${escapeHtml(row.source_file || "-")} • ${escapeHtml(row.match_status || row.review_state || "-")}</div>
    </div>
  `).join("");
}

function renderFeedbackWorkspace() {
  const payload = state.feedbackInsights;
  const aliasNode = el("feedbackAliasList");
  const ruleNode = el("feedbackRuleList");
  if (!aliasNode || !ruleNode) return;
  if (!payload?.summary) {
    el("feedbackReviewedRows").textContent = "0";
    el("feedbackCorrectedRows").textContent = "0";
    el("feedbackAliasCount").textContent = "0";
    el("feedbackRuleCount").textContent = "0";
    aliasNode.innerHTML = '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-white px-4 py-4 text-sm text-muted">Open a project to load feedback suggestions.</div>';
    ruleNode.innerHTML = '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-white px-4 py-4 text-sm text-muted">No rule suggestions available.</div>';
    return;
  }
  el("feedbackReviewedRows").textContent = String(payload.summary.reviewed_rows || 0);
  el("feedbackCorrectedRows").textContent = String(payload.summary.corrected_rows || 0);
  el("feedbackAliasCount").textContent = String(payload.summary.vendor_alias_suggestions || 0);
  el("feedbackRuleCount").textContent = String(payload.summary.rule_suggestions || 0);
  const aliasSuggestions = payload.alias_suggestions || [];
  aliasNode.innerHTML = aliasSuggestions.length ? aliasSuggestions.map((item, index) => `
    <div class="dashboard-list-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="text-sm">${escapeHtml(item.canonical_name)}</strong>
        <span class="dashboard-chip">${item.count} corrections</span>
      </div>
      <div class="mt-2 text-xs leading-6 text-muted">${escapeHtml((item.examples || []).join(" • ") || item.normalized_key)}</div>
      <div class="mt-3">
        <button type="button" data-feedback-alias="${index}" class="rounded-full bg-[rgba(57,112,92,0.12)] px-4 py-2 text-xs font-semibold text-[#275b4a]">Apply Alias</button>
      </div>
    </div>
  `).join("") : '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-white px-4 py-4 text-sm text-muted">No alias suggestions yet.</div>';
  ruleNode.innerHTML = (payload.rule_suggestions || []).length ? payload.rule_suggestions.map((item, index) => `
    <div class="dashboard-list-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="text-sm">${escapeHtml(item.keyword)}</strong>
        <span class="dashboard-chip">${item.count} reviews</span>
      </div>
      <div class="mt-2 text-xs leading-6 text-muted">Status ${escapeHtml(item.status || "-")} • ${escapeHtml((item.examples || []).join(" • ") || item.keyword)}</div>
      <div class="mt-3">
        <button type="button" data-feedback-rule="${index}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-4 py-2 text-xs font-semibold text-emberdark">Create Rule</button>
      </div>
    </div>
  `).join("") : '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-white px-4 py-4 text-sm text-muted">No rule suggestions yet.</div>';
  aliasNode.querySelectorAll("[data-feedback-alias]").forEach((button) => {
    button.addEventListener("click", async () => {
      const item = aliasSuggestions[Number(button.dataset.feedbackAlias)];
      if (!item) return;
      await fetchJson(`/api/projects/${state.selectedProjectId}/feedback-insights/apply`, {
        method: "POST",
        body: JSON.stringify({
          suggestion_type: "vendor_alias",
          normalized_key: item.normalized_key,
          canonical_name: item.canonical_name,
        }),
      });
      await Promise.all([loadFeedbackInsights(), loadVendorAliasesRemote()]);
      renderDocuments(state.documents);
    });
  });
  const ruleSuggestions = payload.rule_suggestions || [];
  ruleNode.querySelectorAll("[data-feedback-rule]").forEach((button) => {
    button.addEventListener("click", async () => {
      const item = ruleSuggestions[Number(button.dataset.feedbackRule)];
      if (!item) return;
      await fetchJson(`/api/projects/${state.selectedProjectId}/feedback-insights/apply`, {
        method: "POST",
        body: JSON.stringify({
          suggestion_type: "project_rule",
          keyword: item.keyword,
          source_type: item.source_type,
          status: item.status,
          category: item.category,
          subcategory: item.subcategory,
        }),
      });
      await Promise.all([loadFeedbackInsights(), loadProjectRulesRemote()]);
      renderDocuments(state.documents);
    });
  });
}

function vendorGroups() {
  const groups = new Map();
  state.documents.forEach((item) => {
    const raw = String(item.company_name || "").trim();
    const normalized = normalizeCompanyName(raw);
    if (!normalized) return;
    if (!groups.has(normalized)) {
      groups.set(normalized, {
        key: normalized,
        canonical: state.vendorAliases[normalized] || raw,
        variants: new Set(),
        count: 0,
      });
    }
    const bucket = groups.get(normalized);
    bucket.canonical = state.vendorAliases[normalized] || bucket.canonical;
    bucket.variants.add(raw);
    bucket.count += 1;
  });
  return Array.from(groups.values())
    .map((item) => ({ ...item, variants: Array.from(item.variants).sort() }))
    .sort((a, b) => b.count - a.count || a.canonical.localeCompare(b.canonical));
}

function renderVendors() {
  const tbody = el("vendorsTable").querySelector("tbody");
  tbody.innerHTML = "";
  const groups = vendorGroups().filter((item) => {
    const q = state.vendorSearch.trim().toLowerCase();
    return !q || [item.canonical, ...item.variants].join(" ").toLowerCase().includes(q);
  });
  const totalPages = Math.max(1, Math.ceil(groups.length / VENDORS_PAGE_SIZE));
  if (state.vendorsPage > totalPages) state.vendorsPage = totalPages;
  el("vendorsPageLabel").textContent = `Page ${state.vendorsPage} of ${totalPages}`;
  el("vendorsSummary").textContent = `${groups.length} vendor group${groups.length === 1 ? "" : "s"}`;
  el("vendorsPrevPage").disabled = state.vendorsPage <= 1;
  el("vendorsNextPage").disabled = state.vendorsPage >= totalPages;
  el("vendorsPrevPage").style.opacity = state.vendorsPage <= 1 ? "0.45" : "1";
  el("vendorsNextPage").style.opacity = state.vendorsPage >= totalPages ? "0.45" : "1";
  if (groups.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" class="px-4 py-6 text-sm text-muted">No vendors match the current filter.</td></tr>`;
    el("vendorDetailEmpty").classList.remove("hidden");
    el("vendorDetailPanel").classList.add("hidden");
    return;
  }
  if (!groups.some((item) => item.key === state.selectedVendorKey)) {
    state.selectedVendorKey = groups[0].key;
  }
  const start = (state.vendorsPage - 1) * VENDORS_PAGE_SIZE;
  groups.slice(start, start + VENDORS_PAGE_SIZE).forEach((group) => {
    const tr = document.createElement("tr");
    tr.className = `border-b border-[rgba(77,49,29,0.08)] ${group.key === state.selectedVendorKey ? "bg-[rgba(165,78,45,0.08)]" : ""}`;
    tr.style.cursor = "pointer";
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(group.canonical)}</td>
      <td class="px-4 py-4">${escapeHtml(group.variants.slice(0, 3).join(", "))}${group.variants.length > 3 ? ` +${group.variants.length - 3}` : ""}</td>
      <td class="px-4 py-4">${group.count}</td>
      <td class="px-4 py-4"><button type="button" data-vendor-key="${group.key}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Manage</button></td>
    `;
    tr.addEventListener("click", () => {
      state.selectedVendorKey = group.key;
      renderVendors();
    });
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-vendor-key]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedVendorKey = button.dataset.vendorKey;
      renderVendors();
    });
  });
  const group = groups.find((item) => item.key === state.selectedVendorKey);
  el("vendorDetailEmpty").classList.add("hidden");
  el("vendorDetailPanel").classList.remove("hidden");
  el("vendorDetailTitle").textContent = group?.canonical || "Vendor Detail";
  el("vendorDetailSubtitle").textContent = group ? `${group.count} records across ${group.variants.length} raw variants` : "Pick a vendor group to review and rename it.";
  el("vendorCanonicalInput").value = group?.canonical || "";
  el("vendorVariantList").textContent = group?.variants.join(" • ") || "-";
}

function renderRules() {
  const tbody = el("rulesTable").querySelector("tbody");
  tbody.innerHTML = "";
  if (state.projectRules.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="px-4 py-6 text-sm text-muted">No rules added for this project yet.</td></tr>`;
    return;
  }
  state.projectRules.forEach((rule) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    const mappedAccountLabel = accountFlowLabel(rule.account_code, rule.offset_account_code);
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(rule.keyword || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(rule.source_type || "Any")}</td>
      <td class="px-4 py-4">${escapeHtml(rule.status || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(rule.category || "-")}${rule.subcategory ? ` / ${escapeHtml(rule.subcategory)}` : ""}</td>
      <td class="px-4 py-4"><div>${escapeHtml(mappedAccountLabel)}</div><div class="text-xs text-muted">${escapeHtml(rule.payment_method || "")}${rule.auto_post ? " • auto" : ""}</div></td>
      <td class="px-4 py-4"><button type="button" data-rule-delete="${rule.id}" class="rounded-full bg-[rgba(180,58,58,0.12)] px-3 py-2 text-xs font-semibold text-[#8f2b2b]">Delete</button></td>
    `;
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-rule-delete]").forEach((button) => {
    button.addEventListener("click", async () => {
      const ruleId = Number(button.dataset.ruleDelete);
      await fetchJson(`/api/projects/${state.selectedProjectId}/rules/${ruleId}`, { method: "DELETE" });
      state.projectRules = state.projectRules.filter((item) => item.id !== ruleId);
      renderRules();
      renderDocuments(state.documents);
    });
  });
}

function filteredTagRecords() {
  const q = state.tagsSearch.trim().toLowerCase();
  return state.documents.filter((item) => {
    const matchesQuery =
      !q ||
      [
        canonicalVendorName(item.company_name),
        item.number,
        item.amount,
        item.source_type,
        recordTagData(item).category,
        recordTagData(item).subcategory,
      ].join(" ").toLowerCase().includes(q);
    const matchesSource = !state.tagsSourceFilter || item.source_type === state.tagsSourceFilter;
    return matchesQuery && matchesSource;
  });
}

function renderTags() {
  const tbody = el("tagsTable").querySelector("tbody");
  tbody.innerHTML = "";
  const sourceNode = el("tagsSourceFilter");
  const accountNode = el("tagAccountCode");
  const offsetNode = el("tagOffsetAccountCode");
  const current = state.tagsSourceFilter;
  const kinds = [...new Set(state.documents.map((item) => item.source_type).filter(Boolean))].sort();
  sourceNode.innerHTML = '<option value="">All Kinds</option>';
  kinds.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    sourceNode.appendChild(option);
  });
  sourceNode.value = current;
  if (accountNode && offsetNode) {
    const currentAccount = accountNode.value;
    const currentOffset = offsetNode.value;
    accountNode.innerHTML = '<option value="">Select account</option>';
    offsetNode.innerHTML = '<option value="">Auto / default</option>';
    state.accountingAccounts.forEach((item) => {
      const label = `${item.code} - ${item.name}`;
      const optionA = document.createElement("option");
      optionA.value = item.code;
      optionA.textContent = label;
      accountNode.appendChild(optionA);
      const optionB = document.createElement("option");
      optionB.value = item.code;
      optionB.textContent = label;
      offsetNode.appendChild(optionB);
    });
    accountNode.value = currentAccount;
    offsetNode.value = currentOffset;
  }
  const rows = filteredTagRecords();
  if (rows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="px-4 py-6 text-sm text-muted">No records match the current tag filters.</td></tr>`;
    el("tagsDetailEmpty").classList.remove("hidden");
    el("tagsDetailPanel").classList.add("hidden");
    return;
  }
  if (!rows.some((item) => item.id === state.selectedTagRecordId)) {
    state.selectedTagRecordId = rows[0].id;
  }
  rows.slice(0, 100).forEach((item) => {
    const tags = recordTagData(item);
    const tr = document.createElement("tr");
    tr.className = `border-b border-[rgba(77,49,29,0.08)] ${item.id === state.selectedTagRecordId ? "bg-[rgba(165,78,45,0.08)]" : ""}`;
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(item.source_type || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(canonicalVendorName(item.company_name) || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.amount || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(tags.category || "-")}${tags.subcategory ? ` / ${escapeHtml(tags.subcategory)}` : ""}</td>
      <td class="px-4 py-4"><button type="button" data-tag-record="${item.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Edit</button></td>
    `;
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-tag-record]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedTagRecordId = Number(button.dataset.tagRecord);
      renderTags();
    });
  });
  const record = rows.find((item) => item.id === state.selectedTagRecordId);
  const tags = record ? recordTagData(record) : null;
  el("tagsDetailEmpty").classList.add("hidden");
  el("tagsDetailPanel").classList.remove("hidden");
  el("tagsDetailTitle").textContent = record ? canonicalVendorName(record.company_name) : "Tag Detail";
  el("tagsDetailSubtitle").textContent = record ? `${record.doc_type || "-"} • ${record.date || "-"} • ${record.amount || "-"}` : "Pick a record to edit its accounting tags.";
  el("tagCategory").value = tags?.category || "";
  el("tagSubcategory").value = tags?.subcategory || "";
  el("tagAccountCode").value = tags?.account_code || "";
  el("tagOffsetAccountCode").value = tags?.offset_account_code || "";
  el("tagCostCode").value = tags?.cost_code || "";
  el("tagCostCenter").value = tags?.cost_center || "";
  el("tagProjectCode").value = tags?.project_code || "";
  el("tagPurchaseOrderId").value = tags?.purchase_order_id || "";
  el("tagPaymentMethod").value = tags?.payment_method || "";
  el("tagVatFlag").checked = Boolean(tags?.vat_flag);
}

function renderGlobalSearch() {
  const tbody = el("globalSearchTable").querySelector("tbody");
  tbody.innerHTML = "";
  const kindNode = el("globalSearchKindFilter");
  const currentKind = state.globalSearchKindFilter;
  kindNode.innerHTML = '<option value="">All Kinds</option>';
  state.globalSearchKindOptions.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    kindNode.appendChild(option);
  });
  kindNode.value = currentKind;
  const totalPages = state.globalSearchPagination.total_pages || 1;
  el("globalSearchPageLabel").textContent = `Page ${state.globalSearchPagination.page} of ${totalPages}`;
  el("globalSearchSummary").textContent = `${state.globalSearchPagination.total || 0} result${(state.globalSearchPagination.total || 0) === 1 ? "" : "s"}`;
  el("globalSearchPrevPage").disabled = state.globalSearchPagination.page <= 1;
  el("globalSearchNextPage").disabled = state.globalSearchPagination.page >= totalPages;
  el("globalSearchPrevPage").style.opacity = state.globalSearchPagination.page <= 1 ? "0.45" : "1";
  el("globalSearchNextPage").style.opacity = state.globalSearchPagination.page >= totalPages ? "0.45" : "1";
  if (!state.globalSearchRows.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="px-4 py-6 text-sm text-muted">No search results match the current filters.</td></tr>';
    el("globalSearchDetailEmpty").classList.remove("hidden");
    el("globalSearchDetailPanel").classList.add("hidden");
    return;
  }
  if (!state.globalSearchRows.some((item) => item.id === state.globalSearchSelectedId)) {
    state.globalSearchSelectedId = state.globalSearchRows[0].id;
  }
  state.globalSearchRows.forEach((item) => {
    const tr = document.createElement("tr");
    tr.className = `border-b border-[rgba(77,49,29,0.08)] ${item.id === state.globalSearchSelectedId ? "bg-[rgba(165,78,45,0.08)]" : ""}`;
    tr.style.cursor = "pointer";
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(item.source_type || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.source_file || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.doc_type || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(canonicalVendorName(item.company_name) || "-")}${reconciliationBadge(item)}</td>
      <td class="px-4 py-4">${escapeHtml(item.amount || "-")}</td>
      <td class="px-4 py-4"><button type="button" data-global-id="${item.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Inspect</button></td>
    `;
    tr.addEventListener("click", () => {
      state.globalSearchSelectedId = item.id;
      renderGlobalSearch();
    });
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-global-id]").forEach((button) => {
    button.addEventListener("click", () => {
      state.globalSearchSelectedId = Number(button.dataset.globalId);
      renderGlobalSearch();
    });
  });
  attachLinkedRecordHandlers(tbody);
  const record = state.documents.find((item) => item.id === state.globalSearchSelectedId) || state.globalSearchRows.find((item) => item.id === state.globalSearchSelectedId) || null;
  el("globalSearchDetailEmpty").classList.add("hidden");
  el("globalSearchDetailPanel").classList.remove("hidden");
  el("globalSearchDetailTitle").textContent = record ? canonicalVendorName(record.company_name) : "Search Detail";
  el("globalSearchDetailSubtitle").textContent = record ? `${record.source_file || "-"} • ${record.source_type || "-"}` : "Pick a result to inspect it.";
  el("globalSearchDetailSummary").textContent = record ? `${record.doc_type || "-"} • ${record.date || "-"} • ${record.number || "-"} • ${record.amount || "-"} • ${record.currency || "-"}` : "-";
  el("globalSearchDetailExplain").textContent = explainRecord(record);
  el("globalSearchDetailWarnings").textContent = record ? (() => {
    return `${warningsAndConfidenceText(record)} | Provenance: ${provenanceText(record)}`;
  })() : "-";
  el("globalSearchDetailRawText").textContent = record?.raw_text || "No raw OCR text stored.";
  el("globalSearchOpenDocument").disabled = !record?.output_path;
  el("globalSearchOpenDocument").style.opacity = record?.output_path ? "1" : "0.45";
  el("globalSearchOpenLinked").disabled = !(record && (record.matched_record_company_name || record.matched_record_number || record.matched_record_amount));
  el("globalSearchOpenLinked").style.opacity = !(record && (record.matched_record_company_name || record.matched_record_number || record.matched_record_amount)) ? "0.45" : "1";
}

function renderEvidence() {
  const tbody = el("evidenceTable").querySelector("tbody");
  tbody.innerHTML = "";
  const rows = evidenceFilteredRows();
  const totalPages = Math.max(1, Math.ceil(rows.length / DOCUMENTS_PAGE_SIZE));
  if (state.evidencePage > totalPages) state.evidencePage = totalPages;
  el("evidencePageLabel").textContent = `Page ${state.evidencePage} of ${totalPages}`;
  el("evidenceSummary").textContent = `${rows.length} row${rows.length === 1 ? "" : "s"}`;
  el("evidencePrevPage").disabled = state.evidencePage <= 1;
  el("evidenceNextPage").disabled = state.evidencePage >= totalPages;
  el("evidencePrevPage").style.opacity = state.evidencePage <= 1 ? "0.45" : "1";
  el("evidenceNextPage").style.opacity = state.evidencePage >= totalPages ? "0.45" : "1";
  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="7" class="px-4 py-6 text-sm text-muted">No evidence rows match the current filters.</td></tr>';
    el("evidenceDetailEmpty").classList.remove("hidden");
    el("evidenceDetailPanel").classList.add("hidden");
    setEvidencePreview("", "Select output or an attachment to preview it here.");
    return;
  }
  if (!rows.some((item) => item.id === state.evidenceSelectedId)) {
    state.evidenceSelectedId = rows[0].id;
  }
  const start = (state.evidencePage - 1) * DOCUMENTS_PAGE_SIZE;
  rows.slice(start, start + DOCUMENTS_PAGE_SIZE).forEach((item) => {
    const attachmentCount = Number(state.evidenceAttachmentCounts[String(item.id)] || 0);
    const tr = document.createElement("tr");
    tr.className = `border-b border-[rgba(77,49,29,0.08)] ${item.id === state.evidenceSelectedId ? "bg-[rgba(165,78,45,0.08)]" : ""}`;
    tr.style.cursor = "pointer";
    tr.innerHTML = `
      <td class="px-4 py-4"><input data-evidence-select="${item.id}" type="checkbox" class="h-4 w-4" ${state.evidenceSelectedIds.has(item.id) ? "checked" : ""} /></td>
      <td class="px-4 py-4">${escapeHtml(item.source_type || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(canonicalVendorName(item.company_name) || "-")}</td>
      <td class="px-4 py-4">${escapeHtml(item.amount || "-")}</td>
      <td class="px-4 py-4">${reconciliationBadge(item)}</td>
      <td class="px-4 py-4">${attachmentCount}</td>
      <td class="px-4 py-4"><button type="button" data-evidence-open="${item.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Manage</button></td>
    `;
    tr.addEventListener("click", async () => {
      state.evidenceSelectedId = item.id;
      await loadEvidenceAttachments(state.evidenceSelectedId);
      renderEvidence();
    });
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-evidence-open]").forEach((button) => {
    button.addEventListener("click", async () => {
      state.evidenceSelectedId = Number(button.dataset.evidenceOpen);
      await loadEvidenceAttachments(state.evidenceSelectedId);
      renderEvidence();
    });
  });
  tbody.querySelectorAll("[data-evidence-select]").forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const id = Number(checkbox.dataset.evidenceSelect);
      if (checkbox.checked) state.evidenceSelectedIds.add(id);
      else state.evidenceSelectedIds.delete(id);
    });
    checkbox.addEventListener("click", (event) => event.stopPropagation());
  });
  const record = rows.find((item) => item.id === state.evidenceSelectedId) || null;
  el("evidenceDetailEmpty").classList.add("hidden");
  el("evidenceDetailPanel").classList.remove("hidden");
  el("evidenceDetailTitle").textContent = record ? canonicalVendorName(record.company_name) : "Evidence Detail";
  el("evidenceDetailSubtitle").textContent = record ? `${record.source_file || "-"} • ${record.doc_type || "-"} • ${record.date || "-"}` : "Pick a stored document to manage attachments.";
  el("evidenceDetailRecord").textContent = record ? `${record.doc_type || "-"} • ${record.number || "-"} • ${record.amount || "-"} • ${record.match_status || "-"}` : "-";
  el("evidenceDetailAudit").textContent = record ? `${explainRecord(record)} | ${warningsAndConfidenceText(record)} | ${provenanceText(record)}` : "-";
  const outputHref = filePreviewHref(record?.output_path || "");
  el("evidenceOpenOutputLink").href = outputHref || "#";
  el("evidenceOpenOutputLink").style.pointerEvents = outputHref ? "auto" : "none";
  el("evidenceOpenOutputLink").style.opacity = outputHref ? "1" : "0.45";
  el("evidenceOpenLinkedButton").disabled = !(record && (record.matched_record_company_name || record.matched_record_number || record.matched_record_amount));
  el("evidenceOpenLinkedButton").style.opacity = !(record && (record.matched_record_company_name || record.matched_record_number || record.matched_record_amount)) ? "0.45" : "1";
  const selectedAttachment = state.evidenceAttachments.find((item) => item.id === state.evidenceSelectedAttachmentId) || null;
  if (selectedAttachment) {
    setEvidencePreview(selectedAttachment.file_path, `${attachmentTypeLabel(selectedAttachment.attachment_type)} • ${selectedAttachment.label || selectedAttachment.file_name}`);
  } else {
    setEvidencePreview(record?.output_path || "", record?.output_file || "Output document");
  }
  renderEvidenceAttachments();
  el("evidencePendingAttachmentPath").textContent = state.pendingEvidenceAttachmentPath || "No file selected.";
}

function renderActivityFeed() {
  const node = el("activityFeed");
  if (!node) return;
  if (!state.activityEvents.length) {
    node.innerHTML = '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-[rgba(255,247,239,0.82)] p-5 text-sm leading-6 text-muted">No tracked project activity yet.</div>';
    return;
  }
  node.innerHTML = state.activityEvents.map((item) => `
    <div class="rounded-2xl border border-[rgba(70,43,24,0.12)] bg-[#fff7ef] p-4">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="text-sm text-ink">${escapeHtml((item.kind || "").replaceAll("_", " "))}</strong>
        <span class="text-xs uppercase tracking-[0.14em] text-muted">${escapeHtml(formatDateTime(item.at))}</span>
      </div>
      <div class="mt-2 text-[11px] uppercase tracking-[0.14em] text-muted">${escapeHtml(item.username || "System")}</div>
      <div class="mt-2 text-sm leading-6 text-muted">${escapeHtml(item.summary || "-")}</div>
    </div>
  `).join("");
}

function renderResources() {
  const tbody = el("resourcesTable").querySelector("tbody");
  tbody.innerHTML = "";
  populateResourceFilters();
  updateResourcesPagination();
  if (!state.selectedProjectId || state.resourcesRows.length === 0) {
    el("resourcesSummary").textContent = "0 resources";
    renderResourceDetail(null);
    return;
  }
  if (!state.resourcesRows.some((item) => item.key === state.selectedResourceKey)) {
    state.selectedResourceKey = state.resourcesRows[0]?.key || "";
    state.resourceDetailPage = 1;
  }
  state.resourcesRows.forEach((item) => {
    const selected = item.key === state.selectedResourceKey;
    const healthClass =
      item.status === "healthy"
        ? "bg-[rgba(57,112,92,0.12)] text-[#275b4a]"
        : item.status === "warning"
          ? "bg-[rgba(217,119,6,0.12)] text-[#9a5b00]"
          : "bg-[rgba(180,58,58,0.12)] text-[#8f2b2b]";
    const healthLabel = `${item.status || "unknown"} • ${item.quality_score ?? 0}`;
    const tr = document.createElement("tr");
    tr.className = `border-b border-[rgba(77,49,29,0.08)] ${selected ? "bg-[rgba(165,78,45,0.08)]" : ""}`;
    tr.style.cursor = "pointer";
    tr.innerHTML = `
      <td class="px-4 py-4">${escapeHtml(item.source_type)}</td>
      <td class="px-4 py-4">${fileLink(item.source_path, item.source_file || "Open")}</td>
      <td class="px-4 py-4">${escapeHtml(item.source_origin)}</td>
      <td class="px-4 py-4"><span class="inline-flex rounded-full px-2 py-1 text-[11px] font-semibold ${healthClass}">${escapeHtml(healthLabel)}</span></td>
      <td class="px-4 py-4">${item.record_count}</td>
      <td class="px-4 py-4">${item.output_count}</td>
      <td class="px-4 py-4">${escapeHtml(item.date_from || "-")}${item.date_to && item.date_to !== item.date_from ? ` to ${escapeHtml(item.date_to)}` : ""}</td>
      <td class="px-4 py-4">Debit ${formatMoney(item.debit_total)} / Credit ${formatMoney(item.credit_total)}</td>
      <td class="px-4 py-4"><button type="button" data-resource-key="${escapeHtml(item.key)}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">View Records</button></td>
    `;
    tr.addEventListener("click", async () => {
      state.selectedResourceKey = item.key;
      state.resourceDetailPage = 1;
      await loadResourceDetail();
      renderResources();
    });
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll("[data-resource-key]").forEach((button) => {
    button.addEventListener("click", async () => {
      state.selectedResourceKey = button.dataset.resourceKey;
      state.resourceDetailPage = 1;
      await loadResourceDetail();
      renderResources();
    });
  });
  renderResourceDetail(state.resourceDetail || state.resourcesRows.find((item) => item.key === state.selectedResourceKey) || null);
}

function renderCloseWorkspace() {
  const kpiGrid = el("closeKpiGrid");
  const agingList = el("closeAgingList");
  const attentionList = el("closeAttentionList");
  const presetNode = el("accountingExportPreset");
  const presetSummaryNode = el("accountingExportPresetSummary");
  if (!kpiGrid || !agingList || !attentionList || !presetNode || !presetSummaryNode) return;
  const currentPreset = state.accountingExportPreset || "ultra_force";
  presetNode.innerHTML = "";
  state.accountingExportPresets.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.key;
    option.textContent = item.label;
    presetNode.appendChild(option);
  });
  if (!presetNode.options.length) {
    const option = document.createElement("option");
    option.value = "ultra_force";
    option.textContent = "ULTRA FORCE";
    presetNode.appendChild(option);
  }
  presetNode.value = currentPreset;
  const selectedPreset = state.accountingExportPresets.find((item) => item.key === currentPreset);
  presetSummaryNode.textContent = selectedPreset
    ? `${selectedPreset.label}: ${selectedPreset.description}`
    : "Choose a preset to see export intent and target layout.";
  const payload = state.closeSummary;
  if (!state.selectedProjectId || !payload?.summary) {
    kpiGrid.innerHTML = "";
    agingList.innerHTML = '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-white px-4 py-4 text-sm text-muted">Open a project to load close data.</div>';
    attentionList.innerHTML = '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-white px-4 py-4 text-sm text-muted">No close items available.</div>';
    return;
  }
  const summary = payload.summary;
  const kpis = [
    ["Stored Records", String(summary.total_documents || 0), "All stored records in the project"],
    ["Bank Transactions", String(summary.bank_transactions || 0), "Imported bank statement rows"],
    ["Unresolved Items", String(summary.unresolved_count || 0), "Missing receipt, low confidence, or still open"],
    ["Unresolved Amount", `${formatMoney(summary.unresolved_amount || 0)} AED`, "Total value of unresolved items"],
    ["Matched Rows", String(summary.matched_count || 0), "Rows already linked or reconciled"],
    ["Reviewed Rows", String(summary.reviewed_count || 0), "Rows with explicit review state"],
  ];
  kpiGrid.innerHTML = kpis.map(([label, value, note]) => `
    <div class="dashboard-kpi-card">
      <div class="dashboard-kpi-label">${label}</div>
      <div class="dashboard-kpi-value">${value}</div>
      <div class="dashboard-kpi-note">${note}</div>
    </div>
  `).join("");

  agingList.innerHTML = (payload.aging || []).map((item) => `
    <div class="dashboard-list-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="text-sm">${escapeHtml(item.bucket)}</strong>
        <span class="dashboard-amount-pill">${formatMoney(item.amount || 0)} AED</span>
      </div>
      <div class="mt-2 text-xs text-muted">${item.count} unresolved item${item.count === 1 ? "" : "s"}</div>
    </div>
  `).join("") || '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-white px-4 py-4 text-sm text-muted">No unresolved aging data.</div>';

  attentionList.innerHTML = (payload.attention || []).map((item) => `
    <div class="dashboard-list-card attention">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <strong class="max-w-[72%] text-sm">${escapeHtml(item.company_name || "Unknown")}</strong>
        <span class="dashboard-amount-pill danger">${formatMoney(item.amount || 0)} AED</span>
      </div>
      <div class="mt-2 text-xs leading-6 text-muted">${escapeHtml(item.date || "Unknown date")} • ${escapeHtml(item.source_file || "-")} • ${item.age_days == null ? "Unknown age" : `${item.age_days} days`}</div>
    </div>
  `).join("") || '<div class="rounded-2xl border border-dashed border-[rgba(77,49,29,0.15)] bg-white px-4 py-4 text-sm text-muted">No unresolved attention items.</div>';
}

function populateHistoryFilters(documents) {
  const typeFilter = el("historyTypeFilter");
  const companyFilter = el("historyCompanyFilter");
  const companyOptions = el("historyCompanyOptions");
  const currentType = state.historyTypeFilter;
  const currentCompany = state.historyCompanyFilter;
  const types = [...new Set(documents.map((item) => item.doc_type).filter(Boolean))].sort();
  const companies = new Map();
  documents.forEach((item) => {
    const raw = String(item.company_name || "").trim();
    const normalized = normalizeCompanyName(raw);
    if (!normalized) return;
    if (!companies.has(normalized)) {
      companies.set(normalized, { label: raw, count: 0 });
    }
    const bucket = companies.get(normalized);
    bucket.count += 1;
    if (raw.length < bucket.label.length) {
      bucket.label = raw;
    }
  });

  typeFilter.innerHTML = '<option value="">All Types</option>';
  companyOptions.innerHTML = "";
  types.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    typeFilter.appendChild(option);
  });
  Array.from(companies.entries())
    .sort((a, b) => a[1].label.localeCompare(b[1].label))
    .forEach(([normalized, value]) => {
    const option = document.createElement("option");
      option.value = value.label;
      option.label = `${value.label} (${value.count})`;
      option.dataset.normalized = normalized;
      companyOptions.appendChild(option);
    });
  typeFilter.value = currentType;
  const currentCompanyLabel = companies.get(currentCompany)?.label || currentCompany;
  companyFilter.value = currentCompanyLabel;
}

function populateDocumentsFilters(documents) {
  const kindFilter = el("documentsKindFilter");
  const typeFilter = el("documentsTypeFilter");
  const currentKind = state.documentsKindFilter;
  const currentType = state.documentsTypeFilter;
  const kinds = [...new Set(documents.map((item) => item.source_type).filter(Boolean))].sort();
  const types = [...new Set(documents.map((item) => item.doc_type).filter(Boolean))].sort();

  kindFilter.innerHTML = '<option value="">All Kinds</option>';
  typeFilter.innerHTML = '<option value="">All Types</option>';
  kinds.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    kindFilter.appendChild(option);
  });
  types.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    typeFilter.appendChild(option);
  });
  kindFilter.value = currentKind;
  typeFilter.value = currentType;
}

function getFilteredDocuments(documents) {
  const query = state.documentsSearch.trim().toLowerCase();
  return documents.filter((item) => {
    const matchesQuery =
      !query ||
      [
        item.source_file,
        item.output_file,
        item.source_type,
        item.source_origin,
        item.source_timestamp,
        item.doc_type,
        item.date,
        item.number,
        item.company_name,
        item.amount,
        item.confidence_label,
        item.match_status,
      ]
        .join(" ")
        .toLowerCase()
        .includes(query);
    const matchesKind = !state.documentsKindFilter || item.source_type === state.documentsKindFilter;
    const matchesType = !state.documentsTypeFilter || item.doc_type === state.documentsTypeFilter;
    const matchesConfidence = !state.documentsConfidenceFilter || item.confidence_label === state.documentsConfidenceFilter;
    const matchesMatch = !state.documentsMatchFilter || (item.match_status || "") === state.documentsMatchFilter;
    return matchesQuery && matchesKind && matchesType && matchesConfidence && matchesMatch;
  });
}

function updateDocumentsPagination(totalItems) {
  const totalPages = state.documentsTablePagination.total_pages || 1;
  el("documentsPageLabel").textContent = `Page ${state.documentsTablePagination.page} of ${totalPages}`;
  el("documentsSummary").textContent = `${totalItems} document${totalItems === 1 ? "" : "s"}`;
  el("documentsPrevPage").disabled = state.documentsTablePagination.page <= 1;
  el("documentsNextPage").disabled = state.documentsTablePagination.page >= totalPages;
  el("documentsPrevPage").style.opacity = state.documentsTablePagination.page <= 1 ? "0.45" : "1";
  el("documentsNextPage").style.opacity = state.documentsTablePagination.page >= totalPages ? "0.45" : "1";
}

function getFilteredHistory(documents) {
  const query = state.historySearch.trim().toLowerCase();
  return documents.filter((item) => {
    const matchesQuery =
      !query ||
      [
        item.source_file,
        item.output_file,
        item.doc_type,
        item.date,
        item.number,
        item.company_name,
        item.amount,
        item.currency,
        item.source_type,
        item.source_origin,
        item.source_timestamp,
        item.match_status,
        item.match_basis,
      ]
        .join(" ")
        .toLowerCase()
        .includes(query);
    const matchesType = !state.historyTypeFilter || item.doc_type === state.historyTypeFilter;
    const matchesCompany = !state.historyCompanyFilter || normalizeCompanyName(item.company_name) === state.historyCompanyFilter;
    const matchesConfidence = !state.historyConfidenceFilter || item.confidence_label === state.historyConfidenceFilter;
    return matchesQuery && matchesType && matchesCompany && matchesConfidence;
  });
}

function updateHistoryPagination(totalItems) {
  const totalPages = state.historyTablePagination.total_pages || 1;
  el("historyPageLabel").textContent = `Page ${state.historyTablePagination.page} of ${totalPages}`;
  el("historySummary").textContent = `${totalItems} result${totalItems === 1 ? "" : "s"}`;
  el("historyPrevPage").disabled = state.historyTablePagination.page <= 1;
  el("historyNextPage").disabled = state.historyTablePagination.page >= totalPages;
  el("historyPrevPage").style.opacity = state.historyTablePagination.page <= 1 ? "0.45" : "1";
  el("historyNextPage").style.opacity = state.historyTablePagination.page >= totalPages ? "0.45" : "1";
}

function renderHistoryTable() {
  const tbody = el("historyTable").querySelector("tbody");
  const selectAll = el("historySelectAll");
  tbody.innerHTML = "";
  populateHistoryFilters(state.documents);
  const filteredDocuments = getFilteredHistory(state.documents);
  updateHistoryPagination(state.historyTablePagination.total || 0);
  const pageDocuments = state.historyTableRows;
  state.selectedHistoryIds = new Set(
    Array.from(state.selectedHistoryIds).filter((id) => state.documents.some((item) => item.id === id)),
  );
  selectAll.checked = false;
  if (!state.selectedProjectId || pageDocuments.length === 0) {
    el("historySummary").textContent = state.documents.length === 0 ? "0 results" : "No results match the current filters";
    return;
  }

  pageDocuments.forEach((item) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    tr.innerHTML = `
      <td class="px-4 py-4"><input data-history-id="${item.id}" type="checkbox" class="history-checkbox h-4 w-4" ${state.selectedHistoryIds.has(item.id) ? "checked" : ""} /></td>
      <td class="px-4 py-4">${formatDateTime(item.created_at)}</td>
      <td class="px-4 py-4">${item.source_type || "-"}</td>
      <td class="px-4 py-4">${item.source_origin || "-"}</td>
      <td class="px-4 py-4">${item.source_timestamp || "-"}</td>
      <td class="px-4 py-4">${fileLink(item.source_path, item.source_file || "Open")}</td>
      <td class="px-4 py-4">${fileLink(item.output_path, item.output_file || "Open")}</td>
      <td class="px-4 py-4">${item.doc_type}</td>
      <td class="px-4 py-4">${item.date}</td>
      <td class="px-4 py-4">${item.number}</td>
      <td class="px-4 py-4">${escapeHtml(item.company_name)}${reconciliationBadge(item)}</td>
      <td class="px-4 py-4">${item.amount}</td>
      <td class="px-4 py-4">${item.currency}</td>
      <td class="px-4 py-4">${confidenceBadge(item.confidence_label, item.confidence_score)}</td>
      <td class="px-4 py-4"><button data-edit-history-id="${item.id}" class="rounded-full bg-[rgba(165,78,45,0.1)] px-3 py-2 text-xs font-semibold text-emberdark">Edit</button></td>
    `;
    tbody.appendChild(tr);
  });

  tbody.querySelectorAll(".history-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const id = Number(checkbox.dataset.historyId);
      if (checkbox.checked) {
        state.selectedHistoryIds.add(id);
      } else {
        state.selectedHistoryIds.delete(id);
      }
      selectAll.checked = pageDocuments.length > 0 && pageDocuments.every((item) => state.selectedHistoryIds.has(item.id));
    });
  });
  tbody.querySelectorAll("[data-edit-history-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const document = state.documents.find((item) => item.id === Number(button.dataset.editHistoryId));
      if (document) {
        openEditResultModal(document);
      }
    });
  });
  attachLinkedRecordHandlers(tbody);

  selectAll.checked = pageDocuments.length > 0 && pageDocuments.every((item) => state.selectedHistoryIds.has(item.id));
}

function renderDocumentsTable() {
  const tbody = el("documentsTable").querySelector("tbody");
  tbody.innerHTML = "";
  populateDocumentsFilters(state.documents);
  updateDocumentsPagination(state.documentsTablePagination.total || 0);
  if (!state.selectedProjectId || state.documentsTableRows.length === 0) {
    el("documentsSummary").textContent = state.documents.length === 0 ? "0 documents" : "No documents match the current filters";
    return;
  }
  state.documentsTableRows.forEach((item) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    tr.innerHTML = `
      <td class="px-4 py-4">${item.source_type || "-"}</td>
      <td class="px-4 py-4">${item.source_timestamp || "-"}</td>
      <td class="px-4 py-4">${fileLink(item.source_path, item.source_file || "Open")}</td>
      <td class="px-4 py-4">${fileLink(item.output_path, item.output_file || "Open")}</td>
      <td class="px-4 py-4">${fileLink(item.enhanced_output_path, item.enhanced_output_path ? "Enhanced PDF" : "")}</td>
      <td class="px-4 py-4">${fileLink(item.original_debug_image, item.original_debug_image ? "Original Image" : "")}</td>
      <td class="px-4 py-4">${fileLink(item.enhanced_debug_image, item.enhanced_debug_image ? "Enhanced Image" : "")}</td>
      <td class="px-4 py-4">${item.doc_type}</td>
      <td class="px-4 py-4">${item.date}</td>
      <td class="px-4 py-4">${item.number}</td>
      <td class="px-4 py-4">${confidenceBadge(item.confidence_label, item.confidence_score)}${reconciliationBadge(item)}</td>
    `;
    tbody.appendChild(tr);
  });
  attachLinkedRecordHandlers(tbody);
}

function renderDocuments(documents) {
  state.documents = documents;
  if (!state.selectedProjectId || documents.length === 0) {
    state.documentsTableRows = [];
    state.historyTableRows = [];
    state.resourcesRows = [];
    state.resourceDetail = null;
    state.resourceDetailRows = [];
    state.resourceDetailPagination = { page: 1, page_size: RESOURCE_DETAIL_PAGE_SIZE, total: 0, total_pages: 1 };
    state.resourceDiagnostics = null;
    state.resourceActivity = [];
    renderDocumentsTable();
    renderReconciliationWorkspace();
    renderReviewQueue();
    renderExceptionsWorkspace();
    renderFeedbackWorkspace();
    renderVendors();
    renderRules();
    renderTags();
    renderGlobalSearch();
    renderEvidence();
    renderCloseWorkspace();
    renderResources();
    renderHistoryTable();
    renderProjectDetail();
    return;
  }
  syncRecordTagsFromDocuments();
  renderProjectDetail();
  renderActiveProjectTab();
}

function projectPayload() {
  return {
    name: el("projectRecordName").value.trim() || "ULTRA FORCE Project",
    description: el("projectDescription").value.trim(),
    job_code: el("projectJobCode").value.trim(),
    client_name: el("projectClientName").value.trim(),
    site_name: el("projectSiteName").value.trim(),
    contract_number: el("projectContractNumber").value.trim(),
    budget_amount: el("projectBudgetAmount").value.trim(),
    contract_value: el("projectContractValue").value.trim(),
    variation_amount: el("projectVariationAmount").value.trim(),
    billed_to_date: el("projectBilledToDate").value.trim(),
    certified_progress_pct: el("projectCertifiedProgressPct").value.trim(),
    retention_percent: el("projectRetentionPercent").value.trim(),
    advance_received: el("projectAdvanceReceived").value.trim(),
    project_status: el("projectStatus").value,
    ...fields(),
  };
}

function resetJobPanels() {
  setStatus("Idle");
  el("logs").textContent = "";
  el("resultsMeta").textContent = "No run yet.";
  el("resultsTable").querySelector("tbody").innerHTML = "";
  hideRunProgress();
}

function resetProjectForm() {
  state.selectedProjectId = null;
  state.documents = [];
  state.documentsTableRows = [];
  state.documentsTablePagination = { page: 1, page_size: DOCUMENTS_PAGE_SIZE, total: 0, total_pages: 1 };
  state.historyTableRows = [];
  state.historyTablePagination = { page: 1, page_size: HISTORY_PAGE_SIZE, total: 0, total_pages: 1 };
  state.resourcesRows = [];
  state.resourcesPagination = { page: 1, page_size: RESOURCES_PAGE_SIZE, total: 0, total_pages: 1 };
  state.resourceKindOptions = [];
  state.resourceDetail = null;
  state.resourceDetailRows = [];
  state.resourceDetailPagination = { page: 1, page_size: RESOURCE_DETAIL_PAGE_SIZE, total: 0, total_pages: 1 };
  state.resourceDiagnostics = null;
  state.resourceActivity = [];
  state.projectMembers = [];
  state.closeSummary = null;
  state.accountingAccounts = [];
  state.accountingPeriods = [];
  state.journalDrafts = [];
  state.journalDraftSummary = { draft_count: 0, posted_amount: 0 };
  state.journalEntries = [];
  state.trialBalanceRows = [];
  state.accountingExportPreset = "ultra_force";
  state.accountingExportPresets = [];
  state.globalSearchQuery = "";
  state.globalSearchKindFilter = "";
  state.globalSearchStatusFilter = "";
  state.globalSearchConfidenceFilter = "";
  state.globalSearchPage = 1;
  state.globalSearchRows = [];
  state.globalSearchPagination = { page: 1, page_size: GLOBAL_SEARCH_PAGE_SIZE, total: 0, total_pages: 1 };
  state.globalSearchSelectedId = 0;
  state.globalSearchKindOptions = [];
  state.savedSearches = [];
  state.evidenceSearch = "";
  state.evidenceAttachmentFilter = "";
  state.evidencePage = 1;
  state.evidenceSelectedId = 0;
  state.evidenceSelectedIds = new Set();
  state.evidenceAttachments = [];
  state.evidenceAttachmentCounts = {};
  state.pendingEvidenceAttachmentPath = "";
  state.evidenceSelectedAttachmentId = 0;
  state.evidencePreviewPath = "";
  state.evidencePreviewLabel = "";
  state.reviewComments = [];
  state.selectedHistoryIds = new Set();
  state.historySearch = "";
  state.historyTypeFilter = "";
  state.historyCompanyFilter = "";
  state.historyConfidenceFilter = "";
  state.documentsSearch = "";
  state.documentsKindFilter = "";
  state.documentsTypeFilter = "";
  state.documentsConfidenceFilter = "";
  state.documentsMatchFilter = "";
  state.resourcesSearch = "";
  state.resourcesKindFilter = "";
  state.resourcesPage = 1;
  state.selectedResourceKey = "";
  state.resourceDetailPage = 1;
  state.reconciliationSearch = "";
  state.reconciliationStatusFilter = "attention";
  state.reconciliationBankFilter = "";
  state.reconciliationSort = "priority";
  state.reconciliationPage = 1;
  state.reconciliationSelectedId = 0;
  state.reconciliationSessionDecisions = {};
  state.reviewQueueSearch = "";
  state.reviewQueueTypeFilter = "";
  state.reviewQueueSourceFilter = "";
  state.reviewQueuePage = 1;
  state.reviewQueueSelectedKey = "";
  state.exceptionsSearch = "";
  state.exceptionsTypeFilter = "";
  state.exceptionsPage = 1;
  state.exceptionsRows = [];
  state.exceptionsPagination = { page: 1, page_size: 12, total: 0, total_pages: 1 };
  state.exceptionsSummary = { total: 0, installments: 0, refund_pairs: 0, split_groups: 0, duplicates: 0, mismatches: 0 };
  state.exceptionsSelectedKey = "";
  state.feedbackInsights = null;
  state.vendorSearch = "";
  state.vendorsPage = 1;
  state.selectedVendorKey = "";
  state.vendorAliases = {};
  state.projectRules = [];
  state.tagsSearch = "";
  state.tagsSourceFilter = "";
  state.selectedTagRecordId = 0;
  state.recordTags = {};
  state.documentsPage = 1;
  state.historyPage = 1;
  state.dashboardSearch = "";
  state.dashboardDateFrom = "";
  state.dashboardDateTo = "";
  state.dashboardDirectionFilter = "";
  state.dashboardMatchFilter = "";
  state.dashboardBankFilter = "";
  state.dashboardAnalytics = null;
  state.dashboardBankOptions = [];
  state.dashboardDrilldownTitle = "Drill Down";
  state.dashboardDrilldownSubtitle = "Click any dashboard item to inspect the underlying bank rows.";
  state.dashboardDrilldownRows = [];
  state.dashboardDrilldownMode = "all";
  state.dashboardDrilldownValue = "";
  state.dashboardDrilldownPagination = { page: 1, page_size: DASHBOARD_DRILLDOWN_PAGE_SIZE, total: 0, total_pages: 1 };
  state.dashboardDrilldownSearch = "";
  state.dashboardDrilldownDirection = "";
  state.dashboardDrilldownMatch = "";
  state.dashboardDrilldownPage = 1;
  el("projectFormTitle").textContent = "New Project";
  el("projectRecordName").value = "ULTRA FORCE Project";
  el("projectDescription").value = "";
  el("projectJobCode").value = "";
  el("projectClientName").value = "";
  el("projectSiteName").value = "";
  el("projectContractNumber").value = "";
  el("projectBudgetAmount").value = "";
  el("projectContractValue").value = "";
  el("projectVariationAmount").value = "";
  el("projectBilledToDate").value = "";
  el("projectCertifiedProgressPct").value = "";
  el("projectRetentionPercent").value = "";
  el("projectAdvanceReceived").value = "";
  el("projectStatus").value = "active";
  applySettings(emptyProjectSettings());
  resetJobPanels();
  renderDocuments([]);
  renderHistoryTable();
  renderSidebarProjects();
  renderProjectsTable();
  renderDashboard();
  renderProjectDetail();
  renderCompaniesWorkspace();
  updateRunAvailability();
}

async function stopJob() {
  if (!state.jobId) {
    showSweetAlert("No Active Run", "There is no active OCR run to stop.", "error");
    return;
  }
  try {
    await fetchJson(`/api/jobs/${state.jobId}/cancel`, { method: "POST" });
    setStatus("cancelling");
    showRunProgress("Stopping Run", "ULTRA FORCE will stop after the current file finishes.");
    showSweetAlert("Stop Requested", "The current run will stop after the file in progress completes.", "info");
  } catch (error) {
    showSweetAlert("Stop Error", error.message, "error");
  }
}

async function pollJob() {
  if (!state.jobId) return;
  try {
    const job = await fetchJson(`/api/jobs/${state.jobId}`);
    renderJob(job);
    if (job.status === "queued") {
      showRunProgress("OCR Queue", "ULTRA FORCE queued the run and is about to start processing.");
    } else if (job.status === "running") {
      showRunProgress("Processing OCR", "Extracting data and generating output files. This can take a bit on larger folders.");
    } else if (job.status === "cancelling") {
      showRunProgress("Stopping Run", "ULTRA FORCE will stop after the current file currently being processed completes.");
    }
    if (job.status === "completed" || job.status === "failed" || job.status === "cancelled") {
      clearInterval(state.pollTimer);
      state.pollTimer = null;
      state.jobId = null;
      hideRunProgress();
      if (state.selectedProjectId) {
        await loadDocuments(state.selectedProjectId);
      }
      updateRunAvailability();
    }
  } catch (error) {
    clearInterval(state.pollTimer);
    state.pollTimer = null;
    setStatus("polling-error");
    hideRunProgress();
    showSweetAlert("Polling Error", error.message, "error");
  }
}

async function runJob() {
  if (!state.authToken) {
    showSweetAlert("Login Required", "Sign in before running OCR jobs.", "error");
    return;
  }
  if (!state.selectedProjectId) {
    showSweetAlert("Project Required", "Create or open a project before running OCR.", "error");
    return;
  }
  const payload = {
    ...fields(),
    project_id: state.selectedProjectId,
  };
  if (!payload.source_dir || !payload.output_dir || !payload.project_name) {
    showSweetAlert("Missing Required Fields", "Output folder and project name are required. PDF mode also needs a source folder, and video mode needs a video file.", "error");
    switchView("projectEditor");
    return;
  }
  if (!payload.source_dir) {
    showSweetAlert("Missing Source Folder", "Choose one source folder containing PDFs, videos, or sheet files.", "error");
    switchView("projectEditor");
    return;
  }
  try {
    showRunProgress("Preparing OCR Run", "Submitting the project for extraction.");
    const response = await fetchJson("/api/jobs", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.jobId = response.job_id;
    setStatus("queued");
    el("logs").textContent = "";
    el("resultsTable").querySelector("tbody").innerHTML = "";
    el("resultsMeta").textContent = "Run queued.";
    switchView("projectDetail");
    switchProjectTab("run");
    if (state.pollTimer) clearInterval(state.pollTimer);
    state.pollTimer = setInterval(pollJob, 1500);
    updateRunAvailability();
    pollJob();
  } catch (error) {
    hideRunProgress();
    showSweetAlert("Run Error", error.message, "error");
  }
}

async function loadProjects() {
  if (!state.authToken) {
    state.projects = [];
    state.selectedProjectId = null;
    renderSidebarProjects();
    renderProjectsTable();
    renderDashboard();
    renderDocuments([]);
    return;
  }
  const payload = await fetchJson("/api/projects");
  state.projects = payload.projects;
  if (!state.projects.some((project) => project.id === state.selectedProjectId)) {
    state.selectedProjectId = null;
    renderDocuments([]);
  }
  renderSidebarProjects();
  renderProjectsTable();
  renderDashboard();
  renderProjectDetail();
  renderCompaniesWorkspace();
  updateRunAvailability();
}

async function loadDocuments(projectId) {
  if (!projectId) {
    renderDocuments([]);
    state.dashboardAnalytics = null;
    state.dashboardBankOptions = [];
    state.dashboardDrilldownRows = [];
    state.dashboardDrilldownPagination = { page: 1, page_size: DASHBOARD_DRILLDOWN_PAGE_SIZE, total: 0, total_pages: 1 };
    resetLoadedProjectTabs();
    return;
  }
  const payload = await fetchJson(`/api/projects/${projectId}/documents?page=1&page_size=10000`);
  renderDocuments(payload.documents);
  resetLoadedProjectTabs();
  await loadProjectTabData("overview", true);
}

function applyProject(project) {
  state.selectedProjectId = project.id;
  el("projectFormTitle").textContent = `Edit Project: ${project.name}`;
  el("projectRecordName").value = project.name;
  el("projectDescription").value = project.description || "";
  el("projectJobCode").value = project.job_code || "";
  el("projectClientName").value = project.client_name || "";
  el("projectSiteName").value = project.site_name || "";
  el("projectContractNumber").value = project.contract_number || "";
  el("projectBudgetAmount").value = project.budget_amount || "";
  el("projectContractValue").value = project.contract_value || "";
  el("projectVariationAmount").value = project.variation_amount || "";
  el("projectBilledToDate").value = project.billed_to_date || "";
  el("projectCertifiedProgressPct").value = project.certified_progress_pct || "";
  el("projectRetentionPercent").value = project.retention_percent || "";
  el("projectAdvanceReceived").value = project.advance_received || "";
  el("projectStatus").value = project.project_status || "active";
  applySettings(project.settings);
  renderSidebarProjects();
  renderProjectsTable();
  renderDashboard();
  renderProjectDetail();
  updateRunAvailability();
}

async function openProject(projectId, tab = "overview") {
  const project = state.projects.find((item) => item.id === projectId);
  if (!project) return;
  applyProject(project);
  await Promise.all([loadVendorAliasesRemote(), loadProjectRulesRemote(), loadCompanyAccountingRules()]);
  await loadProjectMembers();
  await loadDocuments(project.id);
  switchView("projectDetail");
  switchProjectTab(tab);
}

async function saveProject() {
  if (!state.authToken) {
    showSweetAlert("Login Required", "Sign in before saving a project.", "error");
    return;
  }
  const payload = projectPayload();
  try {
    showLoading("Saving Project", "ULTRA FORCE is storing the current project configuration.");
    let savedProject;
    if (state.selectedProjectId) {
      const response = await fetchJson(`/api/projects/${state.selectedProjectId}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      savedProject = response.project;
    } else {
      const response = await fetchJson("/api/projects", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      savedProject = response.project;
    }
    await loadProjects();
    applyProject(savedProject);
    await loadDocuments(savedProject.id);
    switchView("projectDetail");
    switchProjectTab("overview");
    showSweetAlert("Project Saved", "Project configuration stored successfully.", "success");
  } catch (error) {
    showSweetAlert("Project Error", error.message, "error");
  } finally {
    hideLoading();
  }
}

async function rebuildReconciliation() {
  if (!state.selectedProjectId) {
    showSweetAlert("Project Required", "Open a project before rebuilding reconciliation.", "error");
    return;
  }
  try {
    showLoading("Rebuilding Reconciliation", "Recomputing links between bank transactions and stored PDF/video records.");
    const response = await fetchJson(`/api/projects/${state.selectedProjectId}/rebuild-reconciliation`, {
      method: "POST",
    });
    await loadDocuments(state.selectedProjectId);
    renderProjectDetail();
    showSweetAlert("Reconciliation Rebuilt", `${response.updated || 0} stored records were refreshed.`, "success");
  } catch (error) {
    showSweetAlert("Rebuild Error", error.message, "error");
  } finally {
    hideLoading();
  }
}

async function saveEditedResult() {
  if (!state.editingDocumentId) {
    showSweetAlert("No Result Selected", "Choose a stored result to edit first.", "error");
    return;
  }
  const payload = {
    doc_type: el("editDocType").value.trim() || "Unknown",
    date: el("editDocDate").value.trim() || "Unknown",
    number: el("editDocNumber").value.trim() || "Unknown",
    company_name: el("editDocCompany").value.trim() || "Unknown",
    amount: el("editDocAmount").value.trim() || "Unknown",
    currency: el("editDocCurrency").value.trim() || "Unknown",
  };
  try {
    const existing = state.documents.find((item) => item.id === state.editingDocumentId) || null;
    showLoading("Updating Stored Result", "Saving corrections and renaming generated files.");
    const response = await fetchJson(`/api/documents/${state.editingDocumentId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
    if (existing && payload.company_name && normalizeCompanyName(existing.company_name) && payload.company_name !== existing.company_name && state.selectedProjectId) {
      await fetchJson(`/api/projects/${state.selectedProjectId}/vendor-aliases`, {
        method: "POST",
        body: JSON.stringify({
          normalized_key: normalizeCompanyName(existing.company_name),
          canonical_name: payload.company_name,
        }),
      });
      state.vendorAliases[normalizeCompanyName(existing.company_name)] = payload.company_name;
    }
    replaceDocumentInState(response.document);
    closeEditResultModal();
    if (state.selectedProjectId) {
      await loadDocuments(state.selectedProjectId);
    }
    showSweetAlert("Stored Result Updated", "Metadata and output file names were updated.", "success");
  } catch (error) {
    showSweetAlert("Update Error", error.message, "error");
  } finally {
    hideLoading();
  }
}

async function deleteCurrentProject() {
  const project = getSelectedProject();
  if (!project) {
    showSweetAlert("Project Required", "Open a project before deleting it.", "error");
    return;
  }
  const confirmed = await confirmSweetAlert(
    "Delete Project",
    `Delete "${project.name}" and all stored OCR data for this project? This cannot be undone.`,
    "Delete Project",
  );
  if (!confirmed) {
    return;
  }
  try {
    showLoading("Deleting Project", "Removing the project and its stored OCR records.");
    await fetchJson(`/api/projects/${project.id}`, { method: "DELETE" });
    state.selectedProjectId = null;
    state.documents = [];
    resetLoadedProjectTabs();
    resetProjectForm();
    await loadProjects();
    switchView("home");
    showSweetAlert("Project Deleted", "The project and its stored records were removed.", "success");
  } catch (error) {
    showSweetAlert("Delete Error", error.message, "error");
  } finally {
    hideLoading();
  }
}

async function loginOrRegister(mode) {
  const username = el("authUsername").value.trim();
  const password = el("authPassword").value;
  if (!username || !password) {
    showSweetAlert("Missing Credentials", "Enter username and password first.", "error");
    return;
  }
  try {
    const payload = await fetchJson(`/api/auth/${mode}`, {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    state.authToken = payload.token;
    state.currentUser = payload.user;
    localStorage.setItem("ultra_force_token", payload.token);
    await loadProjects();
    showAppView();
    switchView("home");
    renderDashboard();
    if (mode !== "login") {
      showSweetAlert("Account Created", `Welcome ${payload.user.username}.`, "success");
    }
  } catch (error) {
    showSweetAlert("Authentication Error", error.message, "error");
  }
}

async function restoreSession() {
  if (!state.authToken) {
    showAuthView();
    return;
  }
  try {
    const user = await fetchJson("/api/me");
    state.currentUser = user;
    await loadProjects();
    showAppView();
    switchView("home");
  } catch {
    state.authToken = "";
    state.currentUser = null;
    localStorage.removeItem("ultra_force_token");
    showAuthView();
  }
}

async function logout() {
  if (state.authToken) {
    try {
      await fetchJson("/api/auth/logout", { method: "POST" });
    } catch {
      // Ignore logout transport failures and clear local state anyway.
    }
  }
  state.authToken = "";
  state.currentUser = null;
  state.projects = [];
  state.selectedProjectId = null;
  state.documents = [];
  localStorage.removeItem("ultra_force_token");
  if (state.pollTimer) {
    clearInterval(state.pollTimer);
    state.pollTimer = null;
  }
  if (state.modelRefreshTimer) {
    clearInterval(state.modelRefreshTimer);
    state.modelRefreshTimer = null;
  }
  resetProjectForm();
  showAuthView();
  showSweetAlert("Signed Out", "ULTRA FORCE cleared the current session.", "success");
}

async function init() {
  const payload = await fetchJson("/api/settings");
  state.options = payload.options;
  state.models = payload.models?.models || payload.runtime?.trocr_models || [];
  bindCompaniesViewHandlers();

  populateSelect(el("ocrBackend"), payload.options.ocr_backends);
  populateSelect(el("handwritingBackend"), payload.options.handwriting_backends);
  populateSelect(el("trocrModel"), payload.options.trocr_models);
  populateSelect(el("ocrProfile"), payload.options.ocr_profiles);
  populateSelect(el("exportImageMode"), payload.options.export_image_modes);

  applySettings(emptyProjectSettings());
  renderRuntime(payload.runtime);
  renderModels();
  renderCompaniesWorkspace();
  resetProjectForm();
  switchProjectTab("overview");
  setStatus("Idle");
  updateRunAvailability();

  document.querySelectorAll("[data-pick]").forEach((button) => {
    button.addEventListener("click", () => pickFolder(button.dataset.pick));
  });
  document.querySelectorAll("[data-view-target]").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.viewTarget));
  });
  document.querySelectorAll("[data-project-tab]").forEach((button) => {
    button.addEventListener("click", () => switchProjectTab(button.dataset.projectTab));
  });

  el("sweetAlert").addEventListener("click", (event) => {
    if (event.target.id === "sweetAlert") hideSweetAlert();
  });
  el("editResultModal").addEventListener("click", (event) => {
    if (event.target.id === "editResultModal") closeEditResultModal();
  });
  el("linkedRecordModal").addEventListener("click", (event) => {
    if (event.target.id === "linkedRecordModal") closeLinkedRecordModal();
  });
  document.addEventListener("mouseover", (event) => {
    const target = event.target.closest("[data-tooltip]");
    if (!target) return;
    showRichTooltip(target.dataset.tooltip, event.clientX, event.clientY);
  });
  document.addEventListener("mousemove", (event) => {
    const target = event.target.closest("[data-tooltip]");
    if (!target) {
      hideRichTooltip();
      return;
    }
    showRichTooltip(target.dataset.tooltip, event.clientX, event.clientY);
  });
  document.addEventListener("mouseout", (event) => {
    if (event.target.closest("[data-tooltip]")) {
      hideRichTooltip();
    }
  });
  document.addEventListener("click", (event) => {
    const copyButton = event.target.closest("[data-copy-name]");
    if (!copyButton) return;
    event.preventDefault();
    copyToClipboard(copyButton.dataset.copyName, `Copied "${copyButton.dataset.copyName}"`);
  });

  el("loginButton").addEventListener("click", () => loginOrRegister("login"));
  el("registerButton").addEventListener("click", () => loginOrRegister("register"));
  el("logoutButton").addEventListener("click", logout);
  el("refreshModelsButton").addEventListener("click", loadModels);
  el("newProjectButton").addEventListener("click", () => {
    resetProjectForm();
    switchView("projectEditor");
  });
  el("homeAddProjectButton").addEventListener("click", () => {
    resetProjectForm();
    switchView("projectEditor");
  });
  el("cancelProjectEdit").addEventListener("click", () => {
    switchView("home");
  });
  el("saveProject").addEventListener("click", saveProject);
  el("runJob").addEventListener("click", runJob);
  el("stopJob").addEventListener("click", stopJob);
  el("projectRunNowButton").addEventListener("click", () => {
    switchProjectTab("run");
  });
  el("rebuildReconciliationButton").addEventListener("click", rebuildReconciliation);
  el("editProjectButton").addEventListener("click", () => {
    const project = getSelectedProject();
    if (!project) return;
    applyProject(project);
    switchView("projectEditor");
  });
  el("editProjectButtonInline").addEventListener("click", () => {
    const project = getSelectedProject();
    if (!project) return;
    applyProject(project);
    switchView("projectEditor");
  });
  el("historySelectAll").addEventListener("change", (event) => {
    if (event.target.checked) {
      state.historyTableRows.forEach((item) => state.selectedHistoryIds.add(item.id));
    } else {
      state.historyTableRows.forEach((item) => state.selectedHistoryIds.delete(item.id));
    }
    renderHistoryTable();
  });
  el("historySearch").addEventListener("input", async (event) => {
    state.historySearch = event.target.value;
    state.historyPage = 1;
    await loadHistoryTable();
  });
  el("historyTypeFilter").addEventListener("change", async (event) => {
    state.historyTypeFilter = event.target.value;
    state.historyPage = 1;
    await loadHistoryTable();
  });
  el("historyCompanyFilter").addEventListener("input", async (event) => {
    state.historyCompanyFilter = normalizeCompanyName(event.target.value);
    state.historyPage = 1;
    await loadHistoryTable();
  });
  el("historyConfidenceFilter").addEventListener("change", async (event) => {
    state.historyConfidenceFilter = event.target.value;
    state.historyPage = 1;
    await loadHistoryTable();
  });
  el("documentsSearch").addEventListener("input", async (event) => {
    state.documentsSearch = event.target.value;
    state.documentsPage = 1;
    await loadDocumentsTable();
  });
  el("documentsKindFilter").addEventListener("change", async (event) => {
    state.documentsKindFilter = event.target.value;
    state.documentsPage = 1;
    await loadDocumentsTable();
  });
  el("documentsTypeFilter").addEventListener("change", async (event) => {
    state.documentsTypeFilter = event.target.value;
    state.documentsPage = 1;
    await loadDocumentsTable();
  });
  el("documentsConfidenceFilter").addEventListener("change", async (event) => {
    state.documentsConfidenceFilter = event.target.value;
    state.documentsPage = 1;
    await loadDocumentsTable();
  });
  el("documentsMatchFilter").addEventListener("change", async (event) => {
    state.documentsMatchFilter = event.target.value;
    state.documentsPage = 1;
    await loadDocumentsTable();
  });
  el("resourcesSearch").addEventListener("input", async (event) => {
    state.resourcesSearch = event.target.value;
    state.resourcesPage = 1;
    state.resourceDetailPage = 1;
    state.selectedResourceKey = "";
    await loadResourcesTable();
  });
  el("resourcesKindFilter").addEventListener("change", async (event) => {
    state.resourcesKindFilter = event.target.value;
    state.resourcesPage = 1;
    state.resourceDetailPage = 1;
    state.selectedResourceKey = "";
    await loadResourcesTable();
  });
  el("resourcesResetFilters").addEventListener("click", async () => {
    state.resourcesSearch = "";
    state.resourcesKindFilter = "";
    state.resourcesPage = 1;
    state.resourceDetailPage = 1;
    state.selectedResourceKey = "";
    el("resourcesSearch").value = "";
    el("resourcesKindFilter").value = "";
    await loadResourcesTable();
  });
  el("reconciliationSearch").addEventListener("input", (event) => {
    state.reconciliationSearch = event.target.value;
    state.reconciliationPage = 1;
    loadReconciliationQueue();
  });
  el("reconciliationStatusFilter").addEventListener("change", (event) => {
    state.reconciliationStatusFilter = event.target.value;
    state.reconciliationPage = 1;
    loadReconciliationQueue();
  });
  el("reconciliationBankFilter").addEventListener("change", (event) => {
    state.reconciliationBankFilter = event.target.value;
    state.reconciliationPage = 1;
    loadReconciliationQueue();
  });
  el("reconciliationSort").addEventListener("change", (event) => {
    state.reconciliationSort = event.target.value;
    state.reconciliationPage = 1;
    loadReconciliationQueue();
  });
  el("reconciliationResetFilters").addEventListener("click", () => {
    state.reconciliationSearch = "";
    state.reconciliationStatusFilter = "attention";
    state.reconciliationBankFilter = "";
    state.reconciliationSort = "priority";
    state.reconciliationPage = 1;
    el("reconciliationSearch").value = "";
    el("reconciliationStatusFilter").value = "attention";
    el("reconciliationBankFilter").value = "";
    el("reconciliationSort").value = "priority";
    loadReconciliationQueue();
  });
  el("documentsResetFilters").addEventListener("click", async () => {
    state.documentsSearch = "";
    state.documentsKindFilter = "";
    state.documentsTypeFilter = "";
    state.documentsConfidenceFilter = "";
    state.documentsMatchFilter = "";
    state.documentsPage = 1;
    el("documentsSearch").value = "";
    el("documentsKindFilter").value = "";
    el("documentsTypeFilter").value = "";
    el("documentsConfidenceFilter").value = "";
    el("documentsMatchFilter").value = "";
    await loadDocumentsTable();
  });
  el("historyResetFilters").addEventListener("click", async () => {
    state.historySearch = "";
    state.historyTypeFilter = "";
    state.historyCompanyFilter = "";
    state.historyConfidenceFilter = "";
    state.historyPage = 1;
    el("historySearch").value = "";
    el("historyTypeFilter").value = "";
    el("historyCompanyFilter").value = "";
    el("historyConfidenceFilter").value = "";
    await loadHistoryTable();
  });
  el("dashboardSearch").addEventListener("input", (event) => {
    state.dashboardSearch = event.target.value;
    state.dashboardDrilldownPage = 1;
    debounce("dashboardSearch", 220, () => loadDashboardAnalytics(true));
  });
  el("dashboardDateFrom").addEventListener("change", (event) => {
    state.dashboardDateFrom = event.target.value;
    state.dashboardDrilldownPage = 1;
    loadDashboardAnalytics(true);
  });
  el("dashboardDateTo").addEventListener("change", (event) => {
    state.dashboardDateTo = event.target.value;
    state.dashboardDrilldownPage = 1;
    loadDashboardAnalytics(true);
  });
  el("dashboardDirectionFilter").addEventListener("change", (event) => {
    state.dashboardDirectionFilter = event.target.value;
    state.dashboardDrilldownPage = 1;
    loadDashboardAnalytics(true);
  });
  el("dashboardMatchFilter").addEventListener("change", (event) => {
    state.dashboardMatchFilter = event.target.value;
    state.dashboardDrilldownPage = 1;
    loadDashboardAnalytics(true);
  });
  el("dashboardBankFilter").addEventListener("change", (event) => {
    state.dashboardBankFilter = event.target.value;
    state.dashboardDrilldownPage = 1;
    loadDashboardAnalytics(true);
  });
  el("dashboardResetFilters").addEventListener("click", () => {
    state.dashboardSearch = "";
    state.dashboardDateFrom = "";
    state.dashboardDateTo = "";
    state.dashboardDirectionFilter = "";
    state.dashboardMatchFilter = "";
    state.dashboardBankFilter = "";
    state.dashboardDrilldownTitle = "All Filtered Bank Rows";
    state.dashboardDrilldownSubtitle = "Current dashboard dataset after applying filters.";
    state.dashboardDrilldownMode = "all";
    state.dashboardDrilldownValue = "";
    state.dashboardDrilldownSearch = "";
    state.dashboardDrilldownDirection = "";
    state.dashboardDrilldownMatch = "";
    state.dashboardDrilldownPage = 1;
    el("dashboardSearch").value = "";
    el("dashboardDateFrom").value = "";
    el("dashboardDateTo").value = "";
    el("dashboardDirectionFilter").value = "";
    el("dashboardMatchFilter").value = "";
    el("dashboardBankFilter").value = "";
    el("overviewDrilldownSearch").value = "";
    el("overviewDrilldownDirection").value = "";
    el("overviewDrilldownMatch").value = "";
    loadDashboardAnalytics(true);
  });
  el("overviewDrilldownSearch").addEventListener("input", (event) => {
    state.dashboardDrilldownSearch = event.target.value;
    state.dashboardDrilldownPage = 1;
    debounce("dashboardDrilldownSearch", 220, () => loadDashboardAnalytics(false));
  });
  el("overviewDrilldownDirection").addEventListener("change", (event) => {
    state.dashboardDrilldownDirection = event.target.value;
    state.dashboardDrilldownPage = 1;
    loadDashboardAnalytics(false);
  });
  el("overviewDrilldownMatch").addEventListener("change", (event) => {
    state.dashboardDrilldownMatch = event.target.value;
    state.dashboardDrilldownPage = 1;
    loadDashboardAnalytics(false);
  });
  el("overviewDrilldownResetFilters").addEventListener("click", () => {
    state.dashboardDrilldownSearch = "";
    state.dashboardDrilldownDirection = "";
    state.dashboardDrilldownMatch = "";
    state.dashboardDrilldownPage = 1;
    el("overviewDrilldownSearch").value = "";
    el("overviewDrilldownDirection").value = "";
    el("overviewDrilldownMatch").value = "";
    loadDashboardAnalytics(false);
  });
  el("overviewDrilldownPrevPage").addEventListener("click", () => {
    if (state.dashboardDrilldownPage > 1) {
      state.dashboardDrilldownPage -= 1;
      loadDashboardAnalytics(false);
    }
  });
  el("overviewDrilldownNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Number(state.dashboardDrilldownPagination?.total_pages || 1));
    if (state.dashboardDrilldownPage < totalPages) {
      state.dashboardDrilldownPage += 1;
      loadDashboardAnalytics(false);
    }
  });
  el("historyPrevPage").addEventListener("click", async () => {
    if (state.historyPage > 1) {
      state.historyPage -= 1;
      await loadHistoryTable();
    }
  });
  el("historyNextPage").addEventListener("click", async () => {
    const totalPages = state.historyTablePagination.total_pages || 1;
    if (state.historyPage < totalPages) {
      state.historyPage += 1;
      await loadHistoryTable();
    }
  });
  el("documentsPrevPage").addEventListener("click", async () => {
    if (state.documentsPage > 1) {
      state.documentsPage -= 1;
      await loadDocumentsTable();
    }
  });
  el("documentsNextPage").addEventListener("click", async () => {
    const totalPages = state.documentsTablePagination.total_pages || 1;
    if (state.documentsPage < totalPages) {
      state.documentsPage += 1;
      await loadDocumentsTable();
    }
  });
  el("resourcesPrevPage").addEventListener("click", async () => {
    if (state.resourcesPage > 1) {
      state.resourcesPage -= 1;
      await loadResourcesTable();
    }
  });
  el("resourcesNextPage").addEventListener("click", async () => {
    const totalPages = state.resourcesPagination.total_pages || 1;
    if (state.resourcesPage < totalPages) {
      state.resourcesPage += 1;
      await loadResourcesTable();
    }
  });
  el("resourceDetailPrevPage").addEventListener("click", () => {
    if (state.resourceDetailPage > 1) {
      state.resourceDetailPage -= 1;
      loadResourceDetail();
    }
  });
  el("resourceDetailNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Number(state.resourceDetailPagination?.total_pages || 1));
    if (state.resourceDetailPage < totalPages) {
      state.resourceDetailPage += 1;
      loadResourceDetail();
    }
  });
  el("resourceRerunButton").addEventListener("click", async () => {
    const sourcePath = el("resourceRerunButton").dataset.sourcePath || "";
    if (!state.selectedProjectId || !sourcePath) {
      showSweetAlert("Resource Required", "Select a processed resource first.", "error");
      return;
    }
    try {
      showRunProgress("Preparing Rerun", "Staging the selected source for an isolated rerun.");
      const response = await fetchJson(`/api/projects/${state.selectedProjectId}/rerun-resource`, {
        method: "POST",
        body: JSON.stringify({ source_path: sourcePath }),
      });
      state.jobId = response.job_id;
      setStatus("queued");
      el("logs").textContent = "";
      el("resultsTable").querySelector("tbody").innerHTML = "";
      el("resultsMeta").textContent = "Isolated rerun queued.";
      switchView("projectDetail");
      switchProjectTab("run");
      if (state.pollTimer) clearInterval(state.pollTimer);
      state.pollTimer = setInterval(pollJob, 1500);
      updateRunAvailability();
      pollJob();
    } catch (error) {
      hideRunProgress();
      showSweetAlert("Rerun Error", error.message, "error");
    }
  });
  el("closeExportAccountingButton").addEventListener("click", exportCloseAccounting);
  el("closeExportUnresolvedButton").addEventListener("click", exportCloseUnresolved);
  el("closeExportPackageButton").addEventListener("click", exportClosePackage);
  el("accountingExportPreset").addEventListener("change", (event) => {
    state.accountingExportPreset = event.target.value;
    renderCloseWorkspace();
  });
  el("foundationAddAccountButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/accounts`, {
      method: "POST",
      body: JSON.stringify({
        code: el("foundationAccountCode").value.trim(),
        name: el("foundationAccountName").value.trim(),
        account_type: el("foundationAccountType").value,
        subtype: el("foundationAccountSubtype").value.trim(),
        is_active: el("foundationAccountActive").checked,
      }),
    });
    el("foundationAccountCode").value = "";
    el("foundationAccountName").value = "";
    el("foundationAccountSubtype").value = "";
    el("foundationAccountActive").checked = true;
    await loadAccountingFoundation();
  });
  el("seedConstructionAccountsButton").addEventListener("click", async () => {
    const response = await fetchJson(`/api/companies/current/accounts/seed-construction`, {
      method: "POST",
    });
    await loadAccountingFoundation();
    showSweetAlert("Construction COA Ready", `${response.created_count || 0} accounts were added.`, "success");
  });
  el("foundationAddPeriodButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/periods`, {
      method: "POST",
      body: JSON.stringify({
        name: el("foundationPeriodName").value.trim(),
        start_date: el("foundationPeriodStart").value,
        end_date: el("foundationPeriodEnd").value,
        status: el("foundationPeriodStatus").value,
      }),
    });
    el("foundationPeriodName").value = "";
    el("foundationPeriodStart").value = "";
    el("foundationPeriodEnd").value = "";
    el("foundationPeriodStatus").value = "open";
    state.accountingPeriodsPage = 1;
    await loadAccountingFoundation();
  });
  el("foundationSeedQuarterPeriodsButton").addEventListener("click", async () => {
    const year = Number(el("foundationQuarterSeedYear").value || 0);
    if (!year) {
      showSweetAlert("Year Required", "Enter a year to seed quarterly periods.", "error");
      return;
    }
    const response = await fetchJson(`/api/companies/current/periods/seed-quarters`, {
      method: "POST",
      body: JSON.stringify({
        year,
        status: el("foundationQuarterSeedStatus").value,
      }),
    });
    state.accountingPeriodsPage = 1;
    await loadAccountingFoundation();
    showSweetAlert("Quarter Periods Ready", `${response.created_count || 0} quarterly periods were added.`, "success");
  });
  el("foundationSeedMissingPeriodsButton").addEventListener("click", async () => {
    const response = await fetchJson(`/api/companies/current/periods/seed-missing-drafts`, {
      method: "POST",
      body: JSON.stringify({
        status: el("foundationQuarterSeedStatus").value,
      }),
    });
    state.accountingPeriodsPage = 1;
    await loadAccountingFoundation();
    const undatedCount = Number(response.undated_count || 0);
    const undatedHint = undatedCount
      ? ` ${undatedCount} draft${undatedCount === 1 ? "" : "s"} still have no usable date, so no quarter could be created for them.${(response.undated_samples || []).length ? ` Examples: ${(response.undated_samples || []).slice(0, 3).join(", ")}.` : ""}`
      : "";
    showSweetAlert(
      "Missing Quarters Created",
      `${response.created_count || 0} quarter periods were created for uncovered draft dates.${undatedHint}`,
      "success",
    );
  });
  el("foundationGenerateDraftsButton").addEventListener("click", async () => {
    await Promise.all([loadCompanyAccountingRules(), loadProjectRulesRemote(), loadAccountingFoundation()]);
    showSweetAlert("Drafts Refreshed", "Existing parsed records were re-evaluated against your accounting rules and journal drafts were rebuilt.", "success");
  });
  el("foundationPostAllDraftsButton").addEventListener("click", async () => {
    try {
      const response = await fetchJson(`/api/companies/current/journal-post`, {
        method: "POST",
        body: JSON.stringify({ document_ids: [] }),
      });
      state.journalDraftsPage = 1;
      await loadAccountingFoundation();
      const skippedUndatedCount = Number(response.skipped_undated_count || 0);
      const skippedHint = skippedUndatedCount
        ? ` ${skippedUndatedCount} undated draft${skippedUndatedCount === 1 ? "" : "s"} were skipped and need date correction before they can post.`
        : "";
      showSweetAlert("Journals Posted", `${response.created_count || 0} journal entries were posted.${skippedHint}`, "success");
    } catch (error) {
      const blockedDrafts = (state.journalDrafts || []).filter((item) => !item.posting_allowed);
      const missingPeriodDates = blockedDrafts
        .filter((item) => (item.period_status || "") === "missing" && item.date)
        .map((item) => item.date);
      const dateHint = missingPeriodDates.length
        ? ` Missing dates include ${missingPeriodDates.slice(0, 3).join(", ")}${missingPeriodDates.length > 3 ? "..." : ""}.`
        : "";
      const message = String(error?.message || "");
      if (message.includes("No accounting period covers this draft date")) {
        const undatedDrafts = blockedDrafts.filter((item) => !item.date || item.date === "Unknown");
        const undatedHint = undatedDrafts.length
          ? ` ${undatedDrafts.length} blocked draft${undatedDrafts.length === 1 ? "" : "s"} still have no usable date, so periods cannot be created for them until their dates are corrected.`
          : "";
        showSweetAlert(
          "Accounting Period Required",
          `At least one draft date is outside your configured accounting periods.${dateHint}${undatedHint} Add or seed periods that cover those dates, then try posting again.`,
          "error",
        );
        return;
      }
      showSweetAlert("Posting Error", message || "Unable to post journal drafts.", "error");
    }
  });
  el("foundationPeriodsPrevPage").addEventListener("click", () => {
    if (state.accountingPeriodsPage > 1) {
      state.accountingPeriodsPage -= 1;
      renderAccountingFoundation();
    }
  });
  el("foundationPeriodsNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Math.ceil(((state.accountingPeriods || []).filter((item) => {
      if (state.accountingPeriodsStatusFilter && (item.status || "") !== state.accountingPeriodsStatusFilter) return false;
      const search = (state.accountingPeriodsSearch || "").trim().toLowerCase();
      if (!search) return true;
      return [item.name || "", item.start_date || "", item.end_date || "", item.status || ""].join(" ").toLowerCase().includes(search);
    })).length / 10));
    if (state.accountingPeriodsPage < totalPages) {
      state.accountingPeriodsPage += 1;
      renderAccountingFoundation();
    }
  });
  el("foundationJournalPrevPage").addEventListener("click", () => {
    if (state.journalDraftsPage > 1) {
      state.journalDraftsPage -= 1;
      renderAccountingFoundation();
    }
  });
  el("foundationJournalNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Math.ceil(((state.journalDrafts || []).filter((item) => {
      const postingState = item.posting_allowed ? "allowed" : ((item.period_status || "") === "missing" ? "missing" : "blocked");
      if (state.journalDraftsStatusFilter && postingState !== state.journalDraftsStatusFilter) return false;
      const search = (state.journalDraftsSearch || "").trim().toLowerCase();
      if (!search) return true;
      return [
        item.date || "",
        item.reference || "",
        item.vendor || "",
        item.memo || "",
        item.amount || "",
        item.period_name || "",
        item.rule_keyword || "",
      ].join(" ").toLowerCase().includes(search);
    })).length / 12));
    if (state.journalDraftsPage < totalPages) {
      state.journalDraftsPage += 1;
      renderAccountingFoundation();
    }
  });
  el("foundationPeriodsSearch").addEventListener("input", (event) => {
    state.accountingPeriodsSearch = event.target.value;
    state.accountingPeriodsPage = 1;
    renderAccountingFoundation();
  });
  el("foundationPeriodsStatusFilter").addEventListener("change", (event) => {
    state.accountingPeriodsStatusFilter = event.target.value;
    state.accountingPeriodsPage = 1;
    renderAccountingFoundation();
  });
  el("foundationPeriodsSort").addEventListener("change", (event) => {
    state.accountingPeriodsSort = event.target.value;
    state.accountingPeriodsPage = 1;
    renderAccountingFoundation();
  });
  el("foundationPeriodsResetFilters").addEventListener("click", () => {
    state.accountingPeriodsSearch = "";
    state.accountingPeriodsStatusFilter = "";
    state.accountingPeriodsSort = "start_desc";
    state.accountingPeriodsPage = 1;
    renderAccountingFoundation();
  });
  el("foundationJournalSearch").addEventListener("input", (event) => {
    state.journalDraftsSearch = event.target.value;
    state.journalDraftsPage = 1;
    renderAccountingFoundation();
  });
  el("foundationJournalStatusFilter").addEventListener("change", (event) => {
    state.journalDraftsStatusFilter = event.target.value;
    state.journalDraftsPage = 1;
    renderAccountingFoundation();
  });
  el("foundationJournalSort").addEventListener("change", (event) => {
    state.journalDraftsSort = event.target.value;
    state.journalDraftsPage = 1;
    renderAccountingFoundation();
  });
  el("foundationJournalResetFilters").addEventListener("click", () => {
    state.journalDraftsSearch = "";
    state.journalDraftsStatusFilter = "";
    state.journalDraftsSort = "date_desc";
    state.journalDraftsPage = 1;
    renderAccountingFoundation();
  });
  el("foundationEntriesSearch").addEventListener("input", (event) => {
    state.journalEntriesSearch = event.target.value;
    state.journalEntriesPage = 1;
    renderAccountingFoundation();
  });
  el("foundationEntriesStatusFilter").addEventListener("change", (event) => {
    state.journalEntriesStatusFilter = event.target.value;
    state.journalEntriesPage = 1;
    renderAccountingFoundation();
  });
  el("foundationEntriesSort").addEventListener("change", (event) => {
    state.journalEntriesSort = event.target.value;
    state.journalEntriesPage = 1;
    renderAccountingFoundation();
  });
  el("foundationEntriesResetFilters").addEventListener("click", () => {
    state.journalEntriesSearch = "";
    state.journalEntriesStatusFilter = "";
    state.journalEntriesSort = "date_desc";
    state.journalEntriesPage = 1;
    renderAccountingFoundation();
  });
  el("foundationEntriesPrevPage").addEventListener("click", () => {
    if (state.journalEntriesPage > 1) {
      state.journalEntriesPage -= 1;
      renderAccountingFoundation();
    }
  });
  el("foundationEntriesNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Math.ceil(((state.journalEntries || []).filter((item) => {
      if (state.journalEntriesStatusFilter && (item.status || "") !== state.journalEntriesStatusFilter) return false;
      const search = (state.journalEntriesSearch || "").trim().toLowerCase();
      if (!search) return true;
      return [item.entry_date || "", item.reference || "", item.memo || "", item.status || ""].join(" ").toLowerCase().includes(search);
    })).length / 10));
    if (state.journalEntriesPage < totalPages) {
      state.journalEntriesPage += 1;
      renderAccountingFoundation();
    }
  });
  document.querySelectorAll(".manual-journal-debit, .manual-journal-credit").forEach((input) => {
    input.addEventListener("input", updateManualJournalTotals);
  });
  el("postManualJournalButton").addEventListener("click", async () => {
    const payload = {
      entry_date: el("manualJournalDate").value,
      reference: el("manualJournalReference").value.trim(),
      memo: el("manualJournalMemo").value.trim(),
      lines: manualJournalRows(),
    };
    const response = await fetchJson(`/api/companies/current/manual-journal`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    await loadAccountingFoundation();
    showSweetAlert("Manual Journal Posted", `Journal entry ${response.entry?.reference || response.entry?.id || ""} posted successfully.`, "success");
  });
  el("foundationLedgerProjectFilter").addEventListener("change", (event) => {
    state.ledgerProjectFilter = event.target.value;
    if (state.ledgerAccountCode) {
      loadCompanyLedger(state.ledgerAccountCode);
    }
  });
  el("foundationLedgerCostCenterFilter").addEventListener("change", (event) => {
    state.ledgerCostCenterFilter = event.target.value;
    if (state.ledgerAccountCode) {
      loadCompanyLedger(state.ledgerAccountCode);
    }
  });
  el("foundationLedgerSearch").addEventListener("input", (event) => {
    state.ledgerSearch = event.target.value;
    state.ledgerPage = 1;
    renderAccountingFoundation();
  });
  el("foundationLedgerSort").addEventListener("change", (event) => {
    state.ledgerSort = event.target.value;
    state.ledgerPage = 1;
    renderAccountingFoundation();
  });
  el("foundationLedgerResetFilters").addEventListener("click", () => {
    state.ledgerProjectFilter = "";
    state.ledgerCostCenterFilter = "";
    state.ledgerSearch = "";
    state.ledgerSort = "date_desc";
    state.ledgerPage = 1;
    el("foundationLedgerProjectFilter").value = "";
    el("foundationLedgerCostCenterFilter").value = "";
    if (state.ledgerAccountCode) {
      loadCompanyLedger(state.ledgerAccountCode);
    } else {
      renderAccountingFoundation();
    }
  });
  el("foundationLedgerResetSearch").addEventListener("click", () => {
    state.ledgerSearch = "";
    state.ledgerSort = "date_desc";
    state.ledgerPage = 1;
    renderAccountingFoundation();
  });
  el("foundationLedgerPrevPage").addEventListener("click", () => {
    if (state.ledgerPage > 1) {
      state.ledgerPage -= 1;
      renderAccountingFoundation();
    }
  });
  el("foundationLedgerNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Math.ceil(((state.ledgerRows || []).filter((item) => {
      const search = (state.ledgerSearch || "").trim().toLowerCase();
      if (!search) return true;
      return [
        item.entry_date || "",
        item.reference || "",
        item.memo || "",
        item.project_code || "",
        item.cost_center || "",
        item.debit || "",
        item.credit || "",
        item.balance || "",
      ].join(" ").toLowerCase().includes(search);
    })).length / 12));
    if (state.ledgerPage < totalPages) {
      state.ledgerPage += 1;
      renderAccountingFoundation();
    }
  });
  el("saveCompanySettingsButton").addEventListener("click", async () => {
    const response = await fetchJson(`/api/companies/current`, {
      method: "PUT",
      body: JSON.stringify({
        name: el("companySettingsName").value.trim(),
        base_currency: el("companySettingsCurrency").value.trim(),
        fiscal_year_start_month: Number(el("companySettingsFiscalMonth").value || 1),
        vat_registration_number: el("companySettingsVatNumber").value.trim(),
        vat_rate: el("companySettingsVatRate").value.trim(),
      }),
    });
    state.companySettings = response.company || null;
    if (state.currentUser && response.company?.name) {
      state.currentUser.company_name = response.company.name;
    }
    await loadCompanies();
    renderCompaniesWorkspace();
    renderAccountingFoundation();
    showSweetAlert("Company Saved", "Company accounting settings updated.", "success");
  });
  el("addCompanyButton").addEventListener("click", async () => {
    const name = el("newCompanyName").value.trim();
    if (!name) {
      showSweetAlert("Company Name Required", "Enter a company name before adding it.", "error");
      return;
    }
    const response = await fetchJson(`/api/companies`, {
      method: "POST",
      body: JSON.stringify({ name }),
    });
    el("newCompanyName").value = "";
    if (state.currentUser) {
      state.currentUser.company_id = response.company?.id || state.currentUser.company_id;
      state.currentUser.company_name = response.company?.name || state.currentUser.company_name;
    }
    invalidateCompanyPaneCache();
    await runCompanyRenderBatch(async () => {
      await loadCompanyBaseData();
      await ensureCompanyPaneData(state.companiesPane, true);
    });
    showSweetAlert("Company Added", "The new company is now active.", "success");
  });
  el("seedCompanyAccountingRulesButton").addEventListener("click", async () => {
    const response = await fetchJson(`/api/companies/current/accounting-rules/seed`, {
      method: "POST",
    });
    await loadCompanyAccountingRules();
    showSweetAlert("Company Rules Seeded", `${response.created_count || 0} company rules were added from your existing data.`, "success");
  });
  el("addCompanyAccountingRuleButton").addEventListener("click", async () => {
    const keyword = el("companyRuleKeyword").value.trim();
    if (!keyword) {
      showSweetAlert("Keyword Required", "Enter a keyword before adding the company rule.", "error");
      return;
    }
    await fetchJson(`/api/companies/current/accounting-rules`, {
      method: "POST",
      body: JSON.stringify({
        keyword,
        source_type: el("companyRuleSourceType").value,
        category: el("companyRuleCategory").value.trim(),
        subcategory: el("companyRuleSubcategory").value.trim(),
        account_code: el("companyRuleAccountCode").value.trim(),
        offset_account_code: el("companyRuleOffsetAccountCode").value.trim(),
        payment_method: el("companyRulePaymentMethod").value.trim(),
        vat_flag: el("companyRuleVatFlag").checked,
        auto_post: el("companyRuleAutoPost").checked,
      }),
    });
    el("companyRuleKeyword").value = "";
    el("companyRuleSourceType").value = "";
    el("companyRuleCategory").value = "";
    el("companyRuleSubcategory").value = "";
    el("companyRuleAccountCode").value = "";
    el("companyRuleOffsetAccountCode").value = "";
    el("companyRulePaymentMethod").value = "";
    el("companyRuleVatFlag").checked = false;
    el("companyRuleAutoPost").checked = true;
    await loadCompanyAccountingRules();
  });
  el("addCostCenterButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/dimensions`, {
      method: "POST",
      body: JSON.stringify({
        dimension_type: "cost_center",
        code: el("companyCostCenterCode").value.trim(),
        name: el("companyCostCenterName").value.trim(),
        is_active: true,
      }),
    });
    el("companyCostCenterCode").value = "";
    el("companyCostCenterName").value = "";
    await Promise.all([loadCompanyDimensions(), loadCompanyActivity()]);
    renderAccountingFoundation();
  });
  el("addCostCodeButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/dimensions`, {
      method: "POST",
      body: JSON.stringify({
        dimension_type: "cost_code",
        code: el("companyCostCodeCode").value.trim(),
        name: el("companyCostCodeName").value.trim(),
        is_active: true,
      }),
    });
    el("companyCostCodeCode").value = "";
    el("companyCostCodeName").value = "";
    await Promise.all([loadCompanyDimensions(), loadCompanyActivity()]);
    renderTags();
    await loadCompanyJobCostingSummary();
  });
  el("createCompanyBillingEventButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/billing-events`, {
      method: "POST",
      body: JSON.stringify({
        project_id: Number(el("companyBillingProjectSelect").value || 0),
        event_type: el("companyBillingEventType").value,
        label: el("companyBillingLabel").value.trim(),
        event_date: el("companyBillingDate").value,
        amount: el("companyBillingAmount").value.trim(),
        status: el("companyBillingStatus").value,
        note: el("companyBillingNote").value.trim(),
      }),
    });
    el("companyBillingLabel").value = "";
    el("companyBillingDate").value = "";
    el("companyBillingAmount").value = "";
    el("companyBillingNote").value = "";
    await Promise.all([loadCompanyBillingEvents(), loadCompanyJobCostingSummary(), loadCompanyActivity()]);
    showSweetAlert("Billing Event Added", "Project billing event stored.", "success");
  });
  el("createCompanyPoButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/purchase-orders`, {
      method: "POST",
      body: JSON.stringify({
        project_id: Number(el("companyPoProjectSelect").value || 0),
        supplier_party_id: el("companyPoSupplierSelect").value ? Number(el("companyPoSupplierSelect").value) : null,
        cost_code: el("companyPoCostCode").value || "",
        po_number: el("companyPoNumber").value.trim(),
        po_date: el("companyPoDate").value,
        amount: el("companyPoAmount").value.trim(),
        status: el("companyPoStatus").value,
        note: el("companyPoNote").value.trim(),
      }),
    });
    el("companyPoNumber").value = "";
    el("companyPoDate").value = "";
    el("companyPoAmount").value = "";
    el("companyPoNote").value = "";
    await Promise.all([loadCompanyPurchaseOrders(), loadCompanyJobCostingSummary(), loadCompanyActivity()]);
    showSweetAlert("Purchase Order Added", "Committed cost record stored.", "success");
  });
  el("createCompanyReceiptButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/receipts`, {
      method: "POST",
      body: JSON.stringify({
        purchase_order_id: Number(el("companyReceiptPoSelect").value || 0),
        receipt_type: el("companyReceiptType").value,
        receipt_number: el("companyReceiptNumber").value.trim(),
        receipt_date: el("companyReceiptDate").value,
        amount: el("companyReceiptAmount").value.trim(),
        status: el("companyReceiptStatus").value,
        note: el("companyReceiptNote").value.trim(),
      }),
    });
    el("companyReceiptNumber").value = "";
    el("companyReceiptDate").value = "";
    el("companyReceiptAmount").value = "";
    el("companyReceiptNote").value = "";
    await Promise.all([loadCompanyReceipts(), loadCompanyProcurementSummary(), loadCompanyActivity()]);
    showSweetAlert("Receipt Added", "Goods or service receipt stored.", "success");
  });
  el("companiesProcurementExceptionReviewFilter").addEventListener("change", async (event) => {
    state.procurementExceptionReviewFilter = event.target.value || "";
    await loadCompanyProcurementExceptions();
  });
  el("companiesProcurementExceptionMineOnly").addEventListener("change", async (event) => {
    state.procurementExceptionMineOnly = Boolean(event.target.checked);
    await loadCompanyProcurementExceptions();
  });
  el("companiesProcurementExceptionReset").addEventListener("click", async () => {
    state.procurementExceptionReviewFilter = "";
    state.procurementExceptionMineOnly = false;
    await loadCompanyProcurementExceptions();
  });
  el("addSupplierButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/parties`, {
      method: "POST",
      body: JSON.stringify({
        party_type: "supplier",
        name: el("companySupplierName").value.trim(),
        tax_registration_number: el("companySupplierTrn").value.trim(),
        contact_email: el("companySupplierEmail").value.trim(),
        contact_phone: el("companySupplierPhone").value.trim(),
        default_account_code: el("companySupplierDefaultAccount").value,
        payment_terms_days: Number(el("companySupplierTerms").value || 30),
      }),
    });
    ["companySupplierName","companySupplierTrn","companySupplierEmail","companySupplierPhone","companySupplierTerms"].forEach((id) => { el(id).value = ""; });
    el("companySupplierDefaultAccount").value = "";
    await Promise.all([loadCompanyParties(), loadCompanyAging(), loadCompanyActivity()]);
  });
  el("addCustomerButton").addEventListener("click", async () => {
    await fetchJson(`/api/companies/current/parties`, {
      method: "POST",
      body: JSON.stringify({
        party_type: "customer",
        name: el("companyCustomerName").value.trim(),
        tax_registration_number: el("companyCustomerTrn").value.trim(),
        contact_email: el("companyCustomerEmail").value.trim(),
        contact_phone: el("companyCustomerPhone").value.trim(),
        default_account_code: el("companyCustomerDefaultAccount").value,
        payment_terms_days: Number(el("companyCustomerTerms").value || 30),
      }),
    });
    ["companyCustomerName","companyCustomerTrn","companyCustomerEmail","companyCustomerPhone","companyCustomerTerms"].forEach((id) => { el(id).value = ""; });
    el("companyCustomerDefaultAccount").value = "";
    await Promise.all([loadCompanyParties(), loadCompanyAging(), loadCompanyActivity()]);
  });
  el("companyAllocationType").addEventListener("change", async (event) => {
    state.companyAllocationType = event.target.value || "payable";
    if (el("companyAllocationAmount")) el("companyAllocationAmount").value = "";
    if (el("companyAllocationNote")) el("companyAllocationNote").value = "";
    await loadCompanyAllocationWorkspace();
  });
  el("createCompanyAllocationButton").addEventListener("click", async () => {
    const response = await fetchJson(`/api/companies/current/allocations`, {
      method: "POST",
      body: JSON.stringify({
        allocation_type: state.companyAllocationType || "payable",
        target_document_id: Number(el("companyAllocationTargetSelect").value || 0),
        payment_document_id: Number(el("companyAllocationPaymentSelect").value || 0),
        amount: el("companyAllocationAmount").value.trim(),
        note: el("companyAllocationNote").value.trim(),
      }),
    });
    el("companyAllocationAmount").value = "";
    el("companyAllocationNote").value = "";
    await Promise.all([loadCompanyAging(), loadCompanyApDocuments(), loadCompanyArDocuments(), loadCompanyAllocationWorkspace(), loadCompanyActivity()]);
    showSweetAlert("Allocation Created", `Allocation ${response.allocation?.id || ""} saved.`, "success");
  });
  let apDocsSearchTimer = null;
  el("companiesApDocsSearch").addEventListener("input", (event) => {
    state.apDocsSearch = event.target.value || "";
    state.apDocsPagination.page = 1;
    clearTimeout(apDocsSearchTimer);
    apDocsSearchTimer = setTimeout(() => loadCompanyApDocuments(), 250);
  });
  let arDocsSearchTimer = null;
  el("companiesArDocsSearch").addEventListener("input", (event) => {
    state.arDocsSearch = event.target.value || "";
    state.arDocsPagination.page = 1;
    clearTimeout(arDocsSearchTimer);
    arDocsSearchTimer = setTimeout(() => loadCompanyArDocuments(), 250);
  });
  el("companiesApDocsPrev").addEventListener("click", () => {
    if ((state.apDocsPagination.page || 1) > 1) {
      state.apDocsPagination.page -= 1;
      loadCompanyApDocuments();
    }
  });
  el("companiesApDocsNext").addEventListener("click", () => {
    if ((state.apDocsPagination.page || 1) < (state.apDocsPagination.total_pages || 1)) {
      state.apDocsPagination.page += 1;
      loadCompanyApDocuments();
    }
  });
  el("companiesArDocsPrev").addEventListener("click", () => {
    if ((state.arDocsPagination.page || 1) > 1) {
      state.arDocsPagination.page -= 1;
      loadCompanyArDocuments();
    }
  });
  el("companiesArDocsNext").addEventListener("click", () => {
    if ((state.arDocsPagination.page || 1) < (state.arDocsPagination.total_pages || 1)) {
      state.arDocsPagination.page += 1;
      loadCompanyArDocuments();
    }
  });
  let companyProjectsSearchTimer = null;
  el("companiesProjectsSearch").addEventListener("input", (event) => {
    state.companyProjectsSearch = event.target.value || "";
    clearTimeout(companyProjectsSearchTimer);
    companyProjectsSearchTimer = setTimeout(() => renderCompaniesWorkspace(), 180);
  });
  el("companiesProjectsStatusFilter").addEventListener("change", (event) => {
    state.companyProjectsStatusFilter = event.target.value || "";
    renderCompaniesWorkspace();
  });
  el("companiesProjectsResetFilters").addEventListener("click", () => {
    state.companyProjectsSearch = "";
    state.companyProjectsStatusFilter = "";
    renderCompaniesWorkspace();
  });
  el("reconciliationPrevPage").addEventListener("click", () => {
    if (state.reconciliationPage > 1) {
      state.reconciliationPage -= 1;
      loadReconciliationQueue();
    }
  });
  el("reconciliationNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Number(state.reconciliationPagination?.total_pages || 1));
    if (state.reconciliationPage < totalPages) {
      state.reconciliationPage += 1;
      loadReconciliationQueue();
    }
  });
  el("reconciliationOpenLinked").addEventListener("click", () => {
    const record = bankTransactionRecords().find((item) => item.id === state.reconciliationSelectedId);
    if (record) {
      openLinkedRecordModal(record);
    }
  });
  el("reconciliationMarkReviewed").addEventListener("click", async () => {
    if (!state.reconciliationSelectedId) return;
    const response = await fetchJson(`/api/documents/${state.reconciliationSelectedId}/review`, {
      method: "PUT",
      body: JSON.stringify({ review_state: "reviewed", review_note: "Reviewed from reconciliation workspace." }),
    });
    replaceDocumentInState(response.document);
    await Promise.all([loadReconciliationQueue(), loadReviewQueue()]);
  });
  el("reconciliationMarkNeedsReceipt").addEventListener("click", async () => {
    if (!state.reconciliationSelectedId) return;
    const response = await fetchJson(`/api/documents/${state.reconciliationSelectedId}/review`, {
      method: "PUT",
      body: JSON.stringify({ review_state: "missing_receipt", review_note: "Flagged as missing receipt from reconciliation workspace." }),
    });
    replaceDocumentInState(response.document);
    await Promise.all([loadReconciliationQueue(), loadReviewQueue()]);
  });
  el("reconciliationMarkNotApplicable").addEventListener("click", async () => {
    if (!state.reconciliationSelectedId) return;
    const response = await fetchJson(`/api/documents/${state.reconciliationSelectedId}/review`, {
      method: "PUT",
      body: JSON.stringify({ review_state: "not_applicable", review_note: "Marked not applicable from reconciliation workspace." }),
    });
    replaceDocumentInState(response.document);
    await Promise.all([loadReconciliationQueue(), loadReviewQueue()]);
  });
  el("reviewQueueSearch").addEventListener("input", (event) => {
    state.reviewQueueSearch = event.target.value;
    state.reviewQueuePage = 1;
    loadReviewQueue();
  });
  el("reviewQueueTypeFilter").addEventListener("change", (event) => {
    state.reviewQueueTypeFilter = event.target.value;
    state.reviewQueuePage = 1;
    loadReviewQueue();
  });
  el("reviewQueueSourceFilter").addEventListener("change", (event) => {
    state.reviewQueueSourceFilter = event.target.value;
    state.reviewQueuePage = 1;
    loadReviewQueue();
  });
  el("reviewQueueResetFilters").addEventListener("click", () => {
    state.reviewQueueSearch = "";
    state.reviewQueueTypeFilter = "";
    state.reviewQueueSourceFilter = "";
    state.reviewQueuePage = 1;
    el("reviewQueueSearch").value = "";
    el("reviewQueueTypeFilter").value = "";
    el("reviewQueueSourceFilter").value = "";
    loadReviewQueue();
  });
  el("reviewQueuePrevPage").addEventListener("click", () => {
    if (state.reviewQueuePage > 1) {
      state.reviewQueuePage -= 1;
      loadReviewQueue();
    }
  });
  el("reviewQueueNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Number(state.reviewQueuePagination?.total_pages || 1));
    if (state.reviewQueuePage < totalPages) {
      state.reviewQueuePage += 1;
      loadReviewQueue();
    }
  });
  el("exceptionsSearch").addEventListener("input", (event) => {
    state.exceptionsSearch = event.target.value;
    state.exceptionsPage = 1;
    loadExceptions();
  });
  el("exceptionsTypeFilter").addEventListener("change", (event) => {
    state.exceptionsTypeFilter = event.target.value;
    state.exceptionsPage = 1;
    loadExceptions();
  });
  el("exceptionsResetFilters").addEventListener("click", () => {
    state.exceptionsSearch = "";
    state.exceptionsTypeFilter = "";
    state.exceptionsPage = 1;
    el("exceptionsSearch").value = "";
    el("exceptionsTypeFilter").value = "";
    loadExceptions();
  });
  el("exceptionsPrevPage").addEventListener("click", () => {
    if (state.exceptionsPage > 1) {
      state.exceptionsPage -= 1;
      loadExceptions();
    }
  });
  el("exceptionsNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Number(state.exceptionsPagination?.total_pages || 1));
    if (state.exceptionsPage < totalPages) {
      state.exceptionsPage += 1;
      loadExceptions();
    }
  });
  el("reviewOpenDocument").addEventListener("click", () => {
    const issue = state.reviewQueueRows.find((item) => item.key === state.reviewQueueSelectedKey);
    const record = state.documents.find((item) => item.id === issue?.record_id);
    if (record) {
      openEditResultModal(record);
    }
  });
  el("reviewOpenLinkedDocument").addEventListener("click", () => {
    const issue = state.reviewQueueRows.find((item) => item.key === state.reviewQueueSelectedKey);
    const record = state.documents.find((item) => item.id === issue?.record_id);
    if (record) {
      openLinkedRecordModal(record);
    }
  });
  el("reviewAddCommentButton").addEventListener("click", async () => {
    const issue = state.reviewQueueRows.find((item) => item.key === state.reviewQueueSelectedKey);
    const record = state.documents.find((item) => item.id === issue?.record_id);
    const body = el("reviewCommentInput").value.trim();
    if (!record || !body) {
      showSweetAlert("Comment Required", "Select a review item and enter a comment first.", "error");
      return;
    }
    await fetchJson(`/api/projects/${state.selectedProjectId}/comments`, {
      method: "POST",
      body: JSON.stringify({ document_id: record.id, body }),
    });
    el("reviewCommentInput").value = "";
    await loadReviewComments(record.id);
  });
  el("reviewAssignButton").addEventListener("click", async () => {
    const issue = state.reviewQueueRows.find((item) => item.key === state.reviewQueueSelectedKey);
    const record = state.documents.find((item) => item.id === issue?.record_id);
    if (!record) return;
    const assignedUserId = Number(el("reviewAssignUser").value || 0) || null;
    const response = await fetchJson(`/api/documents/${record.id}/assignment`, {
      method: "PUT",
      body: JSON.stringify({ assigned_user_id: assignedUserId }),
    });
    replaceDocumentInState(response.document);
    renderReviewQueue();
    showSweetAlert("Assignment Updated", assignedUserId ? "Review item assigned." : "Assignment cleared.", "success");
  });
  el("vendorSearch").addEventListener("input", (event) => {
    state.vendorSearch = event.target.value;
    state.vendorsPage = 1;
    renderVendors();
  });
  el("memberSaveButton").addEventListener("click", async () => {
    if (!state.selectedProjectId) return;
    if (!canManageProjectMembers()) {
      showSweetAlert("Permission Denied", "Only project admins or owners can manage members.", "error");
      return;
    }
    const username = el("memberUsername").value.trim();
    const role = el("memberRole").value;
    if (!username) {
      showSweetAlert("Username Required", "Enter a username first.", "error");
      return;
    }
    await fetchJson(`/api/projects/${state.selectedProjectId}/members`, {
      method: "POST",
      body: JSON.stringify({ username, role }),
    });
    el("memberUsername").value = "";
    el("memberRole").value = "reviewer";
    await loadProjectMembers();
    showSweetAlert("Member Saved", "Project membership updated.", "success");
  });
  el("vendorResetFilters").addEventListener("click", () => {
    state.vendorSearch = "";
    state.vendorsPage = 1;
    el("vendorSearch").value = "";
    renderVendors();
  });
  el("vendorsPrevPage").addEventListener("click", () => {
    if (state.vendorsPage > 1) {
      state.vendorsPage -= 1;
      renderVendors();
    }
  });
  el("vendorsNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Math.ceil(vendorGroups().filter((item) => {
      const q = state.vendorSearch.trim().toLowerCase();
      return !q || [item.canonical, ...item.variants].join(" ").toLowerCase().includes(q);
    }).length / VENDORS_PAGE_SIZE));
    if (state.vendorsPage < totalPages) {
      state.vendorsPage += 1;
      renderVendors();
    }
  });
  el("vendorSaveCanonical").addEventListener("click", async () => {
    if (!state.selectedVendorKey) return;
    const canonical = el("vendorCanonicalInput").value.trim() || state.selectedVendorKey;
    await fetchJson(`/api/projects/${state.selectedProjectId}/vendor-aliases`, {
      method: "POST",
      body: JSON.stringify({ normalized_key: state.selectedVendorKey, canonical_name: canonical }),
    });
    state.vendorAliases[state.selectedVendorKey] = canonical;
    renderVendors();
  });
  el("vendorClearCanonical").addEventListener("click", async () => {
    if (!state.selectedVendorKey) return;
    delete state.vendorAliases[state.selectedVendorKey];
    const payload = await fetchJson(`/api/projects/${state.selectedProjectId}/vendor-aliases`);
    const alias = (payload.aliases || []).find((item) => item.normalized_key === state.selectedVendorKey);
    if (alias) {
      await fetchJson(`/api/projects/${state.selectedProjectId}/vendor-aliases/${alias.id}`, { method: "DELETE" });
    }
    renderVendors();
    renderDocuments(state.documents);
  });
  el("addRuleButton").addEventListener("click", async () => {
    const keyword = el("ruleKeyword").value.trim();
    if (!keyword) {
      showSweetAlert("Rule Keyword Required", "Enter a keyword before adding a rule.", "error");
      return;
    }
    const response = await fetchJson(`/api/projects/${state.selectedProjectId}/rules`, {
      method: "POST",
      body: JSON.stringify({
        keyword,
        source_type: el("ruleSourceKind").value,
        status: el("ruleStatus").value,
        category: el("ruleCategory").value.trim(),
        subcategory: el("ruleSubcategory").value.trim(),
        account_code: el("ruleAccountCode").value.trim(),
        offset_account_code: el("ruleOffsetAccountCode").value.trim(),
        payment_method: el("rulePaymentMethod").value.trim(),
        auto_post: Boolean(el("ruleAutoPost").checked),
      }),
    });
    state.projectRules.push(response.rule);
    el("ruleKeyword").value = "";
    el("ruleSourceKind").value = "";
    el("ruleStatus").value = "";
    el("ruleCategory").value = "";
    el("ruleSubcategory").value = "";
    el("ruleAccountCode").value = "";
    el("ruleOffsetAccountCode").value = "";
    el("rulePaymentMethod").value = "";
    el("ruleAutoPost").checked = true;
    renderRules();
    renderDocuments(state.documents);
  });
  el("seedAccountingRulesButton").addEventListener("click", async () => {
    const response = await fetchJson(`/api/projects/${state.selectedProjectId}/rules/seed-accounting`, {
      method: "POST",
    });
    await loadProjectRulesRemote();
    await loadDocumentsRemote({ refreshFilters: false });
    showSweetAlert("Accounting Rules Seeded", `${response.created_count || 0} starter rules created from construction heuristics and your existing parsed data.`, "success");
  });
  el("tagsSearch").addEventListener("input", (event) => {
    state.tagsSearch = event.target.value;
    renderTags();
  });
  el("tagsSourceFilter").addEventListener("change", (event) => {
    state.tagsSourceFilter = event.target.value;
    renderTags();
  });
  el("tagsResetFilters").addEventListener("click", () => {
    state.tagsSearch = "";
    state.tagsSourceFilter = "";
    el("tagsSearch").value = "";
    el("tagsSourceFilter").value = "";
    renderTags();
  });
  el("saveTagsButton").addEventListener("click", async () => {
    if (!state.selectedTagRecordId) return;
    const response = await fetchJson(`/api/documents/${state.selectedTagRecordId}/tags`, {
      method: "PUT",
      body: JSON.stringify({
        canonical_company_name: canonicalVendorName(state.documents.find((item) => item.id === state.selectedTagRecordId)?.company_name || ""),
        category: el("tagCategory").value.trim(),
        subcategory: el("tagSubcategory").value.trim(),
        account_code: el("tagAccountCode").value,
        offset_account_code: el("tagOffsetAccountCode").value,
        cost_code: el("tagCostCode").value.trim(),
        cost_center: el("tagCostCenter").value.trim(),
        project_code: el("tagProjectCode").value.trim(),
        purchase_order_id: el("tagPurchaseOrderId").value ? Number(el("tagPurchaseOrderId").value) : null,
        payment_method: el("tagPaymentMethod").value.trim(),
        vat_flag: el("tagVatFlag").checked,
      }),
    });
    replaceDocumentInState(response.document);
    syncRecordTagsFromDocuments();
    renderTags();
  });
  el("clearTagsButton").addEventListener("click", async () => {
    if (!state.selectedTagRecordId) return;
    const response = await fetchJson(`/api/documents/${state.selectedTagRecordId}/tags`, {
      method: "PUT",
      body: JSON.stringify({
        canonical_company_name: "",
        category: "",
        subcategory: "",
        account_code: "",
        offset_account_code: "",
        cost_code: "",
        cost_center: "",
        project_code: "",
        purchase_order_id: null,
        payment_method: "",
        vat_flag: false,
      }),
    });
    replaceDocumentInState(response.document);
    syncRecordTagsFromDocuments();
    renderTags();
  });
  el("downloadAllOutputsButton").addEventListener("click", () => downloadOutputs("all"));
  el("downloadSelectedOutputsButton").addEventListener("click", () => downloadOutputs("selected"));
  el("exportResultsCsvButton").addEventListener("click", () => exportResults("csv"));
  el("exportAccountingCsvButton").addEventListener("click", exportAccountingResults);
  el("exportUnresolvedCsvButton").addEventListener("click", exportUnresolvedResults);
  el("exportResultsExcelButton").addEventListener("click", () => exportResults("xlsx"));
  el("globalSearchInput").addEventListener("input", async (event) => {
    state.globalSearchQuery = event.target.value;
    state.globalSearchPage = 1;
    await loadGlobalSearch();
  });
  el("globalSearchKindFilter").addEventListener("change", async (event) => {
    state.globalSearchKindFilter = event.target.value;
    state.globalSearchPage = 1;
    await loadGlobalSearch();
  });
  el("globalSearchStatusFilter").addEventListener("change", async (event) => {
    state.globalSearchStatusFilter = event.target.value;
    state.globalSearchPage = 1;
    await loadGlobalSearch();
  });
  el("globalSearchConfidenceFilter").addEventListener("change", async (event) => {
    state.globalSearchConfidenceFilter = event.target.value;
    state.globalSearchPage = 1;
    await loadGlobalSearch();
  });
  el("globalSearchResetFilters").addEventListener("click", async () => {
    state.globalSearchQuery = "";
    state.globalSearchKindFilter = "";
    state.globalSearchStatusFilter = "";
    state.globalSearchConfidenceFilter = "";
    state.globalSearchPage = 1;
    el("globalSearchInput").value = "";
    el("globalSearchKindFilter").value = "";
    el("globalSearchStatusFilter").value = "";
    el("globalSearchConfidenceFilter").value = "";
    await loadGlobalSearch();
  });
  el("globalSearchPrevPage").addEventListener("click", async () => {
    if (state.globalSearchPage > 1) {
      state.globalSearchPage -= 1;
      await loadGlobalSearch();
    }
  });
  el("globalSearchNextPage").addEventListener("click", async () => {
    const totalPages = state.globalSearchPagination.total_pages || 1;
    if (state.globalSearchPage < totalPages) {
      state.globalSearchPage += 1;
      await loadGlobalSearch();
    }
  });
  el("globalSearchOpenDocument").addEventListener("click", () => {
    const record = state.documents.find((item) => item.id === state.globalSearchSelectedId) || null;
    if (record) {
      openEditResultModal(record);
    }
  });
  el("globalSearchOpenLinked").addEventListener("click", () => {
    const record = state.documents.find((item) => item.id === state.globalSearchSelectedId) || null;
    if (record) {
      openLinkedRecordModal(record);
    }
  });
  el("saveCurrentSearchButton").addEventListener("click", async () => {
    const name = el("savedSearchName").value.trim();
    if (!name) {
      showSweetAlert("Search Name Required", "Enter a name before saving the current search.", "error");
      return;
    }
    await fetchJson(`/api/projects/${state.selectedProjectId}/saved-searches`, {
      method: "POST",
      body: JSON.stringify({
        name,
        scope: "global_search",
        query: {
          q: state.globalSearchQuery,
          kind: state.globalSearchKindFilter,
          status: state.globalSearchStatusFilter,
          confidence: state.globalSearchConfidenceFilter,
        },
      }),
    });
    el("savedSearchName").value = "";
    await loadSavedSearches();
  });
  el("savedSearchSelect").addEventListener("change", async (event) => {
    const saved = state.savedSearches.find((item) => String(item.id) === event.target.value);
    if (!saved) return;
    state.globalSearchQuery = saved.query?.q || "";
    state.globalSearchKindFilter = saved.query?.kind || "";
    state.globalSearchStatusFilter = saved.query?.status || "";
    state.globalSearchConfidenceFilter = saved.query?.confidence || "";
    state.globalSearchPage = 1;
    el("globalSearchInput").value = state.globalSearchQuery;
    el("globalSearchKindFilter").value = state.globalSearchKindFilter;
    el("globalSearchStatusFilter").value = state.globalSearchStatusFilter;
    el("globalSearchConfidenceFilter").value = state.globalSearchConfidenceFilter;
    await loadGlobalSearch();
  });
  el("deleteSavedSearchButton").addEventListener("click", async () => {
    const selectedId = el("savedSearchSelect").value;
    if (!selectedId) {
      showSweetAlert("Saved Search Required", "Select a saved search first.", "error");
      return;
    }
    await fetchJson(`/api/projects/${state.selectedProjectId}/saved-searches/${selectedId}`, { method: "DELETE" });
    el("savedSearchSelect").value = "";
    await loadSavedSearches();
  });
  el("evidenceSearch").addEventListener("input", (event) => {
    state.evidenceSearch = event.target.value;
    state.evidencePage = 1;
    renderEvidence();
  });
  el("evidenceAttachmentFilter").addEventListener("change", (event) => {
    state.evidenceAttachmentFilter = event.target.value;
    state.evidencePage = 1;
    renderEvidence();
  });
  el("evidenceResetFilters").addEventListener("click", () => {
    state.evidenceSearch = "";
    state.evidenceAttachmentFilter = "";
    state.evidencePage = 1;
    el("evidenceSearch").value = "";
    el("evidenceAttachmentFilter").value = "";
    renderEvidence();
  });
  el("evidencePrevPage").addEventListener("click", () => {
    if (state.evidencePage > 1) {
      state.evidencePage -= 1;
      renderEvidence();
    }
  });
  el("evidenceNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Math.ceil(evidenceFilteredRows().length / DOCUMENTS_PAGE_SIZE));
    if (state.evidencePage < totalPages) {
      state.evidencePage += 1;
      renderEvidence();
    }
  });
  el("pickEvidenceAttachmentButton").addEventListener("click", async () => {
    state.pendingEvidenceAttachmentPath = await pickFile("attachment");
    renderEvidence();
  });
  el("addEvidenceAttachmentButton").addEventListener("click", async () => {
    if (!state.evidenceSelectedId || !state.pendingEvidenceAttachmentPath) {
      showSweetAlert("Attachment Required", "Select a document and pick a file first.", "error");
      return;
    }
    await fetchJson(`/api/documents/${state.evidenceSelectedId}/attachments`, {
      method: "POST",
      body: JSON.stringify({
        attachment_type: el("evidenceAttachmentType").value,
        label: el("evidenceAttachmentLabel").value.trim(),
        file_path: state.pendingEvidenceAttachmentPath,
        note: el("evidenceAttachmentNote").value.trim(),
      }),
    });
    state.pendingEvidenceAttachmentPath = "";
    state.evidenceSelectedAttachmentId = 0;
    el("evidenceAttachmentLabel").value = "";
    el("evidenceAttachmentType").value = "supporting_document";
    el("evidenceAttachmentNote").value = "";
    await loadEvidenceAttachmentCounts();
    await loadEvidenceAttachments(state.evidenceSelectedId);
    renderEvidence();
  });
  el("evidenceOpenLinkedButton").addEventListener("click", () => {
    const record = state.documents.find((item) => item.id === state.evidenceSelectedId) || null;
    if (record) {
      openLinkedRecordModal(record);
    }
  });
  el("exportEvidencePackAllButton").addEventListener("click", () => exportEvidencePack("all"));
  el("exportEvidencePackSelectedButton").addEventListener("click", () => exportEvidencePack("selected"));
  el("exportEvidencePackUnresolvedButton").addEventListener("click", () => exportEvidencePack("unresolved"));
  el("exportClosePackageButton").addEventListener("click", exportClosePackage);
  el("deleteProjectButton").addEventListener("click", deleteCurrentProject);
  el("closeEditResultModal").addEventListener("click", closeEditResultModal);
  el("closeLinkedRecordModal").addEventListener("click", closeLinkedRecordModal);
  el("saveEditedResultButton").addEventListener("click", saveEditedResult);
  el("previewOutputButton").addEventListener("click", () => setEditPreviewMode("output"));
  el("previewEnhancedButton").addEventListener("click", () => setEditPreviewMode("enhanced"));
  el("namingPattern").addEventListener("input", updateNamingPreview);
  el("projectName").addEventListener("input", updateNamingPreview);

  await restoreSession();
  await loadAccountingExportOptions();
  await loadModels();

  if (payload.runtime.messages?.length) {
    showSweetAlert("Runtime Check", payload.runtime.messages.join(" "), "info");
  }
}

init().catch((error) => {
  showAuthView();
  showSweetAlert("Load Error", error.message, "error");
});
