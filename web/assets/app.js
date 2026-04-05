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
  selectedHistoryIds: new Set(),
  editingDocumentId: null,
  historySearch: "",
  historyTypeFilter: "",
  historyCompanyFilter: "",
  historyConfidenceFilter: "",
  historyPage: 1,
  models: [],
  modelRefreshTimer: null,
};

const HISTORY_PAGE_SIZE = 10;

const el = (id) => document.getElementById(id);

function authHeaders() {
  return state.authToken ? { "X-Auth-Token": state.authToken } : {};
}

function setStatus(value) {
  el("jobStatus").textContent = value;
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
  setEditPreviewMode("source", document);
  el("editResultModal").classList.remove("hidden");
}

function closeEditResultModal() {
  state.editingDocumentId = null;
  el("editResultModal").classList.add("hidden");
}

function setEditPreviewMode(mode, docRecord = null) {
  const currentDocument =
    docRecord || state.documents.find((item) => item.id === state.editingDocumentId) || null;
  const modeToPath = {
    source: currentDocument?.source_path || "",
    output: currentDocument?.output_path || "",
    enhanced: currentDocument?.enhanced_output_path || "",
  };
  const path = modeToPath[mode] || modeToPath.output || modeToPath.source || modeToPath.enhanced || "";
  const href = path
    ? `/api/file?path=${encodeURIComponent(path)}&token=${encodeURIComponent(state.authToken)}`
    : "";

  window.document.querySelectorAll(".preview-mode-button").forEach((button) => {
    button.classList.toggle("active", button.id === `preview${mode.charAt(0).toUpperCase()}${mode.slice(1)}Button`);
  });
  el("previewOpenLink").href = href || "#";
  el("previewOpenLink").style.pointerEvents = href ? "auto" : "none";
  el("previewOpenLink").style.opacity = href ? "1" : "0.45";
  el("previewFileLabel").textContent = path || "No file available for this preview.";
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
  return {
    source_dir: el("sourceDir").value.trim(),
    output_dir: el("outputDir").value.trim(),
    debug_image_dir: el("debugImageDir").value.trim(),
    archive_source_dir: el("archiveSourceDir").value.trim(),
    project_name: el("projectName").value.trim(),
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
    excel_name: "document_summary.xlsx",
  };
}

function getSelectedProject() {
  return state.projects.find((project) => project.id === state.selectedProjectId) || null;
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

function switchView(name) {
  state.currentView = name;
  const mapping = {
    home: "homeView",
    system: "systemView",
    projectEditor: "projectEditorView",
    projectDetail: "projectDetailView",
  };
  Object.values(mapping).forEach((id) => el(id).classList.add("hidden"));
  el(mapping[name]).classList.remove("hidden");

  document.querySelectorAll(".nav-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.viewTarget === name);
  });
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
  el("dashboardProjectCount").textContent = String(state.projects.length);
  const selected = getSelectedProject();
  el("dashboardProjectName").textContent = selected ? selected.name : "None selected";
  el("topbarUsername").textContent = state.currentUser?.username || "Unknown";
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
  if (!project) {
    el("projectDetailTitle").textContent = "No project selected";
    el("projectDetailDescription").textContent = "Open a project from the dashboard to manage OCR settings and stored documents.";
    el("overviewProjectName").textContent = "-";
    el("overviewOcrBackend").textContent = "-";
    el("overviewDocumentCount").textContent = "0";
    el("overviewNamingPattern").textContent = emptyProjectSettings().naming_pattern;
    el("projectSettingsSummary").innerHTML = "";
    return;
  }

  const settings = { ...emptyProjectSettings(), ...(project.settings || {}) };
  el("projectDetailTitle").textContent = project.name;
  el("projectDetailDescription").textContent = project.description || "Saved OCR workflow";
  el("overviewProjectName").textContent = settings.project_name || project.name;
  el("overviewOcrBackend").textContent = settings.ocr_backend;
  el("overviewDocumentCount").textContent = String(state.documents.length);
  el("overviewNamingPattern").textContent = settings.naming_pattern;

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
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Request failed");
  }
  return payload;
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
      <td class="px-4 py-4">${fileCell(record.output_file, record.output_file)}</td>
      <td class="px-4 py-4">${record.doc_type}</td>
      <td class="px-4 py-4">${record.date}</td>
      <td class="px-4 py-4">${record.number}</td>
      <td class="px-4 py-4">${record.company_name}</td>
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

