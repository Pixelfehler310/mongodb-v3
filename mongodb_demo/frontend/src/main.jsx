import React, { useCallback, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const backends = [
  { id: "mongo", label: "MongoDB", apiBase: "/api/mongo", model: "embedded document", accent: "document-local" },
  { id: "postgres", label: "PostgreSQL", apiBase: "/api/postgres", model: "normalized tables", accent: "relational" },
];

const emptyFilters = {
  productType: "",
  category: "",
  schemaEvolution: "",
  search: "",
};

const emptyDialogState = {
  mode: null,
  product: null,
  form: null,
  originalForm: null,
  editMode: false,
  error: "",
};

const attributeTypeOptions = ["string", "number", "boolean"];

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = response.status === 204 ? {} : await response.json();
  if (!response.ok) {
    const detail = Array.isArray(payload.details) ? payload.details.join(" ") : payload.detail || payload.error;
    throw new Error(detail || `Request failed: ${response.status}`);
  }
  return payload;
}

function queryParams(filters, limit = 18) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (String(value).trim()) {
      params.set(key, String(value).trim());
    }
  });
  params.set("limit", String(limit));
  return params;
}

function formatCurrency(value, currency) {
  return new Intl.NumberFormat("de-DE", { style: "currency", currency: currency || "EUR" }).format(value || 0);
}

function formatCell(value) {
  if (typeof value === "number") {
    return Number.isInteger(value) ? String(value) : value.toFixed(2);
  }
  return value ?? "";
}

function cloneProduct(product) {
  return JSON.parse(JSON.stringify(product || {}));
}

function sanitizeProductPayload(product) {
  const payload = cloneProduct(product);
  ["regionalTaxCode", "source"].forEach((fieldName) => {
    if (String(payload[fieldName] ?? "").trim() === "") {
      delete payload[fieldName];
    }
  });
  const attributes = {};
  Object.entries(payload.attributes || {}).forEach(([key, value]) => {
    const attributeKey = String(key).trim();
    if (attributeKey) {
      attributes[attributeKey] = value;
    }
  });
  payload.attributes = attributes;
  return payload;
}

function isSameProduct(left, right) {
  return JSON.stringify(left || {}) === JSON.stringify(right || {});
}

function totalInventory(product) {
  return (product?.variants || []).reduce((sum, variant) => sum + (Number(variant.inventoryCount) || 0), 0);
}

function averageRating(product) {
  const reviews = product?.latestReviews || [];
  if (!reviews.length) {
    return null;
  }
  const average = reviews.reduce((sum, review) => sum + (Number(review.rating) || 0), 0) / reviews.length;
  return average.toFixed(1);
}

function valueType(value) {
  if (typeof value === "number") {
    return "number";
  }
  if (typeof value === "boolean") {
    return "boolean";
  }
  return "string";
}

function coerceAttributeValue(value, type) {
  if (type === "number") {
    if (value === "") {
      return "";
    }
    const numberValue = Number(value);
    return Number.isFinite(numberValue) ? numberValue : 0;
  }
  if (type === "boolean") {
    return value === true || value === "true";
  }
  return String(value ?? "");
}

function nextReviewId(product) {
  const base = (product?._id || product?.productId || "product").replace(/[^a-z0-9]+/gi, "_").toLowerCase();
  return `rev_${base}_${Date.now().toString().slice(-6)}`;
}

function currentRoute() {
  return window.location.pathname === "/showcase" ? "/showcase" : "/shop";
}

