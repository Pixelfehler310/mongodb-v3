const state = {
    facets: null,
    products: [],
    lastTotal: 0,
    lastLimit: 0,
    selectedProduct: null,
    currentQueryText: "",
    currentCodeText: "",
    activeTab: "document",
    aggregationKind: "avgPriceByType",
};

const elements = {
    healthStatus: document.querySelector("#healthStatus"),
    filterForm: document.querySelector("#filterForm"),
    productList: document.querySelector("#productList"),
    resultCount: document.querySelector("#resultCount"),
    detailTitle: document.querySelector("#detailTitle"),
    detailContent: document.querySelector("#detailContent"),
    schemaHint: document.querySelector("#schemaHint"),
    statusMessage: document.querySelector("#statusMessage"),
    resetFiltersButton: document.querySelector("#resetFiltersButton"),
    insertSampleButton: document.querySelector("#insertSampleButton"),
    sampleType: document.querySelector("#sampleType"),
    aggregationSelect: document.querySelector("#aggregationSelect"),
    aggregationHead: document.querySelector("#aggregationHead"),
    aggregationBody: document.querySelector("#aggregationBody"),
    aggregationQuery: document.querySelector("#aggregationQuery"),
};

async function fetchJson(url, options = {}) {
    const response = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    const payload = await response.json();
    if (!response.ok) {
        throw new Error(payload.detail || payload.error || `Request failed: ${response.status}`);
    }
    return payload;
}

function setStatus(message = "") {
    elements.statusMessage.textContent = message;
}

function fillSelect(selector, values, mapValue = (value) => value, mapLabel = (value) => value) {
    const select = document.querySelector(selector);
    const first = select.querySelector("option");
    select.replaceChildren(first);
    values.forEach((value) => {
        const option = document.createElement("option");
        option.value = mapValue(value);
        option.textContent = mapLabel(value);
        select.append(option);
    });
}

function populateFacets(facets) {
    fillSelect("#productTypeFilter", facets.productTypes);
    fillSelect("#manufacturerFilter", facets.manufacturers);
    fillSelect("#categoryFilter", facets.categories, (item) => item.slug, (item) => item.name);
    fillSelect("#statusFilter", facets.statuses);
    fillSelect("#ramFilter", facets.ramOptions, (value) => String(value), (value) => `${value} GB`);
    fillSelect("#regionFilter", facets.shippingRegions);
    fillSelect("#tagFilter", facets.tags);
    fillSelect("#schemaFilter", facets.schemaEvolution, (item) => item.value, (item) => item.label);

    elements.aggregationSelect.replaceChildren();
    facets.aggregations.forEach((aggregation) => {
        const option = document.createElement("option");
        option.value = aggregation.kind;
        option.textContent = aggregation.label;
        elements.aggregationSelect.append(option);
    });
}

function collectFilters() {
    const formData = new FormData(elements.filterForm);
    const params = new URLSearchParams();
    for (const [key, value] of formData.entries()) {
        if (String(value).trim()) {
            params.set(key, String(value).trim());
        }
    }
    return params;
}

async function loadHealth() {
    try {
        const health = await fetchJson("/api/health");
        elements.healthStatus.textContent = `${health.productCount} products`;
        elements.healthStatus.className = "status-pill ok";
    } catch (error) {
        elements.healthStatus.textContent = "MongoDB offline";
        elements.healthStatus.className = "status-pill error";
        setStatus(error.message);
    }
}

async function loadFacets() {
    state.facets = await fetchJson("/api/facets");
    populateFacets(state.facets);
}

async function loadProducts({ clearSelection = true } = {}) {
    setStatus("Loading products");
    const params = collectFilters();
    const url = params.toString() ? `/api/products?${params}` : "/api/products";
    const data = await fetchJson(url);
    state.products = data.items;
    state.lastTotal = data.total;
    state.lastLimit = data.limit;
    state.currentQueryText = data.queryText;
    state.currentCodeText = data.codeText;
    if (clearSelection) {
        state.selectedProduct = null;
    }
    renderProducts(data.total, data.limit);
    renderDetail();
    setStatus(data.total ? "" : "No products match the active filters");
}

function renderProducts(total, limit) {
    elements.resultCount.textContent = `${total} result${total === 1 ? "" : "s"} / limit ${limit}`;
    elements.productList.replaceChildren();

    if (!state.products.length) {
        const empty = document.createElement("div");
        empty.className = "muted";
        empty.textContent = "No matching products.";
        elements.productList.append(empty);
        return;
    }

    state.products.forEach((product) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = `product-item${state.selectedProduct?._id === product._id ? " active" : ""}`;
        button.addEventListener("click", () => selectProduct(product._id));

        const text = document.createElement("div");
        const name = document.createElement("div");
        name.className = "product-name";
        name.textContent = product.name;
        const meta = document.createElement("div");
        meta.className = "product-meta";
        meta.textContent = `${formatCurrency(product.basePrice, product.currency)} · ${product.manufacturer?.name || "unknown"}`;
        const category = document.createElement("div");
        category.className = "product-category";
        category.textContent = `${product.categories?.[0]?.name || "Uncategorized"} · updated ${shortDate(product.updatedAt)}`;
        text.append(name, meta, category);

        const badge = document.createElement("span");
        badge.className = "type-badge";
        badge.textContent = product.productType;
        button.append(text, badge);
        elements.productList.append(button);
    });
}