function populateHistoryFilters(documents) {
  const typeFilter = el("historyTypeFilter");
  const companyFilter = el("historyCompanyFilter");
  const currentType = state.historyTypeFilter;
  const currentCompany = state.historyCompanyFilter;
  const types = [...new Set(documents.map((item) => item.doc_type).filter(Boolean))].sort();
  const companies = [...new Set(documents.map((item) => item.company_name).filter(Boolean))].sort();

  typeFilter.innerHTML = '<option value="">All Types</option>';
  companyFilter.innerHTML = '<option value="">All Companies</option>';
  types.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    typeFilter.appendChild(option);
  });
  companies.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    companyFilter.appendChild(option);
  });
  typeFilter.value = currentType;
  companyFilter.value = currentCompany;
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
      ]
        .join(" ")
        .toLowerCase()
        .includes(query);
    const matchesType = !state.historyTypeFilter || item.doc_type === state.historyTypeFilter;
    const matchesCompany = !state.historyCompanyFilter || item.company_name === state.historyCompanyFilter;
    const matchesConfidence = !state.historyConfidenceFilter || item.confidence_label === state.historyConfidenceFilter;
    return matchesQuery && matchesType && matchesCompany && matchesConfidence;
  });
}

function updateHistoryPagination(totalItems) {
  const totalPages = Math.max(1, Math.ceil(totalItems / HISTORY_PAGE_SIZE));
  if (state.historyPage > totalPages) {
    state.historyPage = totalPages;
  }
  el("historyPageLabel").textContent = `Page ${state.historyPage} of ${totalPages}`;
  el("historySummary").textContent = `${totalItems} result${totalItems === 1 ? "" : "s"}`;
  el("historyPrevPage").disabled = state.historyPage <= 1;
  el("historyNextPage").disabled = state.historyPage >= totalPages;
  el("historyPrevPage").style.opacity = state.historyPage <= 1 ? "0.45" : "1";
  el("historyNextPage").style.opacity = state.historyPage >= totalPages ? "0.45" : "1";
}