function useRoute() {
  const [route, setRoute] = useState(currentRoute);
  useEffect(() => {
    const handlePopState = () => setRoute(currentRoute());
    window.addEventListener("popstate", handlePopState);
    if (window.location.pathname === "/") {
      window.history.replaceState({}, "", "/shop");
      setRoute("/shop");
    }
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);
  const navigate = useCallback((nextRoute) => {
    window.history.pushState({}, "", nextRoute);
    setRoute(nextRoute);
  }, []);
  return { route, navigate };
}

function App() {
  const { route, navigate } = useRoute();
  const [backendId, setBackendId] = useState("mongo");
  const backend = useMemo(() => backends.find((item) => item.id === backendId) || backends[0], [backendId]);

  return (
    <>
      <header className="topbar app-header">
        <div>
          <p className="eyebrow">Database Demo</p>
          <h1>{route === "/showcase" ? "Database Showcase" : "Product Catalog Admin"}</h1>
        </div>
        <div className="topbar-actions">
          <nav className="segmented app-nav" aria-label="Application views">
            <button type="button" className={route === "/shop" ? "active" : ""} onClick={() => navigate("/shop")}>
              Shop
            </button>
            <button type="button" className={route === "/showcase" ? "active" : ""} onClick={() => navigate("/showcase")}>
              Showcase
            </button>
          </nav>
          <BackendSelector backendId={backendId} onChange={setBackendId} />
        </div>
      </header>
      {route === "/showcase" ? <ShowcasePage backend={backend} /> : <ShopPage backend={backend} />}
    </>
  );
}

function BackendSelector({ backendId, onChange }) {
  return (
    <div className="segmented" aria-label="Data backend">
      {backends.map((backend) => (
        <button key={backend.id} type="button" className={backendId === backend.id ? "active" : ""} onClick={() => onChange(backend.id)}>
          {backend.label}
        </button>
      ))}
    </div>
  );
}

function ShopPage({ backend }) {
  const [health, setHealth] = useState(null);
  const [facets, setFacets] = useState(null);
  const [filters, setFilters] = useState(emptyFilters);
  const [productsPayload, setProductsPayload] = useState(null);
  const [dialogState, setDialogState] = useState(emptyDialogState);
  const [status, setStatus] = useState("Loading catalog.");

  const loadHealth = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/health`);
    setHealth(payload);
  }, [backend.apiBase]);

  const loadFacets = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/facets`);
    setFacets(payload);
  }, [backend.apiBase]);

  const loadProducts = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/products?${queryParams(filters, 24)}`);
    setProductsPayload(payload);
  }, [backend.apiBase, filters]);

  const refreshShop = useCallback(async () => {
    await Promise.all([loadHealth(), loadFacets(), loadProducts()]);
  }, [loadFacets, loadHealth, loadProducts]);

  useEffect(() => {
    setStatus(`Loading ${backend.label}.`);
    setDialogState(emptyDialogState);
    refreshShop()
      .then(() => setStatus(`${backend.label} ready for CRUD.`))
      .catch((error) => setStatus(error.message));
  }, [backend.label, refreshShop]);

  const openCreate = () => {
    const template = buildProductTemplate(filters.productType || "laptop");
    setDialogState({ mode: "create", product: null, form: template, originalForm: null, editMode: true, error: "" });
  };

  const openProductDialog = async (product) => {
    try {
      const detail = await fetchJson(`${backend.apiBase}/products/${product._id}`);
      const item = cloneProduct(detail.item);
      setDialogState({ mode: "detail", product: item, form: item, originalForm: cloneProduct(item), editMode: false, error: "" });
    } catch (error) {
      setStatus(error.message);
    }
  };

  const closeDialog = () => setDialogState(emptyDialogState);

  const updateDialogForm = (nextForm) => {
    setDialogState((current) => ({ ...current, form: nextForm, error: "" }));
  };

  const enableDialogEdit = () => {
    setDialogState((current) => ({ ...current, editMode: true, error: "" }));
  };

  const saveDialog = async () => {
    try {
      const isCreate = dialogState.mode === "create";
      const endpoint = isCreate ? `${backend.apiBase}/products` : `${backend.apiBase}/products/${dialogState.product._id}`;
      const method = isCreate ? "POST" : "PUT";
      const result = await fetchJson(endpoint, { method, body: JSON.stringify(sanitizeProductPayload(dialogState.form)) });
      await refreshShop();
      closeDialog();
      setStatus(result.message || `${isCreate ? "Created" : "Updated"} product.`);
    } catch (error) {
      setDialogState((current) => ({ ...current, error: error.message }));
    }
  };

  const deleteDialog = async () => {
    try {
      const product = dialogState.product || dialogState.form;
      if (!product?._id) {
        closeDialog();
        return;
      }
      const confirmed = window.confirm(`Delete ${product.name || product._id}?`);
      if (!confirmed) {
        return;
      }
      const result = await fetchJson(`${backend.apiBase}/products/${product._id}`, { method: "DELETE" });
      await refreshShop();
      closeDialog();
      setStatus(result.message || "Deleted product.");
    } catch (error) {
      setDialogState((current) => ({ ...current, error: error.message }));
    }
  };

  return (
    <main className="shop-shell">
      <section className="shop-toolbar">
        <div>
          <p className="eyebrow">CRUD Workspace</p>
          <h2>{backend.label} Product Catalog</h2>
          <p>{backend.model}; same product contract across both backends.</p>
        </div>
        <div className="toolbar-metrics">
          <span className={`status-pill ${health?.ok ? "ok" : "error"}`}>{health?.label || backend.label}</span>
          {health?.primary ? <span className="status-pill">Primary {health.primary}</span> : null}
          {health?.writeConcern ? <span className="status-pill">w={health.writeConcern}</span> : null}
          <span className="status-pill">{health?.productCount ?? productsPayload?.total ?? 0} products</span>
          <button type="button" className="primary-button" onClick={openCreate}>
            New Product
          </button>
        </div>
      </section>

      <section className="shop-grid">
        <aside className="shop-filters">
          <div className="panel-heading compact">
            <h2>Filters</h2>
          </div>
          <FilterBar facets={facets} filters={filters} onChange={(next) => setFilters((current) => ({ ...current, ...next }))} onClear={() => setFilters(emptyFilters)} />
          <p className="status-message" role="status">
            {status}
          </p>
        </aside>

        <section className="shop-products">
          <div className="panel-heading">
            <div>
              <h2>Products</h2>
              <p>Create, inspect, edit, and delete catalog products.</p>
            </div>
            <span className="result-count">{productsPayload?.total ?? 0} matches</span>
          </div>
          <ProductCards products={productsPayload?.items || []} onOpen={openProductDialog} />
        </section>
      </section>

      <ProductDialog dialogState={dialogState} onChange={updateDialogForm} onEdit={enableDialogEdit} onClose={closeDialog} onSave={saveDialog} onDelete={deleteDialog} />
    </main>
  );
}

function ShowcasePage({ backend }) {
  const [health, setHealth] = useState(null);
  const [facets, setFacets] = useState(null);
  const [filters, setFilters] = useState({ ...emptyFilters, productType: "laptop" });
  const [productsPayload, setProductsPayload] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [selectedDetail, setSelectedDetail] = useState(null);
  const [activeTab, setActiveTab] = useState("shape");
  const [aggregationKind, setAggregationKind] = useState("avgRatingByManufacturer");
  const [aggregation, setAggregation] = useState(null);
  const [scenarioResult, setScenarioResult] = useState(null);
  const [status, setStatus] = useState("Loading showcase.");

  const loadHealth = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/health`);
    setHealth(payload);
  }, [backend.apiBase]);

  const loadFacets = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/facets`);
    setFacets(payload);
  }, [backend.apiBase]);

  const loadProducts = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/products?${queryParams(filters, 12)}`);
    setProductsPayload(payload);
    if (!selectedId || !payload.items.some((product) => product._id === selectedId)) {
      setSelectedId(payload.items[0]?._id || null);
    }
  }, [backend.apiBase, filters, selectedId]);

  const loadAggregation = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/aggregation?kind=${aggregationKind}`);
    setAggregation(payload);
  }, [backend.apiBase, aggregationKind]);

  const refreshShowcase = useCallback(async () => {
    await Promise.all([loadHealth(), loadFacets(), loadProducts(), loadAggregation()]);
  }, [loadAggregation, loadFacets, loadHealth, loadProducts]);

  useEffect(() => {
    setSelectedId(null);
    setSelectedDetail(null);
    setScenarioResult(null);
    setStatus(`Loading ${backend.label} showcase.`);
    Promise.all([loadHealth(), loadFacets()])
      .then(() => setStatus(`${backend.label} showcase ready.`))
      .catch((error) => setStatus(error.message));
  }, [backend.label, loadFacets, loadHealth]);

  useEffect(() => {
    loadProducts().catch((error) => setStatus(error.message));
  }, [loadProducts]);

  useEffect(() => {
    loadAggregation().catch((error) => setStatus(error.message));
  }, [loadAggregation]);

  useEffect(() => {
    if (!selectedId) {
      setSelectedDetail(null);
      return;
    }
    fetchJson(`${backend.apiBase}/products/${selectedId}`)
      .then(setSelectedDetail)
      .catch((error) => setStatus(error.message));
  }, [backend.apiBase, selectedId]);

  const runScenario = async (scenarioId) => {
    try {
      const endpoint = scenarioId === "lazy-migration" ? "lazy-migration" : "category-rename";
      const payload = scenarioId === "lazy-migration" ? { productType: "laptop", taxCode: "DE-STD" } : { categorySlug: "work-essentials", newName: "Work Essentials Live" };
      const result = await fetchJson(`${backend.apiBase}/demo/scenarios/${endpoint}`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setScenarioResult(result);
      setActiveTab("code");
      await refreshShowcase();
      setStatus(`${result.scenario} completed on ${backend.label}.`);
    } catch (error) {
      setStatus(error.message);
    }
  };

  const selectedProduct = selectedDetail?.item;
  const hasTaxCode = selectedProduct && Object.prototype.hasOwnProperty.call(selectedProduct, "regionalTaxCode");
  const codeText = codeTextFor(activeTab, selectedDetail, productsPayload, aggregation);

  return (
    <main className="demo-shell showcase-shell">
      <section className="catalog-panel">
        <div className="panel-heading">
          <div>
            <h2>Dataset</h2>
            <p>
              {backend.label}: {backend.model}
            </p>
          </div>
          <div className="toolbar-metrics">
            <span className={`status-pill ${health?.ok ? "ok" : "error"}`}>{health?.label || backend.label}</span>
            {health?.primary ? <span className="status-pill">Primary {health.primary}</span> : null}
            {health?.writeConcern ? <span className="status-pill">w={health.writeConcern}</span> : null}
          </div>
        </div>
        <FilterBar facets={facets} filters={filters} onChange={(next) => setFilters((current) => ({ ...current, ...next }))} onClear={() => setFilters(emptyFilters)} />
        <ProductList products={productsPayload?.items || []} selectedId={selectedId} onSelect={setSelectedId} />
      </section>

      <section className="insight-panel showcase-insight">
        <div className="panel-heading">
          <div>
            <h2>Document vs. Main Entity</h2>
            <p>{selectedProduct?.name || "Select a product to inspect it."}</p>
          </div>
          <div className="tabs" role="tablist" aria-label="Showcase detail views">
            {[
              ["document", "Document"],
              ["shape", "Shape"],
              ["query", "Query"],
              ["code", "Code"],
            ].map(([tabId, label]) => (
              <button key={tabId} type="button" className={`tab-button ${activeTab === tabId ? "active" : ""}`} onClick={() => setActiveTab(tabId)}>
                {label}
              </button>
            ))}
          </div>
        </div>
        <div className={`schema-banner ${selectedProduct ? (hasTaxCode ? "new" : "old") : ""}`}>
          {selectedProduct
            ? hasTaxCode
              ? `Schema v${selectedProduct.schemaVersion}: regionalTaxCode = ${selectedProduct.regionalTaxCode}`
              : `Schema v${selectedProduct.schemaVersion}: legacy product without regionalTaxCode`
            : "The same API object is backed by different storage models."}
        </div>
        <InsightBody activeTab={activeTab} backend={backend} selectedProduct={selectedProduct} selectedDetail={selectedDetail} codeText={codeText} />
      </section>

      <section className="scenario-panel showcase-tools">
        <ScenarioTools onRun={runScenario} status={status} />
        <ScenarioResult result={scenarioResult} />
        <AggregationPanel facets={facets} aggregationKind={aggregationKind} setAggregationKind={setAggregationKind} aggregation={aggregation} />
      </section>
    </main>
  );
}

function FilterBar({ facets, filters, onChange, onClear }) {
  return (
    <div className="filter-bar">
      <SelectField label="Type" value={filters.productType} onChange={(value) => onChange({ productType: value })} options={facets?.productTypes || []} />
      <SelectField label="Category" value={filters.category} onChange={(value) => onChange({ category: value })} options={facets?.categories || []} valueKey="slug" labelKey="name" />
      <SelectField
        label="Schema"
        value={filters.schemaEvolution}
        onChange={(value) => onChange({ schemaEvolution: value })}
        options={facets?.schemaEvolution || []}
        valueKey="value"
        labelKey="label"
      />
      <label>
        Search
        <input type="search" value={filters.search} onChange={(event) => onChange({ search: event.target.value })} placeholder="name or highlight" />
      </label>
      <button type="button" className="ghost-button" onClick={onClear}>
        Clear
      </button>
    </div>
  );
}

function SelectField({ label, value, onChange, options, valueKey, labelKey }) {
  return (
    <label>
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">All</option>
        {options.map((option) => {
          const optionValue = valueKey ? option[valueKey] : option;
          const optionLabel = labelKey ? option[labelKey] : option;
          return (
            <option key={optionValue} value={optionValue}>
              {optionLabel}
            </option>
          );
        })}
      </select>
    </label>
  );
}

function ProductCards({ products, onOpen }) {
  if (!products.length) {
    return <div className="empty-state">No matching products.</div>;
  }
  return (
    <div className="shop-card-grid">
      {products.map((product) => {
        const rating = averageRating(product);
        const categories = product.categories || [];
        return (
          <button key={product._id} type="button" className="product-card" onClick={() => onOpen(product)}>
            <div className="product-card-topline">
              <span className="type-badge neutral">{product.productType}</span>
              <span className={`availability-badge ${product.status}`}>{product.status}</span>
            </div>
            <div className="product-card-title">
              <strong>{product.name}</strong>
              <span>{product.manufacturer?.name || "Unknown manufacturer"}</span>
            </div>
            <div className="product-card-price">{formatCurrency(product.basePrice, product.currency)}</div>
            <div className="product-card-meta">
              <span>{product.sku}</span>
              <span>{totalInventory(product)} in stock</span>
              <span>{rating ? `${rating} / 5` : "No reviews"}</span>
            </div>
            <div className="chip-list compact">
              {categories.slice(0, 3).map((category) => (
                <span key={`${product._id}-${category.slug || category.id}`}>{category.name}</span>
              ))}
            </div>
          </button>
        );
      })}
    </div>
  );
}

function ProductDialog({ dialogState, onChange, onEdit, onClose, onSave, onDelete }) {
  if (!dialogState.mode) {
    return null;
  }
  const isEditing = dialogState.mode === "create" || dialogState.editMode;
  const isDirty = dialogState.mode === "create" || !isSameProduct(dialogState.form, dialogState.originalForm);
  const title = {
    create: "Create Product",
    detail: "Product Detail",
  }[dialogState.mode];
  const product = dialogState.form || {};

  return (
    <div className="dialog-backdrop" role="presentation">
      <section className="product-dialog" role="dialog" aria-modal="true" aria-labelledby="product-dialog-title">
        <div className="panel-heading">
          <div>
            <h2 id="product-dialog-title">{title}</h2>
            <p>{product.name || "New catalog product"}</p>
          </div>
          <div className="dialog-header-actions">
            {dialogState.mode === "detail" && !dialogState.editMode ? (
              <button type="button" className="ghost-button" onClick={onEdit}>
                Edit
              </button>
            ) : null}
            {dialogState.mode === "detail" ? (
              <button type="button" className="danger-button" onClick={onDelete}>
                Delete
              </button>
            ) : null}
            <button type="button" className="ghost-button" onClick={onClose}>
              Close
            </button>
          </div>
        </div>

        <ProductForm product={product} readOnly={!isEditing} onChange={onChange} />

        {dialogState.error ? (
          <p className="dialog-error" role="alert">
            {dialogState.error}
          </p>
        ) : null}

        <div className="dialog-actions">
          {isEditing ? (
            <button type="button" className="primary-button" onClick={onSave} disabled={!isDirty && dialogState.mode !== "create"}>
              {dialogState.mode === "create" ? "Create Product" : "Save Changes"}
            </button>
          ) : null}
          <button type="button" className="ghost-button" onClick={onClose}>
            Close
          </button>
        </div>
      </section>
    </div>
  );
}

function ProductForm({ product, readOnly, onChange }) {
  const updateField = (fieldName, value) => onChange({ ...product, [fieldName]: value });
  const updateManufacturer = (fieldName, value) => onChange({ ...product, manufacturer: { ...(product.manufacturer || {}), [fieldName]: value } });
  const updateArrayItem = (fieldName, index, nextItem) => {
    const items = [...(product[fieldName] || [])];
    items[index] = nextItem;
    onChange({ ...product, [fieldName]: items });
  };
  const addArrayItem = (fieldName, item) => onChange({ ...product, [fieldName]: [...(product[fieldName] || []), item] });
  const removeArrayItem = (fieldName, index) => onChange({ ...product, [fieldName]: (product[fieldName] || []).filter((_, itemIndex) => itemIndex !== index) });
  const attributes = product.attributes || {};
  const addAttribute = () => {
    const baseKey = "newAttribute";
    let index = 1;
    let nextKey = baseKey;
    while (Object.prototype.hasOwnProperty.call(attributes, nextKey)) {
      index += 1;
      nextKey = `${baseKey}${index}`;
    }
    onChange({ ...product, attributes: { ...attributes, [nextKey]: "" } });
  };
  const renameAttribute = (oldKey, newKey) => {
    if (!newKey || oldKey === newKey) {
      return;
    }
    const nextAttributes = {};
    Object.entries(attributes).forEach(([key, value]) => {
      nextAttributes[key === oldKey ? newKey : key] = value;
    });
    onChange({ ...product, attributes: nextAttributes });
  };
  const updateAttribute = (key, value, type = valueType(attributes[key])) => {
    onChange({ ...product, attributes: { ...attributes, [key]: coerceAttributeValue(value, type) } });
  };
  const removeAttribute = (key) => {
    const nextAttributes = { ...attributes };
    delete nextAttributes[key];
    onChange({ ...product, attributes: nextAttributes });
  };

  return (
    <div className="product-form">
      <section className="form-section product-overview-section">
        <div className="product-detail-hero">
          <div>
            <span className="type-badge neutral">{product.productType || "product"}</span>
            <h3>{product.name || "Unnamed product"}</h3>
            <p>{product.manufacturer?.name || "No manufacturer"}</p>
          </div>
          <div className="product-detail-price">
            <strong>{formatCurrency(product.basePrice, product.currency)}</strong>
            <span>{totalInventory(product)} variants in stock</span>
          </div>
        </div>
        <div className="field-grid three">
          <TextInput label="Name" value={product.name} readOnly={readOnly} onChange={(value) => updateField("name", value)} />
          <TextInput label="SKU" value={product.sku} readOnly={readOnly} onChange={(value) => updateField("sku", value)} />
          <TextInput label="Type" value={product.productType} readOnly={readOnly} onChange={(value) => updateField("productType", value)} />
          <NumberInput label="Base Price" value={product.basePrice} readOnly={readOnly} onChange={(value) => updateField("basePrice", value)} />
          <TextInput label="Currency" value={product.currency} readOnly={readOnly} onChange={(value) => updateField("currency", value)} />
          <TextInput label="Status" value={product.status} readOnly={readOnly} onChange={(value) => updateField("status", value)} />
          <TextInput label="Manufacturer ID" value={product.manufacturer?.id} readOnly={readOnly} onChange={(value) => updateManufacturer("id", value)} />
          <TextInput label="Manufacturer" value={product.manufacturer?.name} readOnly={readOnly} onChange={(value) => updateManufacturer("name", value)} />
          <NumberInput label="Schema Version" value={product.schemaVersion} readOnly={readOnly} onChange={(value) => updateField("schemaVersion", value)} />
          <TextInput label="Regional Tax Code" value={product.regionalTaxCode || ""} readOnly={readOnly} onChange={(value) => updateField("regionalTaxCode", value)} />
          <TextInput label="Source" value={product.source || ""} readOnly={readOnly} onChange={(value) => updateField("source", value)} />
          <ReadOnlyField label="Product ID" value={product.productId || product._id || ""} />
        </div>
      </section>

      <section className="form-section">
        <SectionHeading title="Categories" actionLabel="Add Category" readOnly={readOnly} onAction={() => addArrayItem("categories", { id: "", name: "", slug: "" })} />
        <div className="repeater-list">
          {(product.categories || []).map((category, index) => (
            <div key={`${category.id || category.slug || "category"}-${index}`} className="repeater-row categories-row">
              <TextInput label="ID" value={category.id} readOnly={readOnly} onChange={(value) => updateArrayItem("categories", index, { ...category, id: value })} />
              <TextInput label="Name" value={category.name} readOnly={readOnly} onChange={(value) => updateArrayItem("categories", index, { ...category, name: value })} />
              <TextInput label="Slug" value={category.slug} readOnly={readOnly} onChange={(value) => updateArrayItem("categories", index, { ...category, slug: value })} />
              <RemoveButton readOnly={readOnly} onClick={() => removeArrayItem("categories", index)} />
            </div>
          ))}
        </div>
      </section>

      <section className="form-section">
        <SectionHeading title="Dynamic Attributes" actionLabel="Add Attribute" readOnly={readOnly} onAction={addAttribute} />
        <div className="repeater-list">
          {Object.entries(attributes).map(([key, value]) => (
            <div key={key} className="repeater-row attributes-row">
              <TextInput label="Key" value={key} readOnly={readOnly} onChange={(nextKey) => renameAttribute(key, nextKey.trim())} />
              <label>
                Type
                <select value={valueType(value)} disabled={readOnly} onChange={(event) => updateAttribute(key, value, event.target.value)}>
                  {attributeTypeOptions.map((type) => (
                    <option key={type} value={type}>
                      {type}
                    </option>
                  ))}
                </select>
              </label>
              <AttributeValueInput attributeValue={value} readOnly={readOnly} onChange={(nextValue) => updateAttribute(key, nextValue)} />
              <RemoveButton readOnly={readOnly} onClick={() => removeAttribute(key)} />
            </div>
          ))}
        </div>
      </section>

      <section className="form-section">
        <SectionHeading title="Variants" actionLabel="Add Variant" readOnly={readOnly} onAction={() => addArrayItem("variants", { variantId: "", label: "", inventoryCount: 0 })} />
        <div className="repeater-list">
          {(product.variants || []).map((variant, index) => (
            <div key={`${variant.variantId || "variant"}-${index}`} className="repeater-row variants-row">
              <TextInput label="Variant ID" value={variant.variantId} readOnly={readOnly} onChange={(value) => updateArrayItem("variants", index, { ...variant, variantId: value })} />
              <TextInput label="Label" value={variant.label} readOnly={readOnly} onChange={(value) => updateArrayItem("variants", index, { ...variant, label: value })} />
              <NumberInput label="Inventory" value={variant.inventoryCount} readOnly={readOnly} onChange={(value) => updateArrayItem("variants", index, { ...variant, inventoryCount: value })} />
              <RemoveButton readOnly={readOnly} onClick={() => removeArrayItem("variants", index)} />
            </div>
          ))}
        </div>
      </section>

      <section className="form-section">
        <SectionHeading title="Highlights" actionLabel="Add Highlight" readOnly={readOnly} onAction={() => addArrayItem("highlights", "")} />
        <div className="repeater-list">
          {(product.highlights || []).map((highlight, index) => (
            <div key={`${highlight || "highlight"}-${index}`} className="repeater-row highlights-row">
              <TextInput label={`Highlight ${index + 1}`} value={highlight} readOnly={readOnly} onChange={(value) => updateArrayItem("highlights", index, value)} />
              <RemoveButton readOnly={readOnly} onClick={() => removeArrayItem("highlights", index)} />
            </div>
          ))}
        </div>
      </section>

      <section className="form-section">
        <SectionHeading title="Reviews" actionLabel="Add Review" readOnly={readOnly} onAction={() => addArrayItem("latestReviews", { reviewId: nextReviewId(product), rating: 5, title: "" })} />
        <div className="review-summary">
          <strong>{averageRating(product) || "-"}</strong>
          <span>{(product.latestReviews || []).length} reviews</span>
        </div>
        <div className="repeater-list">
          {(product.latestReviews || []).map((review, index) => (
            <div key={`${review.reviewId || "review"}-${index}`} className="repeater-row reviews-row">
              <TextInput label="Review ID" value={review.reviewId} readOnly={readOnly} onChange={(value) => updateArrayItem("latestReviews", index, { ...review, reviewId: value })} />
              <NumberInput label="Rating" value={review.rating} min="1" max="5" readOnly={readOnly} onChange={(value) => updateArrayItem("latestReviews", index, { ...review, rating: value })} />
              <TextInput label="Title" value={review.title} readOnly={readOnly} onChange={(value) => updateArrayItem("latestReviews", index, { ...review, title: value })} />
              <RemoveButton readOnly={readOnly} onClick={() => removeArrayItem("latestReviews", index)} />
            </div>
          ))}
        </div>
      </section>

      <section className="form-section compact-meta">
        <div className="field-grid two">
          <ReadOnlyField label="Created At" value={product.createdAt || ""} />
          <ReadOnlyField label="Updated At" value={product.updatedAt || ""} />
        </div>
      </section>
    </div>
  );
}

function SectionHeading({ title, actionLabel, readOnly, onAction }) {
  return (
    <div className="section-heading">
      <h3>{title}</h3>
      {!readOnly ? (
        <button type="button" className="ghost-button" onClick={onAction}>
          {actionLabel}
        </button>
      ) : null}
    </div>
  );
}

function TextInput({ label, value, readOnly, onChange }) {
  return (
    <label>
      {label}
      <input type="text" value={value ?? ""} disabled={readOnly} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function NumberInput({ label, value, readOnly, onChange, min, max }) {
  return (
    <label>
      {label}
      <input type="number" min={min} max={max} value={value ?? ""} disabled={readOnly} onChange={(event) => onChange(event.target.value === "" ? "" : Number(event.target.value))} />
    </label>
  );
}

function AttributeValueInput({ attributeValue, readOnly, onChange }) {
  if (typeof attributeValue === "boolean") {
    return (
      <label>
        Value
        <select value={String(attributeValue)} disabled={readOnly} onChange={(event) => onChange(event.target.value)}>
          <option value="true">true</option>
          <option value="false">false</option>
        </select>
      </label>
    );
  }
  if (typeof attributeValue === "number") {
    return <NumberInput label="Value" value={attributeValue} readOnly={readOnly} onChange={onChange} />;
  }
  return <TextInput label="Value" value={attributeValue} readOnly={readOnly} onChange={onChange} />;
}

function ReadOnlyField({ label, value }) {
  return (
    <label>
      {label}
      <input type="text" value={value ?? ""} disabled />
    </label>
  );
}

function RemoveButton({ readOnly, onClick }) {
  if (readOnly) {
    return <span className="row-spacer" aria-hidden="true" />;
  }
  return (
    <button type="button" className="danger-button compact-button" onClick={onClick} aria-label="Remove row">
      Remove
    </button>
  );
}

function ProductList({ products, selectedId, onSelect }) {
  if (!products.length) {
    return <div className="empty-state">No matching products.</div>;
  }
  return (
    <div className="product-list">
      {products.map((product) => (
        <button key={product._id} type="button" className={`product-item ${selectedId === product._id ? "active" : ""}`} onClick={() => onSelect(product._id)}>
          <div>
            <strong>{product.name}</strong>
            <span>
              {formatCurrency(product.basePrice, product.currency)} - {product.manufacturer?.name}
            </span>
          </div>
          <span className="type-badge">{product.productType}</span>
        </button>
      ))}
    </div>
  );
}

function InsightBody({ activeTab, backend, selectedProduct, selectedDetail, codeText }) {
  if (activeTab === "shape") {
    return <StorageShape backend={backend} product={selectedProduct} summary={selectedDetail?.storageSummary} />;
  }
  return <pre className="code-block">{activeTab === "document" ? JSON.stringify(selectedProduct || {}, null, 2) : codeText}</pre>;
}

function StorageShape({ backend, product, summary }) {
  if (!product) {
    return <div className="shape-view">Select a product to compare the storage shape.</div>;
  }
  const commonFields = ["id", "product", "manufacturer", "categories", "attributes", "variants", "reviews"];
  const postgresTables = ["products", "manufacturers", "product_categories", "categories", "product_attributes", "product_variants", "product_reviews"];
  const cards =
    backend.id === "mongo"
      ? [
          { title: "root document", fields: ["_id", "productType", "basePrice", "schemaVersion"] },
          { title: "embedded arrays", fields: ["categories[]", "variants[]", "latestReviews[]", "highlights[]"] },
          { title: "embedded objects", fields: ["manufacturer", "attributes"] },
        ]
      : postgresTables.map((table) => ({ title: table, fields: commonFields.filter((field) => table.includes(field.slice(0, 7)) || table === "products") }));
  return (
    <div className="shape-view">
      <div className={`shape-summary ${backend.accent}`}>
        <strong>{backend.label}</strong>
        <p>{summary}</p>
      </div>
      <div className="shape-grid">
        {cards.map((card) => (
          <article key={card.title}>
            <h3>{card.title}</h3>
            <div className="chip-list">
              {card.fields.map((field) => (
                <span key={field}>{field}</span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}

function ScenarioTools({ onRun, status }) {
  return (
    <div className="scenario-result">
      <h2>Database Tools</h2>
      <p>Run targeted modeling scenarios without story-step navigation.</p>
      <div className="row-actions stacked">
        <button type="button" onClick={() => onRun("lazy-migration")}>
          Run Lazy Migration
        </button>
        <button type="button" onClick={() => onRun("category-rename")}>
          Rename Category
        </button>
      </div>
      <p className="status-message compact" role="status">
        {status}
      </p>
    </div>
  );
}

function ScenarioResult({ result }) {
  if (!result) {
    return (
      <div className="scenario-result empty">
        <h2>Scenario Result</h2>
        <p>Run a database tool to show counts, trade-offs, query, and code.</p>
      </div>
    );
  }
  const metrics = Object.entries(result).filter(([key, value]) => typeof value === "number" && !key.toLowerCase().includes("version"));
  return (
    <div className="scenario-result">
      <h2>{result.scenario}</h2>
      <p>{result.headline || result.message}</p>
      <div className="metric-row">
        {metrics.map(([key, value]) => (
          <div key={key} className="metric-card">
            <span>{key}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
      <pre className="code-block small">{result.queryText || result.codeText || "No query for this scenario."}</pre>
    </div>
  );
}

function AggregationPanel({ facets, aggregationKind, setAggregationKind, aggregation }) {
  const keys = aggregation?.results?.length ? Array.from(new Set(aggregation.results.flatMap((row) => Object.keys(row)))) : [];
  return (
    <div className="aggregation-card">
      <div className="panel-heading compact">
        <h2>Analytics</h2>
        <select value={aggregationKind} onChange={(event) => setAggregationKind(event.target.value)} aria-label="Aggregation kind">
          {(facets?.aggregations || []).map((item) => (
            <option key={item.kind} value={item.kind}>
              {item.label}
            </option>
          ))}
        </select>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              {keys.map((key) => (
                <th key={key}>{key === "_id" ? "group" : key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {(aggregation?.results || []).map((row, rowIndex) => (
              <tr key={`${row._id}-${rowIndex}`}>
                {keys.map((key) => (
                  <td key={key}>{formatCell(row[key])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <pre className="code-block small">{aggregation?.queryText || "Loading aggregation."}</pre>
    </div>
  );
}

function codeTextFor(activeTab, selectedDetail, productsPayload, aggregation) {
  if (activeTab === "query") {
    return selectedDetail?.queryText || productsPayload?.queryText || "Load products to see the list query.";
  }
  if (activeTab === "code") {
    return selectedDetail?.codeText || productsPayload?.codeText || "Load products to see the driver code.";
  }
  if (activeTab === "aggregation") {
    return aggregation?.queryText || "Run an aggregation to see the query.";
  }
  return JSON.stringify(selectedDetail?.item || productsPayload?.items?.[0] || {}, null, 2);
}

function buildProductTemplate(productType) {
  const safeType = productType || "laptop";
  const now = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const productId = `manual_${safeType.replace(/[^a-z0-9]+/gi, "_").toLowerCase()}_${Date.now()}`;
  return {
    _id: productId,
    productId,
    sku: `MAN-${safeType.slice(0, 3).toUpperCase()}-${String(Date.now()).slice(-5)}`,
    productType: safeType,
    name: `Manual ${safeType} product`,
    basePrice: 99,
    currency: "EUR",
    manufacturer: { id: "man_manual", name: "Manual Demo Goods" },
    categories: [{ id: "cat_manual", name: "Manual Demo", slug: "manual-demo" }],
    attributes: { demoEditable: true },
    variants: [{ variantId: "var_default", label: "Default", inventoryCount: 10 }],
    highlights: ["form editable", "crud demo"],
    latestReviews: [{ reviewId: "rev_manual_1", rating: 5, title: "Created in the CRUD dialog" }],
    status: "available",
    schemaVersion: 2,
    regionalTaxCode: "DE-STD",
    source: "manual-crud",
    createdAt: now,
    updatedAt: now,
  };
}

createRoot(document.getElementById("root")).render(<App />);
