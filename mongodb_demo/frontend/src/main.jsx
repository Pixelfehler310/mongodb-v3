import React, { useCallback, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const backends = [
  { id: "mongo", label: "MongoDB", apiBase: "/api/mongo", model: "embedded document", accent: "document-local" },
  { id: "postgres", label: "PostgreSQL", apiBase: "/api/postgres", model: "normalized tables", accent: "relational" },
];

const storySteps = [
  { id: "catalog", label: "Catalog", title: "Same app, two backends" },
  { id: "shape", label: "Shape", title: "Document vs. main entity" },
  { id: "schema", label: "Schema", title: "Lazy schema evolution" },
  { id: "update", label: "Update", title: "Denormalized category rename" },
  { id: "analytics", label: "Analytics", title: "Cross-entity aggregation" },
];

const emptyFilters = {
  productType: "",
  category: "",
  schemaEvolution: "",
  search: "",
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

function queryParams(filters) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (String(value).trim()) {
      params.set(key, String(value).trim());
    }
  });
  params.set("limit", "12");
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

function App() {
  const [backendId, setBackendId] = useState("mongo");
  const [storyStep, setStoryStep] = useState("catalog");
  const [filters, setFilters] = useState(emptyFilters);
  const [health, setHealth] = useState(null);
  const [facets, setFacets] = useState(null);
  const [productsPayload, setProductsPayload] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [selectedDetail, setSelectedDetail] = useState(null);
  const [activeTab, setActiveTab] = useState("document");
  const [aggregationKind, setAggregationKind] = useState("avgPriceByType");
  const [aggregation, setAggregation] = useState(null);
  const [scenarioResult, setScenarioResult] = useState(null);
  const [status, setStatus] = useState("Loading demo data.");

  const backend = useMemo(() => backends.find((item) => item.id === backendId) || backends[0], [backendId]);

  const loadHealth = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/api/health`);
    setHealth(payload);
  }, [backend.apiBase]);

  const loadFacets = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/api/facets`);
    setFacets(payload);
  }, [backend.apiBase]);

  const loadProducts = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/api/products?${queryParams(filters)}`);
    setProductsPayload(payload);
    if (!selectedId || !payload.items.some((item) => item._id === selectedId)) {
      setSelectedId(payload.items[0]?._id || null);
    }
  }, [backend.apiBase, filters, selectedId]);

  const loadAggregation = useCallback(async () => {
    const payload = await fetchJson(`${backend.apiBase}/api/aggregation?kind=${aggregationKind}`);
    setAggregation(payload);
  }, [backend.apiBase, aggregationKind]);

  useEffect(() => {
    setStatus("Loading selected backend.");
    setSelectedId(null);
    setSelectedDetail(null);
    setScenarioResult(null);
    Promise.all([loadHealth(), loadFacets()])
      .then(() => setStatus(`${backend.label} ready.`))
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
    fetchJson(`${backend.apiBase}/api/products/${selectedId}`)
      .then(setSelectedDetail)
      .catch((error) => setStatus(error.message));
  }, [backend.apiBase, selectedId]);

  const refreshAll = useCallback(async () => {
    await Promise.all([loadHealth(), loadFacets(), loadProducts(), loadAggregation()]);
  }, [loadAggregation, loadFacets, loadHealth, loadProducts]);

  const runScenario = async (scenarioId) => {
    try {
      const endpoint = scenarioId === "lazy-migration" ? "lazy-migration" : "category-rename";
      const payload = scenarioId === "lazy-migration" ? { productType: "laptop", taxCode: "DE-STD" } : { categorySlug: "work-essentials", newName: "Work Essentials Live" };
      const result = await fetchJson(`${backend.apiBase}/api/demo/scenarios/${endpoint}`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setScenarioResult(result);
      setStoryStep(scenarioId === "lazy-migration" ? "schema" : "update");
      setActiveTab("code");
      await refreshAll();
      setStatus(`${result.scenario} completed on ${backend.label}.`);
    } catch (error) {
      setStatus(error.message);
    }
  };

  const insertSample = async () => {
    try {
      const productType = filters.productType || "laptop";
      const payload = await fetchJson(`${backend.apiBase}/api/products/sample`, {
        method: "POST",
        body: JSON.stringify({ productType }),
      });
      await refreshAll();
      setSelectedId(payload.item._id);
      setScenarioResult({ ...payload, scenario: "sample-insert", headline: payload.message });
      setStatus(payload.message);
    } catch (error) {
      setStatus(error.message);
    }
  };

  const selectedProduct = selectedDetail?.item;
  const hasTaxCode = selectedProduct && Object.prototype.hasOwnProperty.call(selectedProduct, "regionalTaxCode");
  const codeText = codeTextFor(activeTab, selectedDetail, productsPayload, aggregation);

  return (
    <>
      <header className="topbar">
        <div>
          <p className="eyebrow">Presentation Demo</p>
          <h1>Product Catalog Trade-offs</h1>
        </div>
        <div className="topbar-actions">
          <span className={`status-pill ${health?.ok ? "ok" : "error"}`}>{health?.label || "backend"}</span>
          <div className="segmented" aria-label="Data backend">
            {backends.map((item) => (
              <button key={item.id} type="button" className={backendId === item.id ? "active" : ""} onClick={() => setBackendId(item.id)}>
                {item.label}
              </button>
            ))}
          </div>
          <button type="button" className="primary-button" onClick={insertSample}>
            Insert Sample
          </button>
        </div>
      </header>

      <main className="demo-shell">
        <aside className="story-panel">
          <div className="panel-heading compact">
            <h2>Story</h2>
          </div>
          <div className="story-steps">
            {storySteps.map((step) => (
              <button key={step.id} type="button" className={storyStep === step.id ? "active" : ""} onClick={() => setStoryStep(step.id)}>
                <span>{step.label}</span>
                <small>{step.title}</small>
              </button>
            ))}
          </div>
          <ScenarioControls onRun={runScenario} backend={backend} />
          <p className="status-message" role="status">
            {status}
          </p>
        </aside>

        <section className="catalog-panel">
          <div className="panel-heading">
            <div>
              <h2>Catalog</h2>
              <p>
                {backend.label}: {backend.model}
              </p>
            </div>
            <span className="result-count">{productsPayload?.total ?? 0} products</span>
          </div>
          <FilterBar facets={facets} filters={filters} onChange={(next) => setFilters((current) => ({ ...current, ...next }))} onClear={() => setFilters(emptyFilters)} />
          <ProductList products={productsPayload?.items || []} selectedId={selectedId} onSelect={setSelectedId} />
        </section>

        <section className="insight-panel">
          <div className="panel-heading">
            <div>
              <h2>{storySteps.find((step) => step.id === storyStep)?.title}</h2>
              <p>{selectedProduct?.name || "Select a product to inspect it."}</p>
            </div>
            <div className="tabs" role="tablist" aria-label="Detail views">
              {["document", "shape", "query", "code"].map((tab) => (
                <button key={tab} type="button" className={`tab-button ${activeTab === tab ? "active" : ""}`} onClick={() => setActiveTab(tab)}>
                  {tab === "shape" ? "Shape" : tab[0].toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
          </div>
          <div className={`schema-banner ${selectedProduct ? (hasTaxCode ? "new" : "old") : ""}`}>
            {selectedProduct
              ? hasTaxCode
                ? `Schema v${selectedProduct.schemaVersion}: regionalTaxCode = ${selectedProduct.regionalTaxCode}`
                : `Schema v${selectedProduct.schemaVersion}: legacy product without regionalTaxCode`
              : "The same UI contract is served by both database models."}
          </div>
          <InsightBody activeTab={activeTab} backend={backend} selectedProduct={selectedProduct} selectedDetail={selectedDetail} codeText={codeText} />
        </section>

        <section className="scenario-panel">
          <ScenarioResult result={scenarioResult} />
          <AggregationPanel facets={facets} aggregationKind={aggregationKind} setAggregationKind={setAggregationKind} aggregation={aggregation} />
        </section>
      </main>
    </>
  );
}

function ScenarioControls({ onRun, backend }) {
  return (
    <div className="scenario-controls">
      <h3>Simulate</h3>
      <button type="button" onClick={() => onRun("lazy-migration")}>
        Run Lazy Migration
      </button>
      <button type="button" onClick={() => onRun("category-rename")}>
        Rename Category
      </button>
      <p>{backend.label} executes the same demo scenario through its own storage model.</p>
    </div>
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

function ScenarioResult({ result }) {
  if (!result) {
    return (
      <div className="scenario-result empty">
        <h2>Scenario Result</h2>
        <p>Run a simulation to show counts, trade-offs, query, and code.</p>
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
            {(aggregation?.results || []).map((row, index) => (
              <tr key={`${row._id}-${index}`}>
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

createRoot(document.getElementById("root")).render(<App />);