function renderHistory(documents) {
  const tbody = el("historyTable").querySelector("tbody");
  const selectAll = el("historySelectAll");
  tbody.innerHTML = "";
  populateHistoryFilters(documents);
  const filteredDocuments = getFilteredHistory(documents);
  updateHistoryPagination(filteredDocuments.length);
  const start = (state.historyPage - 1) * HISTORY_PAGE_SIZE;
  const pageDocuments = filteredDocuments.slice(start, start + HISTORY_PAGE_SIZE);
  state.selectedHistoryIds = new Set(
    Array.from(state.selectedHistoryIds).filter((id) => filteredDocuments.some((item) => item.id === id)),
  );
  selectAll.checked = false;
  if (!state.selectedProjectId || filteredDocuments.length === 0) {
    el("historySummary").textContent = documents.length === 0 ? "0 results" : "No results match the current filters";
    return;
  }

  pageDocuments.forEach((item) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    tr.innerHTML = `
      <td class="px-4 py-4"><input data-history-id="${item.id}" type="checkbox" class="history-checkbox h-4 w-4" ${state.selectedHistoryIds.has(item.id) ? "checked" : ""} /></td>
      <td class="px-4 py-4">${formatDateTime(item.created_at)}</td>
      <td class="px-4 py-4">${fileLink(item.source_path, item.source_file || "Open")}</td>
      <td class="px-4 py-4">${fileLink(item.output_path, item.output_file || "Open")}</td>
      <td class="px-4 py-4">${item.doc_type}</td>
      <td class="px-4 py-4">${item.date}</td>
      <td class="px-4 py-4">${item.number}</td>
      <td class="px-4 py-4">${item.company_name}</td>
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
      const document = filteredDocuments.find((item) => item.id === Number(button.dataset.editHistoryId));
      if (document) {
        openEditResultModal(document);
      }
    });
  });

  selectAll.checked = pageDocuments.length > 0 && pageDocuments.every((item) => state.selectedHistoryIds.has(item.id));
}

function renderDocuments(documents) {
  state.documents = documents;
  const tbody = el("documentsTable").querySelector("tbody");
  tbody.innerHTML = "";
  if (!state.selectedProjectId || documents.length === 0) {
    renderHistory([]);
    renderProjectDetail();
    return;
  }
  documents.forEach((item) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-[rgba(77,49,29,0.08)]";
    tr.innerHTML = `
      <td class="px-4 py-4">${fileLink(item.source_path, item.source_file || "Open")}</td>
      <td class="px-4 py-4">${fileLink(item.output_path, item.output_file || "Open")}</td>
      <td class="px-4 py-4">${fileLink(item.enhanced_output_path, item.enhanced_output_path ? "Enhanced PDF" : "")}</td>
      <td class="px-4 py-4">${fileLink(item.original_debug_image, item.original_debug_image ? "Original Image" : "")}</td>
      <td class="px-4 py-4">${fileLink(item.enhanced_debug_image, item.enhanced_debug_image ? "Enhanced Image" : "")}</td>
      <td class="px-4 py-4">${item.doc_type}</td>
      <td class="px-4 py-4">${item.date}</td>
      <td class="px-4 py-4">${item.number}</td>
      <td class="px-4 py-4">${confidenceBadge(item.confidence_label, item.confidence_score)}</td>
    `;
    tbody.appendChild(tr);
  });
  renderHistory(documents);
  renderProjectDetail();
}

function projectPayload() {
  return {
    name: el("projectRecordName").value.trim() || "ULTRA FORCE Project",
    description: el("projectDescription").value.trim(),
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
  state.selectedHistoryIds = new Set();
  state.historySearch = "";
  state.historyTypeFilter = "";
  state.historyCompanyFilter = "";
  state.historyConfidenceFilter = "";
  state.historyPage = 1;
  el("projectFormTitle").textContent = "New Project";
  el("projectRecordName").value = "ULTRA FORCE Project";
  el("projectDescription").value = "";
  applySettings(emptyProjectSettings());
  resetJobPanels();
  renderDocuments([]);
  renderHistory([]);
  renderSidebarProjects();
  renderProjectsTable();
  renderDashboard();
  renderProjectDetail();
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
    showSweetAlert("Missing Required Fields", "Source folder, output folder, and project name are required.", "error");
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
  updateRunAvailability();
}

async function loadDocuments(projectId) {
  if (!projectId) {
    renderDocuments([]);
    return;
  }
  const payload = await fetchJson(`/api/projects/${projectId}/documents`);
  renderDocuments(payload.documents);
}

function applyProject(project) {
  state.selectedProjectId = project.id;
  el("projectFormTitle").textContent = `Edit Project: ${project.name}`;
  el("projectRecordName").value = project.name;
  el("projectDescription").value = project.description || "";
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
    showLoading("Updating Stored Result", "Saving corrections and renaming generated files.");
    await fetchJson(`/api/documents/${state.editingDocumentId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
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
    showSweetAlert(mode === "login" ? "Login Successful" : "Account Created", `Welcome ${payload.user.username}.`, "success");
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

  populateSelect(el("ocrBackend"), payload.options.ocr_backends);
  populateSelect(el("handwritingBackend"), payload.options.handwriting_backends);
  populateSelect(el("trocrModel"), payload.options.trocr_models);
  populateSelect(el("ocrProfile"), payload.options.ocr_profiles);
  populateSelect(el("exportImageMode"), payload.options.export_image_modes);

  applySettings(emptyProjectSettings());
  renderRuntime(payload.runtime);
  renderModels();
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
      const filteredDocuments = getFilteredHistory(state.documents);
      const start = (state.historyPage - 1) * HISTORY_PAGE_SIZE;
      const pageDocuments = filteredDocuments.slice(start, start + HISTORY_PAGE_SIZE);
      pageDocuments.forEach((item) => state.selectedHistoryIds.add(item.id));
    } else {
      const filteredDocuments = getFilteredHistory(state.documents);
      const start = (state.historyPage - 1) * HISTORY_PAGE_SIZE;
      const pageDocuments = filteredDocuments.slice(start, start + HISTORY_PAGE_SIZE);
      pageDocuments.forEach((item) => state.selectedHistoryIds.delete(item.id));
    }
    renderHistory(state.documents);
  });
  el("historySearch").addEventListener("input", (event) => {
    state.historySearch = event.target.value;
    state.historyPage = 1;
    renderHistory(state.documents);
  });
  el("historyTypeFilter").addEventListener("change", (event) => {
    state.historyTypeFilter = event.target.value;
    state.historyPage = 1;
    renderHistory(state.documents);
  });
  el("historyCompanyFilter").addEventListener("change", (event) => {
    state.historyCompanyFilter = event.target.value;
    state.historyPage = 1;
    renderHistory(state.documents);
  });
  el("historyConfidenceFilter").addEventListener("change", (event) => {
    state.historyConfidenceFilter = event.target.value;
    state.historyPage = 1;
    renderHistory(state.documents);
  });
  el("historyResetFilters").addEventListener("click", () => {
    state.historySearch = "";
    state.historyTypeFilter = "";
    state.historyCompanyFilter = "";
    state.historyConfidenceFilter = "";
    state.historyPage = 1;
    el("historySearch").value = "";
    el("historyTypeFilter").value = "";
    el("historyCompanyFilter").value = "";
    el("historyConfidenceFilter").value = "";
    renderHistory(state.documents);
  });
  el("historyPrevPage").addEventListener("click", () => {
    if (state.historyPage > 1) {
      state.historyPage -= 1;
      renderHistory(state.documents);
    }
  });
  el("historyNextPage").addEventListener("click", () => {
    const totalPages = Math.max(1, Math.ceil(getFilteredHistory(state.documents).length / HISTORY_PAGE_SIZE));
    if (state.historyPage < totalPages) {
      state.historyPage += 1;
      renderHistory(state.documents);
    }
  });
  el("downloadAllOutputsButton").addEventListener("click", () => downloadOutputs("all"));
  el("downloadSelectedOutputsButton").addEventListener("click", () => downloadOutputs("selected"));
  el("exportResultsCsvButton").addEventListener("click", () => exportResults("csv"));
  el("exportResultsExcelButton").addEventListener("click", () => exportResults("xlsx"));
  el("deleteProjectButton").addEventListener("click", deleteCurrentProject);
  el("closeEditResultModal").addEventListener("click", closeEditResultModal);
  el("saveEditedResultButton").addEventListener("click", saveEditedResult);
  el("previewSourceButton").addEventListener("click", () => setEditPreviewMode("source"));
  el("previewOutputButton").addEventListener("click", () => setEditPreviewMode("output"));
  el("previewEnhancedButton").addEventListener("click", () => setEditPreviewMode("enhanced"));
  el("namingPattern").addEventListener("input", updateNamingPreview);
  el("projectName").addEventListener("input", updateNamingPreview);

  await restoreSession();
  await loadModels();

  if (payload.runtime.messages?.length) {
    showSweetAlert("Runtime Check", payload.runtime.messages.join(" "), "info");
  }
}

init().catch((error) => {
  showAuthView();
  showSweetAlert("Load Error", error.message, "error");
});