async function selectProduct(productId) {
    setStatus("Loading document");
    const data = await fetchJson(`/api/products/${encodeURIComponent(productId)}`);
    state.selectedProduct = data.item;
    state.currentQueryText = data.queryText;
    state.currentCodeText = data.codeText;
    renderProducts(state.lastTotal, state.lastLimit);
    renderDetail();
    setStatus("");
}

function renderDetail() {
    const selected = state.selectedProduct;
    document.querySelectorAll(".tab-button").forEach((button) => {
        button.classList.toggle("active", button.dataset.tab === state.activeTab);
    });

    if (!selected) {
        elements.detailTitle.textContent = "Document";
        elements.schemaHint.className = "schema-hint";
        elements.schemaHint.textContent = "List query is shown until a product is selected.";
        elements.detailContent.textContent = state.activeTab === "code" ? state.currentCodeText : state.currentQueryText || "Select a product to inspect its document.";
        if (state.activeTab === "document") {
            elements.detailContent.textContent = "Select a product to inspect its document.";
        }
        return;
    }

    elements.detailTitle.textContent = selected.name;
    const hasTaxCode = Object.hasOwn(selected, "regionalTaxCode");
    elements.schemaHint.className = `schema-hint ${hasTaxCode ? "newer" : "older"}`;
    elements.schemaHint.textContent = hasTaxCode
        ? `Schema version ${selected.schemaVersion}: regionalTaxCode = ${selected.regionalTaxCode}`
        : `Schema version ${selected.schemaVersion}: no regionalTaxCode field`;

    if (state.activeTab === "query") {
        elements.detailContent.textContent = state.currentQueryText;
    } else if (state.activeTab === "code") {
        elements.detailContent.textContent = state.currentCodeText;
    } else {
        elements.detailContent.textContent = JSON.stringify(selected, null, 2);
    }
}

async function loadAggregation() {
    const data = await fetchJson(`/api/aggregation?kind=${encodeURIComponent(state.aggregationKind)}`);
    renderAggregation(data);
}

function renderAggregation(data) {
    elements.aggregationQuery.textContent = data.queryText;
    elements.aggregationHead.replaceChildren();
    elements.aggregationBody.replaceChildren();

    const keys = Array.from(new Set(data.results.flatMap((row) => Object.keys(row))));
    const headerRow = document.createElement("tr");
    keys.forEach((key) => {
        const th = document.createElement("th");
        th.textContent = key === "_id" ? "group" : key;
        headerRow.append(th);
    });
    elements.aggregationHead.append(headerRow);

    data.results.forEach((row) => {
        const tr = document.createElement("tr");
        keys.forEach((key) => {
            const td = document.createElement("td");
            td.textContent = formatCell(row[key]);
            tr.append(td);
        });
        elements.aggregationBody.append(tr);
    });
}

function formatCell(value) {
    if (typeof value === "number") {
        return Number.isInteger(value) ? String(value) : value.toFixed(2);
    }
    return value ?? "";
}

function formatCurrency(value, currency) {
    return new Intl.NumberFormat("de-DE", { style: "currency", currency: currency || "EUR" }).format(value || 0);
}

function shortDate(value) {
    if (!value) {
        return "unknown";
    }
    return new Intl.DateTimeFormat("de-DE", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" }).format(new Date(value));
}

async function insertSample() {
    setStatus("Inserting sample product");
    const payload = { productType: elements.sampleType.value };
    const data = await fetchJson("/api/products/sample", {
        method: "POST",
        body: JSON.stringify(payload),
    });
    await loadFacets();
    await loadProducts({ clearSelection: false });
    await selectProduct(data.item._id);
    await loadAggregation();
    await loadHealth();
    setStatus(data.message);
}

function bindEvents() {
    elements.filterForm.addEventListener("input", () => loadProducts().catch(handleError));
    elements.filterForm.addEventListener("change", () => loadProducts().catch(handleError));
    elements.filterForm.addEventListener("submit", (event) => {
        event.preventDefault();
        loadProducts().catch(handleError);
    });
    elements.resetFiltersButton.addEventListener("click", () => {
        elements.filterForm.reset();
        loadProducts().catch(handleError);
    });
    elements.insertSampleButton.addEventListener("click", () => insertSample().catch(handleError));
    elements.aggregationSelect.addEventListener("change", () => {
        state.aggregationKind = elements.aggregationSelect.value;
        loadAggregation().catch(handleError);
    });
    document.querySelectorAll(".tab-button").forEach((button) => {
        button.addEventListener("click", () => {
            state.activeTab = button.dataset.tab;
            renderDetail();
        });
    });
}

function handleError(error) {
    setStatus(error.message);
}

async function init() {
    bindEvents();
    await loadHealth();
    await loadFacets();
    await loadProducts();
    await loadAggregation();
}

init().catch(handleError);